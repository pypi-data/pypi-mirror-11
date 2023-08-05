"""
This module contains function and classes for interfacing with the GnuCobol
compiler.
"""
import glob
import locale
import logging
import os
import re
import subprocess
import sys
import shutil
import tempfile

from pyqode.cobol.widgets import CobolCodeEdit
from pyqode.core.cache import Cache
from pyqode.core.modes import CheckerMessages
from pyqode.qt import QtCore

from open_cobol_ide import system
from open_cobol_ide.enums import FileType
from open_cobol_ide.memoize import memoized
from open_cobol_ide.settings import Settings


def _logger():
    return logging.getLogger(__name__)


def _get_encoding(filename):
    """
    Gets a filename encoding from the pyqode.core cache. If the requested file
    path could not be found in cache, the locale preferred encoding is used.

    :param filename: path of the file in cache.
    :return: cached encoding
    """
    try:
        encoding = Cache().get_file_encoding(filename)
    except KeyError:
        encoding = locale.getpreferredencoding()
        _logger().warning(
            'encoding for %s not found in cache, using locale preferred '
            'encoding instead: %s', filename, encoding)
    return encoding


def get_file_type(path):
    """
    Detects file type. If the file contains 'PROCEDURE DIVISION USING', then it
    is considered as a module else it is considered as an executable.

    :param path: file path
    :return: FileType
    """
    encoding = _get_encoding(path)
    _logger().debug('detecting file type: %s - %s', path, encoding)
    try:
        from .settings import Settings
        ftype = Settings().get_file_type(path)
    except KeyError:
        ftype = FileType.EXECUTABLE
        with open(path, 'r', encoding=encoding) as f:
            content = f.read().upper()
        if re.match(r'.*PROCEDURE[\s\n]+DIVISION[\s\n]+USING', content, re.DOTALL):
            ftype = FileType.MODULE
    _logger().debug('file type: %r', ftype)
    return ftype


def check_compiler():
    """
    Checks if a valid cobol compiler can be found.

    :raises: CompilerNotFound if no compiler could be found.
    """
    import sys
    if not GnuCobolCompiler().is_working():
        if sys.platform == 'win32':
            msg = 'GnuCOBOL is bundled with the IDE. Ensure that ' \
                  'the IDE is installed in a path without spaces and ' \
                  'that the GnuCOBOL folder sits next to the executable.'
        elif sys.platform == 'darwin':
            msg = 'You have to install the package open-cobol using Homebrew '\
                  'or MacPorts. \n' \
                  'If you installed open-cobol in a ' \
                  'non standard directory, you can specify that directory ' \
                  'in the preferences dialog (build & run tab).'
        else:
            msg = 'You have to install the package open-cobol using your ' \
                  "distribution's package manager"
        raise CompilerNotFound(msg)


class CompilerNotFound(Exception):
    """
    Error raised when no compiler were found.
    """
    pass


class VisualStudioWrapperBatch:
    """
    Helps creating a wrapper batch that setup visual studio command line
    environment before running the cobc command, this is needed to use the
    kiska builds on Windows.
    """
    CODE_TEMPLATE = r"""@echo off
call "{0}\vcvars32.bat"
@echo on
call {1} %*
"""
    FILENAME = 'cobc_wrapper.bat'

    @classmethod
    def path(cls):
        return os.path.join(tempfile.gettempdir(), cls.FILENAME)

    @classmethod
    def generate(cls):
        print(cls.path())
        with open(cls.path(), 'w') as f:
            f.write(cls.CODE_TEMPLATE.format(
                os.path.dirname(Settings().vcvars32),
                Settings().compiler_path))


