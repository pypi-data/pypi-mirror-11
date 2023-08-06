#
#  __init__.py
#  Shared classes and functions for the flashbake package.
    
import os
import os.path
import logging
import sys
import commands
import glob
from types import *
import flashbake.plugins
from flashbake.plugins import PluginError, PLUGIN_ERRORS


class ConfigError(Exception):
    pass

class ControlConfig:
    """ Accumulates options from a control file for use by the core modules as
        well as for the plugins.  Also handles boot strapping the configured
        plugins. """
    def __init__(self):
        self.initialized = False
        self.extra_props = dict()

        self.email = None
        self.notice_to = None
        self.notice_from = None
        self.smtp_host = 'localhost'
        self.smtp_port = 25
        
        self.prop_types = dict()
        self.prop_types['smtp_port'] = int

        self.plugin_names = list()
        self.plugins = list()

        self.git_path = None

    def init(self):
        """ Do any property clean up, after parsing but before use """
        if self.initialized == True:
            return

        if self.notice_from == None and self.notice_to != None:
            self.notice_from = self.notice_to

        if len(self.plugin_names) == 0:
            logging.debug('No plugins configured, enabling the stock set.')
            raise ConfigError('No plugins configured!')

        for plugin_name in self.plugin_names:
            plugin = self.initplugin(plugin_name)
            self.plugins.append(plugin)

    def sharedproperty(self, name, type = None):
        """ Declare a shared property, this way multiple plugins can share some
            value through the config object. """
        if name in self.__dict__:
            return

        value = None

        if name in self.extra_props:
            value = self.extra_props[name]
            del self.extra_props[name]

            if type != None:
                try:
                    value = type(value)
                except:
                    raise ConfigError('Problem parsing %s for option %s'
                            % (name, value))
            self.__dict__[name] = value

    def addplugins(self, plugin_names):
        # use a comprehension to ensure uniqueness
        [self.__add_last(inbound_name) for inbound_name in plugin_names]

    def initplugin(self, plugin_spec):
        """ Initialize a plugin, including vetting that it meets the correct
            protocol; not private so it can be used in testing. """
        if plugin_spec.find(':') < 0:
            raise PluginError(PLUGIN_ERRORS.invalid_plugin, plugin_spec)

        tokens = plugin_spec.split(':')
        module_name = tokens[0]
        plugin_name = tokens[1]

        try:
            __import__(module_name)
        except ImportError:
            logging.warn('Invalid module, %s' % plugin_name)
            raise PluginError(PLUGIN_ERRORS.unknown_plugin, plugin_spec)

        try:
            # TODO re-visit pkg_resources, EntryPoint
            plugin_class = self.__forname(module_name, plugin_name)
            plugin = plugin_class(plugin_spec)
        except:
            logging.debug('Couldn\'t load class %s' % plugin_spec)
            raise PluginError(PLUGIN_ERRORS.unknown_plugin, plugin_spec)
        if not isinstance(plugin, flashbake.plugins.AbstractMessagePlugin):
            raise PluginError(PLUGIN_ERRORS.invalid_type, plugin_spec)
        self.__checkattr(plugin_spec, plugin, 'connectable', bool)
        self.__checkattr(plugin_spec, plugin, 'addcontext', MethodType)

        plugin.init(self)

        return plugin

    def __add_last(self, plugin_name):
        if plugin_name in self.plugin_names:
            self.plugin_names.remove(plugin_name) 
        self.plugin_names.append(plugin_name)

    def __checkattr(self, plugin_spec, plugin, name, expected_type):
        try:
            attrib = eval('plugin.%s' % name)
        except AttributeError:
            raise PluginError(PLUGIN_ERRORS.missing_attribute, plugin_spec, name)

        if not isinstance(attrib, expected_type):
            raise PluginError(PLUGIN_ERRORS.invalid_attribute, plugin_spec, name)

    # with thanks to Ben Snider
    # http://www.bensnider.com/2008/02/27/dynamically-import-and-instantiate-python-classes/
    def __forname(self, module_name, plugin_name):
        ''' Returns a class of "plugin_name" from module "module_name". '''
        module = __import__(module_name)
        module = sys.modules[module_name]
        classobj = getattr(module, plugin_name)
        return classobj

