LiteLog
=======

LiteLog is an easy-to-use, totally standard-library Python logging utility that makes complex logging functions easy.

Features
--------

    * automatically-named per-file logfiles, specifically written next to the source files.
    * special __debug__ log, where tagged functions can have all of their input/output/errors
      safely reported completely transparently and without interference.
    * different log message levels, just like the 'logging' builtin.
    * recursive calls in __debug__ are indented, so determining function call depth is natural.