class GnuCobolCompiler(QtCore.QObject):
    """
    Provides an interface to the GnuCobol compiler (cobc)
    """
    #: signal emitted when the compilation process started, parameter
    #: is the command
    started = QtCore.Signal(str)

    #: signal emitted when the compilation process finished and its output
    #: is available for parsing.
    output_available = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        #: platform specifc extensions, sorted per file type
        self.extensions = [
            # no extension for exe on linux and mac
            '.exe' if system.windows else '',
            # dll on windows, so everywhere else
            '.dll' if system.windows else '.so'
        ]

    @staticmethod
    def get_version():
        """
        Returns the GnuCOBOL compiler version as a string
        """
        cmd = [Settings().compiler_path, '--version']
        try:
            _logger().debug('getting cobc version: %s' % ' '.join(cmd))
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                p = subprocess.Popen(
                    cmd, shell=False, startupinfo=startupinfo,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE)
            else:
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        except (OSError, TypeError):
            _logger().exception('GnuCOBOL compiler not found (command: %s)' %
                                cmd)
            return 'Not installed'
        else:
            stdout, stderr = p.communicate()
            try:
                stdout = str(stdout.decode(locale.getpreferredencoding()))
            except UnicodeDecodeError:
                stdout = None
                lversion = 'Failed to parse cobc output'
            else:
                lversion = stdout.splitlines()[0]
                lversion = lversion.replace('cobc (', '').replace(')', '')
                _logger().debug('parsing version line: %s' % lversion)
            return lversion

    @classmethod
    @memoized
    def check_compiler(cls, compiler):
        if Settings().vcvars32:
            try:
                VisualStudioWrapperBatch.generate()
            except OSError as e:
                _logger().exception('failed to generate visual studio wrapper '
                                    'batch')
                return str(e), 1
            compiler = VisualStudioWrapperBatch.path()

        from open_cobol_ide.view.dialogs.preferences import DEFAULT_TEMPLATE
        cbl_path = os.path.join(tempfile.gettempdir(), 'test.cbl')
        with open(cbl_path, 'w') as f:
            f.write(DEFAULT_TEMPLATE)
        dest = os.path.join(tempfile.gettempdir(),
                            'test' + ('.exe' if system.windows else ''))
        p = QtCore.QProcess()
        args = ['-x', '-o', dest, cbl_path]
        p.start(compiler, args)
        _logger().debug('check compiler')
        _logger().debug('process environment: %r',
                        p.processEnvironment().toStringList())
        _logger().debug('command: %s %s', compiler, ' '.join(args))
        p.waitForFinished()
        try:
            stdout = bytes(p.readAllStandardOutput()).decode(
                locale.getpreferredencoding())
            stderr = bytes(p.readAllStandardError()).decode(
                locale.getpreferredencoding())
        except UnicodeDecodeError:
            # something is wrong in the output, the compiler might be broker
            output = None
        else:
            output = stderr + stdout
        if p.exitStatus() == p.Crashed or output is None:
            exit_code = 139
        else:
            exit_code = p.exitCode()
        _logger().debug('process output: %r', output)
        _logger().debug('process exit code: %r', exit_code)
        _logger().info('GnuCOBOL compiler check: %s',
                       'success' if exit_code == 0 else 'fail')
        try:
            os.remove(dest)
            os.remove(cbl_path)
        except OSError:
            pass
        return output, p.exitCode()

    def is_working(self):
        """
        Checks if the GNUCobol compiler is working.
        """
        pth = Settings().compiler_path
        if pth:
            _, exit_code = self.check_compiler(pth)
            return exit_code == 0
        return False

    def extension_for_type(self, file_type):
        """
        Returns a platform specific extension for the specified file type.

        :param file_type: file type
        :return: extension
        """
        return self.extensions[int(file_type)]

    def prepare_bin_dir(self, path, output_full_path):
        assert not os.path.isfile(path)  # must be a directory
        if not os.path.exists(path):
            os.makedirs(path)
        if sys.platform == "win32":
            # copy the dll
            files = glob.glob(os.path.join(
                Settings().compiler_path, "*.dll"))
            for f in files:
                shutil.copy(f, path)
        if os.path.exists(output_full_path):
            try:
                os.remove(output_full_path)
            except OSError:
                _logger().exception(
                    'Failed to previous binary file: %s' % output_full_path)

    def compile(self, file_path, file_type, object_files=None,
                additional_options=None, output_dir=None):
        """
        Compiles a file. This is a blocking function, it returns only when
        the compiler process finished.

        :param file_path: Path of the file to compile.
        :param file_type: File type (exe or dll)
        :param output_dir: Output directory, if None, the directory set in the
                           application directory will be used.
        :return: status, list of checker messages
        """
        _logger().info('compiling %s' % file_path)
        path, filename = os.path.split(file_path)
        if output_dir is None:
            output_dir = Settings().output_directory
        if not os.path.isabs(output_dir):
            output_dir = os.path.abspath(os.path.join(path, output_dir))
        # run command using qt process api, this is blocking.
        if object_files:
            inputs = [filename] + object_files
        else:
            inputs = [filename]
        # ensure bin dir exists
        output_full_path = os.path.join(
            output_dir, self._get_output_filename(inputs, file_type))
        if os.path.exists(output_full_path) and \
            os.path.getmtime(file_path) <= \
                os.path.getmtime(output_full_path):
            desc = 'compilation skipped, up to date...'
            self.output_available.emit('%s: %s' % (file_path, desc))
            msg = (desc, CheckerMessages.INFO, -1, 0, None, None, file_path)
            return 0, [msg]

        self.prepare_bin_dir(output_dir, output_full_path)
        pgm, options = self.make_command(inputs, file_type, output_dir,
                                         additional_options)
        process = QtCore.QProcess()
        process.setWorkingDirectory(path)
        process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        cmd = '%s %s' % (pgm, ' '.join(options))
        _logger().info('command: %s', cmd)
        _logger().debug('working directory: %s', path)
        _logger().debug('system environment: %s', process.systemEnvironment())
        process.start(pgm, options)
        self.started.emit(cmd)
        process.waitForFinished()
        if process.exitStatus() != process.Crashed:
            status = process.exitCode()
        else:
            status = 139
        try:
            output = process.readAllStandardOutput().data().decode(
                locale.getpreferredencoding())
        except UnicodeDecodeError:
            output = 'Failed to decode compiler output with encoding %s' % \
                     locale.getpreferredencoding()
        self.output_available.emit(output)
        messages = self.parse_output(output, file_path)
        binary_created = os.path.exists(output_full_path)
        _logger().info('compiler process exit code: %d', status)
        _logger().info('compiler process output: %s', output)
        _logger().info('binary file (%s) created:  %r',
                       output_full_path, binary_created)
        if status != 0 or not binary_created:
            # compilation failed but the parser failed to extract cobol related
            # messages, there might be an issue at the C level or at the
            # linker level
            messages.append((output, CheckerMessages.ERROR, - 1, 0,
                             None, None, file_path))
        _logger().debug('compile results: %r - %r', status, messages)
        return status, messages

    def _get_output_filename(self, inputs, file_type):
        return os.path.splitext(inputs[0])[0] + self.extension_for_type(
            file_type)

    def make_command(self, input_file_names, file_type, output_dir=None,
                     additional_options=None):
        """
        Makes the command needed to compile the specified file.

        :param input_file_names: Input file names (without path).
            The first name must be the source file, other entries can
            be used to link with additional object files.
        :param output_file_name: Output file base name (without path and
            extension). None to use the input_file_name base name.
        :param file_type: file type (exe or dll).

        :return: a tuple made up of the program name and the command arguments.
        """
        from .settings import Settings
        settings = Settings()
        output_file_name = self._get_output_filename(
            input_file_names, file_type)
        options = []
        if file_type == FileType.EXECUTABLE:
            options.append('-x')
        options.append('-o')
        options.append(os.path.join(output_dir, output_file_name))
        options.append('-std=%s' % str(settings.cobol_standard).replace(
            'GnuCobolStandard.', ''))
        options += settings.compiler_flags
        if settings.free_format:
            options.append('-free')
        if settings.copybook_paths:
            for pth in settings.copybook_paths.split(';'):
                if not pth:
                    continue
                options.append('-I%s' % pth)
        if settings.library_search_path:
            for pth in settings.library_search_path.split(';'):
                if pth:
                    options.append('-L%s' % pth)
        if settings.libraries:
            for lib in settings.libraries.split(' '):
                if lib:
                    options.append('-l%s' % lib)
        if additional_options:
            options += additional_options
        for ifn in input_file_names:
            if system.windows and ' ' in ifn:
                ifn = '"%s"' % ifn
            options.append(ifn)
        if Settings().compiler_path and Settings().vcvars32:
            VisualStudioWrapperBatch.generate()
            pgm = VisualStudioWrapperBatch.path()
        else:
            pgm = Settings().compiler_path
        return pgm, options

    @staticmethod
    def parse_output(compiler_output, file_path):
        """
        Parses the compiler output

        :param compiler_output: compiler output
        :param filename: input filename
        :return: list of tuples. Each tuple are made up of the arguments needed
            to create a :class:`pyqode.core.modes.CheckerMessage`.

        """
        _logger().debug('parsing cobc output: %s' % compiler_output)
        retval = []
        exp = r'%s: *\d*:.*:.*$' % os.path.split(file_path)[1]
        prog = re.compile(exp)
        # parse compilation results
        for l in compiler_output.splitlines():
            if prog.match(l):
                _logger().debug('MATCHED')
                status = CheckerMessages.WARNING
                tokens = l.split(':')
                line = tokens[1]
                error_type = tokens[2]
                desc = ''.join(tokens[3:])
                if 'error' in error_type.lower():
                    status = CheckerMessages.ERROR
                # there does not seems to be any 'warning' messages output
                # if 'warning' in error_type.lower():
                #     status = CheckerMessages.WARNING
                msg = (desc.strip(), status, int(line) - 1, 0,
                       None, None, file_path)
                _logger().debug('message: %r', msg)
                retval.append(msg)
        return retval

    @classmethod
    def get_dependencies(cls, filename, recursive=True):
        """
        Gets the dependencies of a cobol program/module.

        :param filename: path of the file to analyse.
        :param recursive: True to perform recursive analysis (analyses
            dependencies of dependencies recursively).
        :return: The set of dependencies that needs to be compiled to compile
            and use the requested program/module.
        """
        encoding = _get_encoding(filename)
        directory = os.path.dirname(filename)
        dependencies = []
        prog = re.compile(r'(^(\s|\d|\w)*CALL[\s\n]*.*".*")',
                          re.MULTILINE | re.IGNORECASE)
        with open(filename, 'r', encoding=encoding) as f:
            content = f.read()
            if not Settings().free_format:
                content = '\n'.join([' ' * 6 + l[6:] for l in content.splitlines()])
            for m in prog.findall(content):
                for m in m:
                    try:
                        module_base_name = re.findall('"(.*)"', m)[0]
                    except IndexError:
                        continue
                    # try to see if the module can be found in the current
                    # directory
                    for ext in Settings().all_extensions:
                        pth = os.path.join(directory, module_base_name + ext)
                        if os.path.exists(pth) and \
                                pth.lower() not in dependencies:
                            if filename != pth:
                                dependencies.append(os.path.normpath(pth))
                                if recursive:
                                    dependencies += cls.get_dependencies(pth)

        dependencies = list(set(dependencies))
        _logger().debug('dependencies of %s: %r', filename, dependencies)
        return dependencies


