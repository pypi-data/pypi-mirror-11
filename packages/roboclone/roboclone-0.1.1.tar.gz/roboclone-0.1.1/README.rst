RoboClone |buildstatus| |pypiversion| |pypidownloads|
=========================================================================================================================================
A neat little script for cloning git repositories containing FRC robot projects
and configuring them for use with Eclipse.

Install Instructions
--------------------
Open a terminal and run::

   pip install git+https://github.com/simon-andrews/roboclone.git

Usage
-----
Now that you have RoboClone installed, it's time to use it! Open a terminal and type `roboclone`. Something like this
should show up::

   $ roboclone
   usage: roboclone [-h] remote_url [destination]
   roboclone: error: too few arguments

Add the `-h` switch to show a help message::

   $ roboclone -h
   usage: roboclone [-h] remote_url [destination]
   
   positional arguments:
     remote_url   url of the remote git repository (https or ssh)
     destination  directory to clone repository to

   optional arguments:
     -h, --help   show this help message and exit

Clone a repository::

   $ roboclone https://github.com/Team4761/2015-Robot-Code.git
   Cloning into '2015-Robot-Code'...
   remote: Counting objects: 6211, done.
   remote: Total 6211 (delta 0), reused 0 (delta 0), pack-reused 6211
   Receiving objects: 100% (6211/6211), 2.17 MiB | 650.00 KiB/s, done.
   Resolving deltas: 100% (2998/2998), done.
   Checking connectivity... done.

.. |buildstatus| image:: https://img.shields.io/travis/simon-andrews/roboclone.png
    :target: https://travis-ci.org/simon-andrews/roboclone

.. |pypiversion| image:: https://img.shields.io/pypi/v/roboclone.png
    :target: https://pypi.python.org/pypi/roboclone/

.. |pypidownloads| image:: https://img.shields.io/pypi/dm/roboclone.png
    :target: https://pypi.python.org/pypi/roboclone/