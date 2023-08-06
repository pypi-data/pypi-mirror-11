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