PARAM_FILE_CONTENT = '''DBHOST=%(host)s
DBUSER=%(user)s
DBPASSWD=%(pswd)s
DBNAME=%(dbname)s
DBPORT=%(port)s
DBSOCKET=%(socket)s
'''


class DbpreCompiler(QtCore.QObject):
    """
    Provides an interface to the Dbpre tool.

    Commands:
        - /path/to/dbpre SOURCE.scb -I/path/to/framework -ts=TAB_LEN
        - copy PGCTBBATWS to source dir
        - cobc -x SOURCE.cob /path/to/cobmysqlapi.o -L/usr/lib/mysql
          -lmysqlclient -o bin/SOURCE.exe

    (-L: library search path, -l libraries to link with)
    """
    #: signal emitted when the compilation process started, parameter
    #: is the command
    started = QtCore.Signal(str)

    #: signal emitted when the compilation process finished and its output
    #: is available for parsing.
    output_available = QtCore.Signal(str)

    _INVALID = 'invalid dbpre executable'

    def __init__(self, dbpre_path=None):
        super().__init__()
        if dbpre_path is None:
            dbpre_path = Settings().dbpre
        self.dbpre_path = dbpre_path

    def get_version(self, path=None):
        """
        Returns the GnuCobol compiler version as a string
        """
        program = self.dbpre_path
        cmd = [program, '--version']
        try:
            _logger().debug('getting dbpre version: %s' % ' '.join(cmd))
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                p = subprocess.Popen(
                    cmd, shell=False, startupinfo=startupinfo,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE)
            else:
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        except OSError:
            pass
        else:
            stdout, stderr = p.communicate()
            stdout = stdout.decode()
            lversion = stdout.splitlines()[0]
            if re.match(r'dbpre V \d.\d.+', lversion):
                return lversion
        return self._INVALID

    def is_working(self):
        """

        :return:
        """
        return self.get_version() != self._INVALID

    def make_command(self, file_path):
        """
        Make the dbpre command.

        :param file_path: .scb path
        """
        source = os.path.splitext(os.path.split(file_path)[1])[0]
        return self.dbpre_path, [source, '-I%s' % Settings().dbpre_framework,
                                 '-ts=%d' % Settings().tab_len]

    def _run_dbpre(self, file_path):
        """
        Run the dbpre process and returns it's exit code and
        output (both stderr and stdout).

        :param file_path: .scb path.
        :return: int, str
        """
        path = os.path.dirname(file_path)
        pgm, options = self.make_command(file_path)
        process = QtCore.QProcess()
        process.setWorkingDirectory(path)
        process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        cmd = '%s %s' % (pgm, ' '.join(options))
        _logger().info('command: %s', cmd)
        _logger().debug('working directory: %s', path)
        _logger().debug('system environment: %s', process.systemEnvironment())
        process.start(pgm, options)
        self.started.emit(cmd)
        process.waitForFinished()
        status = process.exitCode()
        try:
            output = process.readAllStandardOutput().data().decode(
                locale.getpreferredencoding())
        except UnicodeDecodeError:
            output = 'Failed to decode dbpre output with encoding: %s' % \
                locale.getpreferredencoding()
        self.output_available.emit(output)
        return output, status

    def _copy_dbpre_framework(self, path):
        """
        Copies the dbpre framework files to the source directory.

        :param path: path of the .scb file
        """
        _logger().info('copying dbpre framework to source directory')
        pgctbbat = os.path.join(Settings().dbpre_framework, 'PGCTBBAT')
        pgctbbatws = os.path.join(Settings().dbpre_framework, 'PGCTBBATWS')
        sqlca = os.path.join(Settings().dbpre_framework, 'SQLCA')
        results = os.listdir(os.path.dirname(path))
        if 'PGCTBBAT' not in results:
            _logger().info('copying PGCTBBAT')
            shutil.copy(pgctbbat, os.path.dirname(path))
        if 'PGCTBBATWS' not in results:
            _logger().info('copying PGCTBBATWS')
            shutil.copy(pgctbbatws, os.path.dirname(path))
        if 'SQLCA' not in results:
            _logger().info('copying QSLCA')
            shutil.copy(sqlca, os.path.dirname(path))

    def _compile_with_cobc(self, path):
        """
        Compile the .cob generated by dbpre.

        :param path: path of the .scb file.

        :return: status, messages
        """
        _logger().info('compiling with cobc')
        cob_path = os.path.splitext(path)[0] + '.cob'
        compiler = GnuCobolCompiler()
        compiler.started.connect(self.started.emit)
        compiler.output_available.connect(self.output_available.emit)
        return compiler.compile(cob_path, get_file_type(cob_path),
                                object_files=[Settings().cobmysqlapi])

    def _generate_param_file(self, source_path):
        """
        Generate the bin/EXECUTABLE.param file based on the settings defined in
        the preferences dialog.

        :param source_path: path of the .scb file.
        """
        name = os.path.splitext(os.path.split(source_path)[1])[0] + '.param'
        content = PARAM_FILE_CONTENT % {
            'host': Settings().dbhost,
            'user': Settings().dbuser,
            'pswd': Settings().dbpasswd,
            'dbname': Settings().dbname,
            'port': Settings().dbport,
            'socket': Settings().dbsocket
        }
        output_dir = Settings().output_directory
        if not os.path.isabs(output_dir):
            output_dir = os.path.abspath(os.path.join(source_path, output_dir))
        path = os.path.join(output_dir, name)
        if not os.path.exists(path):
            _logger().info('creating %s', name)
            with open(path, 'w') as f:
                f.write(content)

    def compile(self, path):
        """
        Compile an sql cobol file using dbpre.

        :param path: path of the sql cobol file (.scb)

        :return: build status, list of error/warning messages to
                 display.
        """
        if not self.is_working():
            return -1, []
        output, status = self._run_dbpre(path)
        _logger().info('dbpre output:%s', output)
        if status != 0:
            # dbpre failed with some errors, let the user know about that
            return status, [(output.strip(), CheckerMessages.ERROR, -1, 0,
                             None, None, path)]
        self._copy_dbpre_framework(path)
        status, messages = self._compile_with_cobc(path)
        self._generate_param_file(path)
        return status, messages


