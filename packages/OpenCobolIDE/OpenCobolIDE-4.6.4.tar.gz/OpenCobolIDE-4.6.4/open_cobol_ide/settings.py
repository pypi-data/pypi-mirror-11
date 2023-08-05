"""
This module contains a class for accessing the application settings.
"""
import json
import os
import sys
from pyqode.qt import QtCore
from pyqode.qt.QtCore import QSettings
from open_cobol_ide import system
from open_cobol_ide.enums import FileType, GnuCobolStandard


class Settings(object):
    """
    Wraps QSettings to give an intuitive and easy access to the application
    settings (thought getter/setter properties).
    """
    def __init__(self):
        self._settings = QSettings('OpenCobolIDE', 'OpenCobolIDE4')

    def clear(self):
        """
        Clear the settings.
        """
        self._settings.clear()

    # Geometry and state (visible windows, ...) + working settings (last path)
    # ------------------------------------------------------------------------
    @property
    def geometry(self):
        v = self._settings.value('mainWindowGeometry')
        if v:
            return bytes(v)
        return None

    @geometry.setter
    def geometry(self, geometry):
        self._settings.setValue('mainWindowGeometry', geometry)

    @property
    def state(self):
        v = self._settings.value('mainWindowState')
        if v:
            return bytes(v)
        return None

    @state.setter
    def state(self, state):
        self._settings.setValue('mainWindowState', state)

    @property
    def preferences_width(self):
        v = int(self._settings.value('preferences_width', '800'))
        return v

    @preferences_width.setter
    def preferences_width(self, width):
        self._settings.setValue('preferences_width', int(width))

    @property
    def preferences_height(self):
        v = int(self._settings.value('preferences_height', '400'))
        return v

    @preferences_height.setter
    def preferences_height(self, height):
        self._settings.setValue('preferences_height', int(height))

    @property
    def maximised(self):
        return bool(int(self._settings.value('maximised', '0')))

    @maximised.setter
    def maximised(self, value):
        self._settings.setValue('maximised', int(value))

    @property
    def fullscreen(self):
        return bool(int(self._settings.value('fullscreen', '0')))

    @fullscreen.setter
    def fullscreen(self, value):
        self._settings.setValue('fullscreen', int(value))

    @property
    def size(self):
        return self._settings.value('size', QtCore.QSize(1200, 800))

    @size.setter
    def size(self, value):
        self._settings.setValue('size', value)

    @property
    def outline_visible(self):
        return bool(int(self._settings.value('navigationPanelVisible', '1')))

    @outline_visible.setter
    def outline_visible(self, value):
        self._settings.setValue('navigationPanelVisible', int(value))

    @property
    def last_path(self):
        """
        Returns the last used open/save path
        """
        default_value = ''
        if sys.platform == 'win32':
            default_value = 'c:\\'
        return self._settings.value('lastUsedPath', default_value)

    @last_path.setter
    def last_path(self, path):
        """
        Sets the last used path (save or open path):

        :param path: path string
        :type path: str or unicode
        """
        self._settings.setValue('lastUsedPath', os.path.dirname(path))

    @property
    def perspective(self):
        return self._settings.value(
            'perspective', 'default')

    @perspective.setter
    def perspective(self, value):
        self._settings.setValue('perspective', value)

    @property
    def verbose(self):
        return bool(int(self._settings.value('verbose', '0')))

    @verbose.setter
    def verbose(self, value):
        self._settings.setValue('verbose', int(value))

    #
    # Editor settings settings
    #
    @property
    def preferred_eol(self):
        return int(self._settings.value('preferredEOL', 0))

    @preferred_eol.setter
    def preferred_eol(self, value):
        self._settings.setValue('preferredEOL', int(value))

    @property
    def autodetect_eol(self):
        return bool(self._settings.value('autodetectEOL', True))

    @autodetect_eol.setter
    def autodetect_eol(self, value):
        self._settings.setValue('autodetectEOL', bool(value))

    @property
    def display_lines(self):
        return bool(int(self._settings.value('displayLineNumbers', '1')))

    @display_lines.setter
    def display_lines(self, value):
        self._settings.setValue('displayLineNumbers', int(value))

    @property
    def highlight_caret(self):
        return bool(int(self._settings.value('highlightCurrentLine', '1')))

    @highlight_caret.setter
    def highlight_caret(self, value):
        self._settings.setValue('highlightCurrentLine', int(value))

    @property
    def show_whitespaces(self):
        return bool(int(self._settings.value('highlightWhitespaces', '0')))

    @show_whitespaces.setter
    def show_whitespaces(self, value):
        self._settings.setValue('highlightWhitespaces', int(value))

    @property
    def tab_len(self):
        return int(self._settings.value('tabWidth', '4'))

    @tab_len.setter
    def tab_len(self, value):
        self._settings.setValue('tabWidth', int(value))

    @property
    def enable_autoindent(self):
        return bool(int(self._settings.value('enableAutoIndent', '1')))

    @enable_autoindent.setter
    def enable_autoindent(self, value):
        self._settings.setValue('enableAutoIndent', int(value))

    @property
    def completion_filter_mode(self):
        ret_val = int(self._settings.value('codeCompletionFilterMode', 1))
        return ret_val

    @completion_filter_mode.setter
    def completion_filter_mode(self, value):
        self._settings.setValue('codeCompletionFilterMode', int(value))

    @property
    def code_completion_trigger_len(self):
        return int(self._settings.value('ccTriggerLen', '1'))

    @code_completion_trigger_len.setter
    def code_completion_trigger_len(self, value):
        self._settings.setValue('ccTriggerLen', value)

    @property
    def show_errors(self):
        return bool(int(self._settings.value('showErrors', '1')))

    @show_errors.setter
    def show_errors(self, value):
        self._settings.setValue('showErrors', int(value))

    @property
    def enable_smart_backspace(self):
        return bool(int(self._settings.value('enable_smart_backspace', '0')))

    @enable_smart_backspace.setter
    def enable_smart_backspace(self, value):
        self._settings.setValue('enable_smart_backspace', int(value))

    #
    # Editor style settings
    #
    @property
    def dark_style(self):
        return bool(int(self._settings.value('dark_style', '0')))

    @dark_style.setter
    def dark_style(self, value):
        self._settings.setValue('dark_style', int(value))

    @property
    def icon_theme(self):
        return self._settings.value('icon_theme', 'default')

    @icon_theme.setter
    def icon_theme(self, value):
        self._settings.setValue('icon_theme', value)

    @property
    def font(self):
        font = self._settings.value('fontName')
        if not font:
            font = 'Source Code Pro'
        return font

    @font.setter
    def font(self, font):
        self._settings.setValue('fontName', font)

    @property
    def font_size(self):
        return int(self._settings.value('fontSize', '11'))

    @font_size.setter
    def font_size(self, value):
        self._settings.setValue('fontSize', value)

    @property
    def color_scheme(self):
        return self._settings.value('colorScheme', 'qt')

    @color_scheme.setter
    def color_scheme(self, value):
        self._settings.setValue('colorScheme', value)

    # Run settings
    # ----------------------
    @property
    def external_terminal(self):
        return bool(int(self._settings.value('runInShell', '0')))

    @external_terminal.setter
    def external_terminal(self, value):
        self._settings.setValue('runInShell', int(value))

    @property
    def external_terminal_command(self):
        # works on gnome, what about KDE and how do I detect that?
        # at the moment just go with gnome, user can change that in the
        # settings dialog anyway
        def get_terminal():
            """
            Gets the authentication program used to run command as root (
            on linux only).

            The function try to use one of the following programs:
                - gksu
                - kdesu

            """
            for program in ['gnome-terminal', 'xfce4-terminal', 'konsole']:
                if system.which(program) is not None:
                    return program
            return 'gnome-terminal'
        default_shell_cmd = ('%s -e' % get_terminal() if not system.darwin else
                             'open')
        return str(self._settings.value('shell', default_shell_cmd))

    @external_terminal_command.setter
    def external_terminal_command(self, cmd):
        self._settings.setValue('shell', cmd)

    # Compiler settings
    # ----------------------
    @property
    def autodetect_submodules(self):
        return bool(int(self._settings.value('autoDetectSubmodules', 1)))

    @autodetect_submodules.setter
    def autodetect_submodules(self, value):
        self._settings.setValue('autoDetectSubmodules', int(value))

    @property
    def output_directory(self):
        return self._settings.value('outputDirectory', 'bin')

    @output_directory.setter
    def output_directory(self, value):
        self._settings.setValue('outputDirectory', value)

    @staticmethod
    def default_compiler_path():
        if system.windows:
            # get the bundled compiler path as default
            # compiler on windows
            if getattr(sys, 'frozen', False):
                # The application is frozen
                cwd = os.path.dirname(sys.executable)
                default = os.path.join(cwd, 'GnuCOBOL', 'bin', 'cobc.exe')
            else:
                cwd = os.getcwd()
                default = os.path.join(cwd, 'GnuCOBOL-Win32-MinGW', 'bin',
                                       'cobc.exe')
        else:
            default = system.which('cobc')
        return default

    @property
    def compiler_path(self):
        default = self.default_compiler_path()
        path = self._settings.value('compilerPath', default)
        if not path or not os.path.exists(path) or not os.path.isfile(path):
            path = default
            self.compiler_path = path
        return path

    @compiler_path.setter
    def compiler_path(self, value):
        # add to PATH
        if value:
            sep = ';' if sys.platform == 'win32' else ':'
            os.environ['PATH'] += sep + os.path.dirname(value)
        self._settings.setValue('compilerPath', value)

    @property
    def vcvars32(self):
        return self._settings.value('vcvars32', '')

    @vcvars32.setter
    def vcvars32(self, value):
        self._settings.setValue('vcvars32', value)

    @property
    def compiler_flags(self):
        lst = eval(self._settings.value('compilerFlags', '["-debug"]'))
        ret_val = []
        for v in lst:
            if v:
                ret_val.append(v.replace('&', ''))
        return ret_val

    @compiler_flags.setter
    def compiler_flags(self, value):
        self._settings.setValue('compilerFlags', repr(value))

    @property
    def copybook_paths(self):
        return self._settings.value('copybook_paths', '')

    @copybook_paths.setter
    def copybook_paths(self, value):
        self._settings.setValue('copybook_paths', value)

    @property
    def library_search_path(self):
        return self._settings.value('library_search_path', '')

    @library_search_path.setter
    def library_search_path(self, value):
        self._settings.setValue('library_search_path', value)

    @property
    def libraries(self):
        return self._settings.value('libraries', '')

    @libraries.setter
    def libraries(self, value):
        self._settings.setValue('libraries', value)

    @property
    def cobc_extensions(self):
        values = eval(self._settings.value('cobcExtensions',
                      "['.cob', '.cbl', '.pco', '.cpy', '.lst']"))
        return [v.lower() for v in values]

    @cobc_extensions.setter
    def cobc_extensions(self, exts):
        exts = list(set([ext.lower() for ext in exts]))
        self._settings.setValue('cobcExtensions', repr(exts))

    # Cobol settings
    # ----------------------
    @property
    def free_format(self):
        return bool(int(self._settings.value('free_format', '0')))

    @free_format.setter
    def free_format(self, value):
        self._settings.setValue('free_format', int(value))

    @property
    def lower_case_keywords(self):
        return bool(int(self._settings.value('lower_case_keywords', '0')))

    @lower_case_keywords.setter
    def lower_case_keywords(self, value):
        self._settings.setValue('lower_case_keywords', int(value))

    @property
    def comment_indicator(self):
        return self._settings.value('comment_indicator', '*> ')

    @comment_indicator.setter
    def comment_indicator(self, value):
        self._settings.setValue('comment_indicator', value)

    @property
    def cobol_standard(self):
        return GnuCobolStandard(int(self._settings.value(
            'cobc_standard', '0')))

    @cobol_standard.setter
    def cobol_standard(self, value):
        self._settings.setValue('cobc_standard', int(value))

    # Cache
    def get_file_type(self, file_path):
        """
        Gets file type from cache.

        Raises a KeyError if no file type were cached for the specified file
        path.

        :param file_path: path of the file to look up
        :returns: The cached file type.

        """
        try:
            map = json.loads(self._settings.value('cached_file_types'))
        except TypeError:
            map = {}
        return FileType(map[file_path])

    def set_file_type(self, path, ftype):
        """
        Cache the file type of the specified file.

        :param path: path of the file to cache
        :param ftype: file type to cache
        """
        try:
            map = json.loads(self._settings.value('cached_file_types'))
        except TypeError:
            map = {}
        map[path] = int(ftype)
        self._settings.setValue('cached_file_types', json.dumps(map))

    @property
    def lock_fs_path(self):
        return str(self._settings.value('lock_fs_path', ''))

    @lock_fs_path.setter
    def lock_fs_path(self, value):
        self._settings.setValue('lock_fs_path', str(value))

    # SQL Cobol Settings
    # ----------------------
    @property
    def esqloc(self):
        return self._settings.value('esqloc', '')

    @esqloc.setter
    def esqloc(self, value):
        self._settings.setValue('esqloc', value)

    @property
    def esqloc_extensions(self):
        values = eval(self._settings.value('esqlOcExtensions', "['.sqb']"))
        return [v.lower() for v in values]

    @esqloc_extensions.setter
    def esqloc_extensions(self, exts):
        exts = list(set([v.lower() for v in exts]))
        self._settings.setValue('esqlOcExtensions', repr(exts))

    @property
    def dbpre_extensions(self):
        values = eval(self._settings.value('dbpreExtensions', "['.scb']"))
        return [v.lower() for v in values]

    @dbpre_extensions.setter
    def dbpre_extensions(self, exts):
        exts = list(set([v.lower() for v in exts]))
        self._settings.setValue('dbpreExtensions', repr(exts))

    @property
    def dbpre(self):
        return self._settings.value('dbpre', '')

    @dbpre.setter
    def dbpre(self, path):
        self._settings.setValue('dbpre', path)

    @property
    def cobmysqlapi(self):
        return self._settings.value('cobmysqlapi', '')

    @cobmysqlapi.setter
    def cobmysqlapi(self, path):
        self._settings.setValue('cobmysqlapi', path)

    @property
    def dbpre_framework(self):
        return self._settings.value('dbpre_framework', '')

    @dbpre_framework.setter
    def dbpre_framework(self, path):
        self._settings.setValue('dbpre_framework', path)

    @property
    def dbhost(self):
        return self._settings.value('dbhost', 'localhost')

    @dbhost.setter
    def dbhost(self, value):
        self._settings.setValue('dbhost', value)

    @property
    def dbuser(self):
        return self._settings.value('dbuser', '')

    @dbuser.setter
    def dbuser(self, value):
        self._settings.setValue('dbuser', value)

    @property
    def dbpasswd(self):
        return self._settings.value('dbpasswd', '')

    @dbpasswd.setter
    def dbpasswd(self, value):
        self._settings.setValue('dbpasswd', value)

    @property
    def dbname(self):
        return self._settings.value('dbname', '')

    @dbname.setter
    def dbname(self, value):
        self._settings.setValue('dbname', value)

    @property
    def dbport(self):
        return self._settings.value('dbport', '03306')

    @dbport.setter
    def dbport(self, value):
        self._settings.setValue('dbport', value)

    @property
    def dbsocket(self):
        return self._settings.value('dbsocket', 'null')

    @dbsocket.setter
    def dbsocket(self, value):
        self._settings.setValue('dbsocket', value)

    @property
    def all_extensions(self):
        return self.cobc_extensions + self.esqloc_extensions + \
            self.dbpre_extensions

    # environment variables
    def default_path(self):
        path = os.pathsep.join([os.path.dirname(self.default_compiler_path())])
        return path

    # ------------
    # PATH
    # ------------
    @property
    def path(self):
        pth = self._settings.value('environment/PATH', self.default_path())
        paths = []
        for p in pth.split(os.pathsep):
            if os.path.exists(p):
                paths.append(p)
        paths = list(set(paths))
        if not paths:
            paths = [self.default_path()]
        retval = os.pathsep.join(paths)
        return retval

    @path.setter
    def path(self, value):
        self._settings.setValue('environment/PATH', value)

    @property
    def path_enabled(self):
        return bool(int(self._settings.value(
            'environment/PATH_Enabled', 1 if system.windows else 0)))

    @path_enabled.setter
    def path_enabled(self, value):
        self._settings.setValue('environment/PATH_Enabled', int(value))

    # -----------------
    # COB_CONFIG_DIR
    # -----------------
    def default_config_dir(self):
        root = os.path.abspath(os.path.join(
            os.path.dirname(self.compiler_path), '..'))
        default = os.path.join(root, 'config')
        return default

    @property
    def cob_config_dir(self):
        default = self.default_config_dir()
        value = self._settings.value('environment/COB_CONFIG_DIR', default)
        if not os.path.exists(value):
            value = default
        return value

    @cob_config_dir.setter
    def cob_config_dir(self, value):
        self._settings.setValue('environment/COB_CONFIG_DIR', value)

    @property
    def cob_config_dir_enabled(self):
        return bool(int(
            self._settings.value('environment/COB_CONFIG_DIR_Enabled',
                                 True if system.windows else False)))

    @cob_config_dir_enabled.setter
    def cob_config_dir_enabled(self, value):
        value = self._settings.setValue(
            'environment/COB_CONFIG_DIR_Enabled', int(value))

    # -----------------
    # COB_COPY_DIR
    # -----------------
    def default_copy_dir(self):
        root = os.path.abspath(os.path.join(
            os.path.dirname(self.compiler_path), '..'))
        default = os.path.join(root, 'copy')
        return default

    @property
    def cob_copy_dir(self):
        default = self.default_copy_dir()
        value = self._settings.value('environment/COB_COPY_DIR', default)
        if not os.path.exists(value):
            value = default
        return value

    @cob_copy_dir.setter
    def cob_copy_dir(self, value):
        self._settings.setValue('environment/COB_COPY_DIR', value)

    @property
    def cob_copy_dir_enabled(self):
        return bool(int(self._settings.value(
            'environment/COB_COPY_DIR_Enabled',
            True if system.windows else False)))

    @cob_copy_dir_enabled.setter
    def cob_copy_dir_enabled(self, value):
        self._settings.setValue('environment/COB_COPY_DIR_Enabled', int(value))

    # -----------------
    # COB_INCLUDE_PATH
    # -----------------
    def default_include_dir(self):
        root = os.path.abspath(os.path.join(
            os.path.dirname(self.compiler_path), '..'))
        default = os.path.join(root, 'include')
        return default

    @property
    def cob_include_path(self):
        default = self.default_include_dir()
        value = self._settings.value('environment/COB_INCLUDE_PATH', default)
        if not os.path.exists(value):
            value = default
        return value

    @cob_include_path.setter
    def cob_include_path(self, value):
        self._settings.setValue('environment/COB_INCLUDE_PATH', value)

    @property
    def cob_include_path_enabled(self):
        return bool(int(self._settings.value(
            'environment/COB_INCLUDE_PATH_Enabled',
            True if system.windows else False)))

    @cob_include_path_enabled.setter
    def cob_include_path_enabled(self, value):
        self._settings.setValue('environment/COB_INCLUDE_PATH_Enabled',
                                int(value))

    # -----------------
    # COB_LIB_PATH
    # -----------------
    def default_lib_path(self):
        root = os.path.abspath(os.path.join(
            os.path.dirname(self.compiler_path), '..'))
        default = os.path.join(root, 'lib')
        return default

    @property
    def cob_lib_path(self):
        default = self.default_lib_path()
        value = self._settings.value('environment/COB_LIB_PATH', default)
        if not os.path.exists(value):
            value = default
        return value

    @cob_lib_path.setter
    def cob_lib_path(self, value):
        self._settings.setValue('environment/COB_LIB_PATH', value)

    @property
    def cob_lib_path_enabled(self):
        return bool(int(self._settings.value(
            'environment/COB_LIB_PATH_Enabled',
            True if system.windows else False)))

    @cob_lib_path_enabled.setter
    def cob_lib_path_enabled(self, value):
        self._settings.setValue('environment/COB_LIB_PATH_Enabled', int(value))


if __name__ == '__main__':
    # Settings()._settings.setValue('resetCompilerPath', 1)
    Settings().clear()
