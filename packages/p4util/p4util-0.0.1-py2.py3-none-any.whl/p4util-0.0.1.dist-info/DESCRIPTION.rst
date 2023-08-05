p4util - Your Perforce Scripting Toolkit
========================================

Intro
-----

This is a collection of Python scripts that may enhance your Perforce
experience.

To run individual scripts, run:

python -m p4util.script

Install
-------

-  Sync //guest/lester\_cheung/p4util/... to your workspace.

-  Run ``python setup.py install``

Develop
-------

-  Sync //guest/lester\_cheung/p4util/... to your workspace.

-  Run ``python setup.py develop``

This will install the package that points to your workspace using
symlinks so you can test your changes without re-installing.

TODOs
-----

Please file a job against ``project=p4util`` for enhancement requests.

-  [testing] automated testing - patch/pull request welcome!
-  [Script] atime from audit log
-  [log] analyzer
-  [log] structual log analyzer
-  [reviewd] p4review2 as p4util.reviewd
-  [trigger] filename-case-enforce
-  [trigger] archive trigger
-  [trigger] ldap/ad auth triggers (low-priority)

Credits
-------

-  Sven (sven\_erik\_knop) - for his P4Pythonlib
   (//guest/sven\_erik\_knop/P4Pythonlib) and P4Python.