class EsqlOCCompiler(QtCore.QObject):
    """
    Provides an interface to esqlOC.exe:

    esqlOC.exe -static -o file.cob file.sqb

    GnuCobol Commands:
    SET OC_RUNTIME=c:\OpenCobol_bin
    SET esqlOC_RUNTIME=c:\esqlOC\release
    SET COB_CFLAGS=-I %OC_RUNTIME%
    SET COB_LIBS=
      %OC_RUNTIME%\libcob.lib %OC_RUNTIME%\mpir.lib %esqlOC_RUNTIME%\ocsql.lib
    SET COB_CONFIG_DIR=
      %OC_RUNTIME%\config\ set PATH=C:\WINDOWS\system32;%OC_RUNTIME%
    call "%PROGRAMFILES%\Microsoft Visual Studio 10.0\VC\vcvarsall.bat"
    %OC_RUNTIME%\cobc.exe -fixed -v -x -static -o c:\Temp\esqlOCGetStart1.exe
      c:\Temp\esqlOCGetStart1.cob
    """
    #: signal emitted when the compilation process started, parameter
    #: is the command
    started = QtCore.Signal(str)

    #: signal emitted when the compilation process finished and its output
    #: is available for parsing.
    output_available = QtCore.Signal(str)

    EXTENSIONS = [".SQB"]

    _INVALID = 'invalid esqlOC executable'

    def __init__(self):
        super().__init__()
        self.esqloc_path = os.path.join(Settings().esqloc, 'esqlOC.exe')

    def is_working(self):
        """

        :return:
        """
        return os.path.exists(self.esqloc_path)

    def make_command(self, source, destination):
        """
        Make the esqloc command.

        :param file_path: .scb path
        """
        return self.esqloc_path, ['-static', '-o', destination, source]

    def _run_esqloc(self, file_path):
        """
        Run the esqloc process and returns it's exit code and
        output (both stderr and stdout).

        :param file_path: .sqb path.
        :return: int, str, str
        """
        path = os.path.dirname(file_path)
        source = os.path.split(file_path)[1]
        destination = os.path.splitext(source)[0] + '.cob'
        pgm, options = self.make_command(source, destination)
        process = QtCore.QProcess()
        process.setWorkingDirectory(path)
        process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        cmd = '%s %s' % (pgm, ' '.join(options))
        _logger().info('command: %s', cmd)
        _logger().debug('working directory: %s', path)
        _logger().debug('system environment: %s', process.systemEnvironment())
        process.start(pgm, options)
        self.started.emit(cmd)
        process.waitForFinished()
        status = process.exitCode()
        try:
            output = process.readAllStandardOutput().data().decode(
                locale.getpreferredencoding())
        except UnicodeDecodeError:
            output = 'Failed to decode esqloc output with encoding: ' % \
                locale.getpreferredencoding()
        self.output_available.emit(output)
        return output, status, destination

    def _compile_with_cobc(self, path):
        """
        Compile the .cob generated by dbpre.

        :param path: path of the .scb file.

        :return: status, messages
        """
        _logger().info('compiling with cobc')
        cob_path = os.path.splitext(path)[0] + '.cob'
        compiler = GnuCobolCompiler()
        compiler.started.connect(self.started.emit)
        compiler.output_available.connect(self.output_available.emit)
        return compiler.compile(
            cob_path, get_file_type(cob_path), additional_options=[
                '-static', '-L%s' % Settings().esqloc, '-locsql.lib'])

    def compile(self, path):
        """
        Compile an sql cobol file using dbpre.

        :param path: path of the sql cobol file (.scb)

        :return: build status, list of error/warning messages to
                 display.
        """
        if not self.is_working():
            return -1, []
        output, status, cob_file = self._run_esqloc(path)
        _logger().info('esqloc output:%s', output)
        if status != 0:
            # esqloc failed with some errors, let the user know about that
            return status, [(output.strip(), CheckerMessages.ERROR, -1, 0,
                             None, None, path)]
        status, messages = self._compile_with_cobc(os.path.join(
            os.path.dirname(path), cob_file))
        return status, messages


if __name__ == '__main__':
    GnuCobolCompiler.get_dependencies('/home/colin/COBDUMP.cbl')
