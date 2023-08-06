======
icheck
======

"Because syntax checking should happen on file writes, not VCS commits"

quick (or not so quick) and dirty tool to run syntax checking and doc tests
on python code in a separate screen window

Features
---------
* Syntax check files
* Doc test files
* Call a command on syntax failures
* terminal bell
* filter files by hashbang and globs
* color output with tty detection
* multiple output formats (oneline, short and long)
* Supports python2 and python3

This program was mainly written to assist me in developing python code and 
letting me know a couple of seconds before i try and run my program that there 
are basic syntax mistakes in the code.

to achieve this inotify is used to wait for files to be written to and then if 
all pre conditions are fine (globs and hashbangs) then a syntax check is 
executed. on an error a message is printed and it moves on to the next file

By using the 'bell' facility the window running check does not have to be 
visible to the programmer and instead a message will be printed in the message 
line on error indicating attention may be required, allowing screen to be used 
as the windowing component of a flexible IDE setup

Examples
---------
To check a directory for file changes and run syntax checks on file save try 
the following command

    $ icheck -b ~/code/icheck/icheck/

This will 'ring the bell' in the terminal on file changes that are 
syntactically incorrect. in screen this causes a 'bell in window x' message to 
be displayed at the bottom of the screen for all files in the directory

To limit ourselves to just scanning .py files (sounds like a good idea!) we can 
add a filter based on filename with the '-g' flag

    $ icheck -b -g '\*.py' ~/code/icheck/icheck/

Optionally we can filter based on the hash-bang at the beginning of the file 
with '-s' this defaults to looking for the string 'python' however this can be 
changed by specifying it after the '-s' flag. This is applied in an 'AND' 
fashion with the '-g' flag so that the file extension AND the shebang need to 
match. if only one detection method is desired then only use one flag or 
optionally use neither detection and specify exactly which files you want to 
watch (ie specifying files on the cmdline rather than the directory they are 
contained in)


Limitations
------------
* At this point in time file watching is not recursive, creating directories 
  does not cause them to be watched. It is assumed that the project layout that 
  you are watching is mostly static for the time being. to watch 
  sub-directories try the command below

    $ icheck ~/code/icheck/icheck ~/code/icheck/icheck/\*/


.. :changelog:

Release History
---------------

1.8 (2015-08-29)
++++++++++++++++
- Run Doctests as well as syntax checking

1.7 (2015-08-15)
++++++++++++++++

**Bug Fixes**

- Errors on the last line of a src file would crash the checker

1.6 (2014-10-24)
++++++++++++++++

**Bug Fixes**

- Certain conditions would prevent a variable that was used from being set/create

1.5 (2014-10-24)
++++++++++++++++

- Fixed up some links in setup.py
- Add reason why the syntax check failed to output, where available

1.4 (2014-10-24)
++++++++++++++++

- Check on file close rather than write to avoid partial files

1.3 (2014-10-20)
++++++++++++++++

- Add python 2.7 compatibility

1.2.1 (2014-10-20)
++++++++++++++++++

**Bug Fixes**

- Fix packaging again and convert to module, now installs correctly

1.2 (2014-10-20)
++++++++++++++++

**Bug Fixes**

- Fix packaging so setup.py is included again

1.1 (2014-10-20)
++++++++++++++++

- Change-log now appended to project description

**Bug Fixes**

- Fixed (one) race condition on checking hashbang
- Fixed up entry point to eat stack trace on Keyboard Interrupt

1.0 (2014-10-19)
++++++++++++++++

- Initial Release




