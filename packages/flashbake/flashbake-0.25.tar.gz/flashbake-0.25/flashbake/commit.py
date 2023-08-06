#
#  commit.py
#  Parses a project's control file and wraps git operations, calling the context
#  script to build automatic commit messages as needed.

import os
import sys
import re
import datetime
import time
import logging
import context
# this import is only valid for Linux
import commands
# Import smtplib for the actual sending function
import smtplib
import flashbake
import git

# Import the email modules we'll need
if sys.hexversion < 0x2050000:
    from email.MIMEText import MIMEText
else:
    from email.mime.text import MIMEText

def parsecontrol(project_dir, control_file, config = None, results = None):
    """ Parse the dot-control file to get config options and hot files. """

    logging.debug('Checking %s' % control_file)

    if None == results:
        hot_files = flashbake.HotFiles(project_dir)
    else:
        hot_files = results
        
    if None == config:
        control_config = flashbake.ControlConfig()
    else:
        control_config = config

    control_file = open(control_file, 'r')
    try:
        for line in control_file:
            # skip anything else if the config consumed the line
            if __capture(control_config, line):
                continue

            hot_files.addfile(line.strip())
    finally:
        control_file.close()
        
    return (hot_files, control_config)

def preparecontrol(hot_files, control_config):
    control_config.init()
    logging.debug("loading file plugins")
    for plugin in control_config.file_plugins:
        logging.debug("running plugin %s" % plugin)
        plugin.processfiles(hot_files, control_config)
    return (hot_files, control_config)
    
def commit(control_config, hot_files, quiet_mins, dryrun):
    # change to the project directory, necessary to find the .flashbake file and
    # to correctly refer to the project files by relative paths
    os.chdir(hot_files.project_dir)

    git_obj = git.Git(hot_files.project_dir, control_config.git_path)

    control_config.dryrun = dryrun

    # the wrapper object ensures git is on the path
    git_status = git_obj.status()

    # get the git status for the project
    if git_status.startswith('fatal'):
        logging.error('Fatal error from git.')
        if 'fatal: Not a git repository' == git_status:
            logging.error('Make sure "git init" was run in %s'
                % os.path.realpath(hot_files.project_dir))
        else:
            logging.error(git_status)
        sys.exit(1)

    # in particular find the existing entries that need a commit
    pending_re = re.compile('#\s*(renamed|copied|modified|new file):.*')

    now = datetime.datetime.today()
    quiet_period = datetime.timedelta(minutes=quiet_mins)

    to_commit = list()
    # first look in the files git already knows about
    logging.debug("Examining git status.")
    for line in git_status.splitlines():
        if pending_re.match(line):
            pending_file = __trimgit(line)

            # not in the dot-control file, skip it
            if not (hot_files.contains(pending_file)):
                continue

            logging.debug('Parsing status line %s to determine commit action' % line)

            # remove files that will be considered for commit
            hot_files.remove(pending_file)

            # check the quiet period against mtime
            last_mod = os.path.getmtime(pending_file)
            pending_mod = datetime.datetime.fromtimestamp(last_mod)
            pending_mod += quiet_period

            # add the file to the list to include in the commit
            if pending_mod < now:
                to_commit.append(pending_file)
                logging.debug('Flagging file, %s, for commit.' % pending_file)
            else:
                logging.debug('Change for file, %s, is too recent.' % pending_file)

    logging.debug('Examining unknown or unchanged files.')

    hot_files.warnproblems()

    # figure out what the status of the remaining files is
    for control_file in hot_files.control_files:
        # this shouldn't happen since HotFiles.addfile uses glob.iglob to expand
        # the original file lines which does so based on what is in project_dir
        if not os.path.exists(control_file):
            logging.debug('%s does not exist yet.' % control_file)
            hot_files.putabsent(control_file)
            continue

        status_output = git_obj.status(control_file)

        if status_output.startswith('error'):
            if status_output.find('did not match') > 0:
                hot_files.putneedsadd(control_file)
                logging.debug('%s exists but is unknown by git.' % control_file)
            else:
                logging.error('Unknown error occurred!')
                logging.error(status_output)
            continue
        # use a regex to match so we can enforce whole word rather than
        # substring matchs, otherwise 'foo.txt~' causes a false report of an
        # error
        control_re = re.compile('\<' + re.escape(control_file) + '\>')
        if control_re.search(status_output) == None:
            logging.debug('%s has no uncommitted changes.' % control_file)
        # if anything hits this block, we need to figure out why
        else:
            logging.error('%s is in the status message but failed other tests.' % control_file)
            logging.error('Try \'git status "%s"\' for more info.' % control_file)

    hot_files.addorphans(git_obj, control_config)

    if len(to_commit) > 0:
        logging.info('Committing changes to known files, %s.' % to_commit)
        message_file = context.buildmessagefile(control_config)
        if not dryrun:
            # consolidate the commit to be friendly to how git normally works
            commit_output = git_obj.commit(message_file, to_commit)
            logging.debug(commit_output)
        os.remove(message_file)
        logging.info('Commit for known files complete.')
    else:
        logging.info('No changes to known files found to commit.')

    if hot_files.needsnotice():
        __sendnotice(control_config, hot_files)
    else:
        logging.info('No missing or untracked files found, not sending email notice.')
        
