"""
This is a very carefully-controlled file used to allow all other python modules
to log their activity in a sane manner.  Code which wishes to log its activity
will usually include lines such as the following at the top:

    ####################################
    # SETTING UP THE LOGGER
    import os
    from LiteLog import litelog
    ROOTPATH = os.path.splitext(__file__)[0]
    LOGPATH = "{0}.log".format(ROOTPATH) # this simply specifies the absolute path -- feel free to change this.
    LOGGER = litelog.get(__name__, path=LOGPATH)
    LOGGER.info("----------BEGIN----------")

    # do the following step if you want
    # a global 'debug' log file:
    litelog.set_debug(__file__)
    ####################################

    @litelog.logwrap # <--- do this if you want a __debug__.log to record I/O/Error of function calls
    def f():
        ...
        LOGGER.info('just a test') # <--- do this if you want to log custom
                                   #      messages to the script's personal log.

This will create a <filename>.log file adjacent to the source code file itself.
This is a boon to (human) debuggers.  The logger allows different levels of
criticality (debug, info, warning, error, critical). See
    https://docs.python.org/2/library/logging.html
for more details.

(c) 2015 Matthew Cotton
"""

import logging
from logging.handlers import RotatingFileHandler

import functools
import inspect
import os
import sys
import traceback
import warnings


####################################
# This code defines the ABSOLUTE path of where the
# __debug__.log file should be located

# TODO: Attempt to place __debug__.log at the base of each project?
#       i.e., automatically determine who has imported us?

_DEBUG_LOG_PATH = None
_META_LOGGER    = None
_FIRST          = True

def set_debug(pyfile_obj, meta_logger=True):
    """Puts __debug__.log next to the provided Python __file__"""
    path = os.path.realpath(pyfile_obj)
    set_debug_by_path(path, meta_logger=meta_logger)

def set_debug_by_path(path, meta_logger=True):
    """Puts __debug__.log in the given directory"""
    global _DEBUG_LOG_PATH
    path = os.path.join(path, '') # enfore trailing <SEP>
    _DEBUG_LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(path)), "__debug__.log")
    if meta_logger:
        _create_meta_logger()

def _create_meta_logger():
    """
    We only set up meta-logger if the user wants it

    Please only call this once... ?
    """

    global _META_LOGGER

    if _DEBUG_LOG_PATH is None:
        raise RuntimeError("_DEBUG_LOG_PATH not set!  Can't create meta-logger.")
    elif _META_LOGGER is not None:
        # _META_LOGGER already exists!  Refusing to create a new one
        return

    parent = os.path.dirname(_DEBUG_LOG_PATH)
    _META_LOGGER = get("__debug__", _DEBUG_LOG_PATH, is_debug_log=True) # !!!

####################################


class MattsCustomFormatter(logging.Formatter):
    """
    Class which acts as a Formatter object, but which automatically indents
    log messages based on how many function calls deep the messages originate.
    """
    # TODO: fine-tune indentation levels

    # SOURCE: http://stackoverflow.com/questions/9212228/using-custom-formatter-classes-with-pythons-logging-config-module
    # SOURCE: http://code.activestate.com/recipes/412603-stack-based-indentation-of-formatted-logging/

    def __init__( self, name, fmt=None, datefmt=None, is_debug_log=False ):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.name = name
        self.is_debug_log = is_debug_log
        self.baseline = self.determine_baseline()

    def determine_baseline(self):
        stack = inspect.stack()
        stack = [elems for elems in stack if __file__ not in elems[1]]
        # for row in stack:
        #     print row
        return len(stack)

    def format( self, record ):

        ####################################
        # fetch the function call stack;
        # ignore logwraps as function calls,
        # and filter things like builtins

        stack = inspect.stack()
        stack = [e[1] for e in stack]
        # print "UNMODDED:"
        # for fi in stack:
        #     print fi
        # print "MODDED:"
        stack = [e for e in stack if "Python.framework" not in e]
        stack = [e for e in stack if "logging/__init__.py" not in e]
        stack = [e for e in stack if "litelog.py" not in e]
        # stack = stack[self.baseline:]
        # for fi in stack:
        #     print fi
        # print "is debug log:", self.is_debug_log
        # print len(stack), self.baseline
        # print stack
        # print
        MattsCustomFormatter.STACK = stack

        ####################################
        # establish the indent
        indent = bytearray('...') * (len(stack) - self.baseline)
        if indent:
            indent[0] = ' '
        record.indent = indent

        # record.function = stack[8][3]

        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)

        output_string = self._fmt.format(**record.__dict__)  # REVOLUTIONARY!  Not.

        ####################################
        # the rest of this is taken from
        # the actual logging module!

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it'output_string constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            if output_string[-1:] != "\n":
                output_string = output_string + "\n"
            try:
                output_string = output_string + record.exc_text
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when output_string is Unicode and record.exc_text is str
                # See issue 8924.
                # We also use replace for when there are multiple
                # encodings, e.g. UTF-8 for the filesystem and latin-1
                # for a script. See issue 13232.
                output_string = output_string + record.exc_text.decode(sys.getfilesystemencoding(), 'replace')

        del record.indent
        # del record.function

        return output_string


def get(name, path='activity.log', is_debug_log=False):
    """
    Returns a logger object so that a given file can log its activity.
    If two loggers are created with the same name, they will output 2x to the same file.
    """
    # SOURCE: http://stackoverflow.com/questions/7621897/python-logging-module-globally

    # formatter = IndentFormatter("%(asctime)s [%(levelname)8s] %(module)30s:%(indent)s%(message)s")
    formatter = MattsCustomFormatter(name, "{asctime} [{levelname:8}] {module} :{indent} {message}", is_debug_log=is_debug_log)
    handler = RotatingFileHandler(path, maxBytes=1024 * 100, backupCount=3)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name) # will return same logger if same name given

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger


def logwrap(func):
    """
    This function is a decorator which allows all input/output/errors of any
    given function to be logged, timestamped, and output to a SINGLE __debug__.log FILE!

    Useful for more egregious errors (such as logical errors,
    or the abuse of function signatures).
    """

    global _FIRST, _META_LOGGER

    if _META_LOGGER == None:
        warnings.warn("_META_LOGGER not set up!  @log.logwrap will have no effect!")
        return func

    if _FIRST:
        _META_LOGGER.debug("----------BEGIN----------")
        _FIRST = False

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        """
        Replacement function which wraps I/O and erroring.
        """

        _META_LOGGER.debug("<{}> called with:".format(func.__name__))
        _META_LOGGER.debug("args: {}".format(args))
        _META_LOGGER.debug("kwargs: {}".format(kwargs))

        try:
            out = func(*args, **kwargs)
            _META_LOGGER.debug("<{}> returned: {}".format(func.__name__, out))
            return out
        except:
            # SOURCE: http://stackoverflow.com/questions/9005941/python-exception-decorator-how-to-preserve-stacktrace
            _META_LOGGER.debug("<{}> threw error: {}\n".format(func.__name__, traceback.format_exc()))
            (errorobj, errortype, errtraceback) = sys.exc_info()  # error/type/traceback
            raise errorobj, errortype, errtraceback

    return wrapped