class HotFiles:
    """
    Track the files as they are parsed and manipulated with regards to their git
    status and the dot-control file.
    """
    def __init__(self, project_dir):
        self.project_dir = os.path.realpath(project_dir)
        self.linked_files = dict()
        self.outside_files = set()
        self.control_files = set()
        self.not_exists = set()
        self.to_add = set()

    def addfile(self, filename):
        to_expand = os.path.join(self.project_dir, filename)
        file_exists = False
        logging.debug('%s: %s'
               % (filename, glob.glob(to_expand)))
        if sys.hexversion < 0x2050000:
            glob_iter = glob.glob(to_expand)
        else:
            glob_iter = glob.iglob(to_expand)

        for expanded_file in glob_iter:
            # track whether iglob iterates at all, if it does not, then the line
            # didn't expand to anything meaningful
            if not file_exists:
                file_exists = True

            # skip the file if some previous glob hit it
            if (expanded_file in self.outside_files
                    or expanded_file in self.linked_files.keys()):
                continue

            # the commit code expects a relative path
            rel_file = self.__make_rel(expanded_file)

            # skip the file if some previous glob hit it
            if rel_file in self.control_files:
                continue

            # checking this after removing the expanded project directory
            # catches absolute paths to files outside the project directory
            if rel_file == expanded_file:
                self.outside_files.add(expanded_file)
                continue

            link = self.__check_link(expanded_file)

            if link == None:
                self.control_files.add(rel_file)
            else:
                self.linked_files[expanded_file] = link
                
        if not file_exists:
            self.putabsent(filename)

    def contains(self, filename):
        return filename in self.control_files

    def remove(self, filename):
        self.control_files.remove(filename)

    def putabsent(self, filename):
        self.not_exists.add(filename)

    def putneedsadd(self, filename):
        self.to_add.add(filename)

    def warnproblems(self):
        # print warnings for linked files
        for filename in self.linked_files.keys():
            logging.info('%s is a link or its directory path contains a link.' % filename)
        # print warnings for files outside the project
        for filename in self.outside_files:
            logging.info('%s is outside the project directory.' % filename)
        # print warnings for files outside the project
        for filename in self.not_exists:
            logging.info('%s does not exist.' % filename)

    def addorphans(self, git_obj, control_config):
        if len(self.to_add) == 0:
            return

        message_file = context.buildmessagefile(control_config)

        to_commit = list()
        for orphan in self.to_add:
            logging.debug('Adding %s.' % orphan)
            add_output = git_obj.add(orphan)
            logging.debug('Add output, %s' % orphan)
            to_commit.append(orphan)

        logging.info('Adding new files, %s.' % to_commit)
        # consolidate the commit to be friendly to how git normally works
        if not control_config.dryrun:
            commit_output = git_obj.commit(message_file, to_commit)
            logging.debug('Commit output, %s' % commit_output)

        os.remove(message_file)

    def needsnotice(self):
        return (len(self.not_exists) > 0
               or len(self.linked_files) > 0
               or len(self.outside_files) > 0) 

    def __check_link(self, filename):
        # add, above, makes sure filename is always relative
        if os.path.islink(filename):
           return filename
        directory = os.path.dirname(filename)

        while (len(directory) > 0):
            # stop at the project directory, if it is in the path
            if directory == self.project_dir:
                break
            # stop at root, as a safety check though it should not happen
            if directory == os.sep:
                break
            if os.path.islink(directory):
                return directory
            directory = os.path.dirname(directory)
        return None

    def __make_rel(self, filepath):
        return self.__drop_prefix(self.project_dir, filepath)

    def __drop_prefix(self, prefix, filepath):
        if not filepath.startswith(prefix):
            return filepath

        if not prefix.endswith(os.sep):
            prefix += os.sep
        if sys.hexversion < 0x2060000:
            return filepath.replace(prefix, "")
        else:
            return os.path.relpath(filepath, prefix)