def __capture(config, line):
    """ Used by the dot-control parsing code to capture files and properties
        as they are encountered. """
    # grab comments but don't do anything
    if line.startswith('#'):
        return True

    # grab blanks but don't do anything
    if len(line.strip()) == 0:
        return True

    if line.find(':') > 0:
        prop_tokens = line.split(':', 1)
        prop_name = prop_tokens[0].strip()
        prop_value = prop_tokens[1].strip()

        if 'plugins' == prop_name:
           config.addplugins(prop_value.split(','))
           return True

        # hang onto any extra propeties in case plugins use them
        if not prop_name in config.__dict__:
            config.extra_props[prop_name] = prop_value;
            return True

        try:
            if prop_name in config.prop_types:
                prop_value = config.prop_types[prop_name](prop_value)
            config.__dict__[prop_name] = prop_value
        except:
            raise flashbake.ConfigError(
                    'The value, %s, for option, %s, could not be parse as %s.'
                    % (prop_value, prop_name, config.prop_types[prop_name]))

        return True

    return False

def __trimgit(status_line):
    if status_line.find('->') >= 0:
        tokens = status_line.split('->')
        return tokens[1].strip()

    tokens = status_line.split(':')
    return tokens[1].strip()

def __sendnotice(control_config, hot_files):
    if (None == control_config.notice_to
            and not control_config.dryrun):
        logging.info('Skipping notice, no notice_to: recipient set.')
        return

    body = ''
    
    if len(hot_files.not_exists) > 0:
        body += '\nThe following files do not exist:\n\n'

        for file in hot_files.not_exists:
           body += '\t' + file + '\n'

        body += '\nMake sure there is not a typo in .flashbake and that you created/saved the file.\n'
    
    if len(hot_files.linked_files) > 0:
        body += '\nThe following files in .flashbake are links or have a link in their directory path.\n\n'

        for (file, link) in hot_files.linked_files.iteritems():
            if file == link:
                body += '\t' + file + ' is a link\n'
            else:
                body += '\t' + link + ' is a link on the way to ' + file + '\n'

        body += '\nMake sure the physical file and its parent directories reside in the project directory.\n'
    
    if len(hot_files.outside_files) > 0:
        body += '\nThe following files in .flashbake are not in the project directory.\n\n'

        for file in hot_files.outside_files:
           body += '\t' + file + '\n'

        body += '\nOnly files in the project directory can be tracked and committed.\n'


    if control_config.dryrun:
        logging.debug(body)
        if control_config.notice_to != None:
            logging.info('Dry run, skipping email notice.')
        return

    # Create a text/plain message
    msg = MIMEText(body, 'plain')

    msg['Subject'] = ('Some files in %s do not exist'
            % os.path.realpath(hot_files.project_dir))
    msg['From'] = control_config.notice_from
    msg['To'] = control_config.notice_to

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    logging.debug('\nConnecting to SMTP on host %s, port %d'
            % (control_config.smtp_host, control_config.smtp_port))

    try:
        s = smtplib.SMTP()
        s.connect(host=control_config.smtp_host,port=control_config.smtp_port)
        logging.info('Sending notice to %s.' % control_config.notice_to)
        logging.debug(body)
        s.sendmail(control_config.notice_from, [control_config.notice_to], msg.as_string())
        logging.info('Notice sent.')
        s.close()
    except Exception, e:
        logging.error('Couldn\'t connect, will send later.')
        logging.debug("SMTP Error:\n" + str(e));
