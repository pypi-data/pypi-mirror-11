LiteLog
=======

LiteLog is an easy-to-use, totally standard-library Python logging utility that makes complex logging functions easy.

Features
--------

    * automatically-named per-file logfiles, specifically written next to the source files.
    * special __debug__ log, where tagged functions can have all of their input/output/errors safely reported completely transparently and without interference.
    * different log message levels, just like the 'logging' builtin.
    * recursive calls in __debug__ are indented, so determining function call depth is natural.

Installation
------------

To install globally, run:

    sudo pip install litelog

To install locally (such as within a virtual environment), run:

    pip install litelog

Usage
-----

The following is copy-and-pasteable code, so long as litelog is available globally:

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

When pasted at the top of your program, the above lines:

    * create a logger specifically for the current file, with the same name (ex:  test.py -> test.log)
    * add a starting line/delimiter to the log, to indicate separate module imports/runs (by default, the logs are *appended* to)
    * creates an optional global "debug" logger, which can record the I/O/Errors of any function tagged with '@litelog.logwrap' (set_debug() should only be called once)

Here are the actual use case examples:

    @litelog.logwrap # <--- do this if you want a __debug__.log to record I/O/Error of function calls
    def f():
        ...
        LOGGER.info('just a test') # <--- do this if you want to log custom
                                   #      messages to the script's personal log.

    ####################################
    # logging levels:
    LOGGER.debug   (...)
    LOGGER.info    (...)
    LOGGER.warning (...)
    LOGGER.error   (...)
    LOGGER.critical(...)