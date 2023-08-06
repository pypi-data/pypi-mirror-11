===============================
Pimp My Pillow
===============================

| |version| |downloads| |wheel|

.. |version| image:: http://img.shields.io/pypi/v/pmp.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pmp

.. |downloads| image:: http://img.shields.io/pypi/dm/pmp.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/pmp

.. |wheel| image:: https://pypip.in/wheel/pmp/badge.png?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pmp



Pimp My Pillow will install a fully working Pillow distribution. No more 'decoder * is not supported' messages!"

* Free software: GPL V3 license

Installation
============

On Debian/Ubuntu distributions you need to install libyaml-dev before running
python setup.py install.


To install it from sources do:

::

   [foo@host]$ git clone https://github.com/edvm/pimp-my-pillow.git
   [foo@host]$ cd pmp; python setup.py install 


To install it from PyPi do as root:

::

   [foo@host]# pip install pimpmypillow 


Or using a virtualenv will work too:

::

   (project)py2@089b711eb21b:~/$ pip install pimpmypillow

   
Usage
=====

PMP can output the needed commands that need to be run in the console to install
Pillow without installing anything in the system. To do this use the 'install'
option with the '--drymode' argument, for example:

::

   (project)py2@089b711eb21b:~/$ pmp install --drymode
   Run the following command as root to install needed dependencies:
   su -c "apt-get install -y tk-dev libjpeg-dev zlib1g-dev libtiff5-dev libfreetype6-dev liblcms2-dev libwebp-dev libtk-img-doc libopenjpeg-dev python-dev gcc cmake"
   
   To have jpeg support, run as root the following script:
   su -c "/opt/py2/.virtualenvs/project/lib/python2.7/site-packages/pmp-0.1.0-py2.7.egg/pmp/scripts/install-openjpeg.sh"
   
   Finally install Pillow with the following command:
   /opt/py2/.virtualenvs/project/bin/pip install Pillow
   
   (project)py2@089b711eb21b:~/$


If you want pmp install Pillow in the system, run it as root like:

::

   [foo@host]# pmp install 


To get pmp command help do:

::

   [foo@host]$ pmp --help 


To have openjpeg support, please install pmp/scripts/install-openjpeg.sh by hand, like:

::

   [foo@host]$ cd pmp/scripts/ 
   [foo@host]$ chmod +x ./install-openjpeg.sh; ./install-openjpeg.sh 


IMPORTANT NOTE: If you have installed Pillow before installing'pmp', you will
need to:

::

   1- Uninstall Pillow
   [foo@host]$ pip uninstall Pillow
   2- Install pmp
   [foo@host]$ pip install pmp 
   3- Use pmp
   [foo@host]$ pip install --drymode 
 
    
When using 'pmp', you should end with a full powered pillow installation like:

::

    *** TKINTER support not available
    --- JPEG support available
    --- OPENJPEG (JPEG2000) support available (2.1)
    --- ZLIB (PNG/ZIP) support available
    --- LIBTIFF support available
    --- FREETYPE2 support available
    --- LITTLECMS2 support available
    --- WEBP support available
    --- WEBPMUX support available

Now pray the gods so someone invite me a beer.


Documentation
=============

Currently Debian 7, Debian 8 and Ubuntu 14.10, 15.04 are supported (give support for other distros
is really easy, please keep reading). This library use yaml files
to know which package should install, please take a look at pmp/settings/debian.yml 
or pmp/settings/ubuntu.yml. It uses one yaml file per gnu/linux distribution. At
each yaml file, keys are distro versions.

Help me support more distros
----------------------------

If when installing your distro is still not supported, you will get a 
traceback like folows:

::

    (virtualenv) root@180121250ef0:/opt/pimp-my-pillow# pmp --help
    usage: pmp [-h] [--interactive] install
    Pimp My Pillow
    positional arguments:
      install        Install Pillow
    optional arguments:
      -h, --help     show this help message and exit
      --interactive  Non interactive
    (bombear) root@180121250ef0:/opt/pimp-my-pillow# pmp install
    Traceback (most recent call last):
      File "/opt/envs/bombear/bin/pmp", line 9, in <module>
        load_entry_point('pmp==0.1.0', 'console_scripts', 'pmp')()
      File "/opt/pimp-my-pillow/src/pmp/__init__.py", line 164, in main
        stderr, stdout = install_pillow(args_.interactive)
      File "/opt/pimp-my-pillow/src/pmp/__init__.py", line 97, in install_pillow
        install_pillow_dependencies(interactive)
      File "/opt/pimp-my-pillow/src/pmp/__init__.py", line 59, in install_pillow_dependencies
        conf = get_gnu_linux_distro_conf()
      File "/opt/pimp-my-pillow/src/pmp/__init__.py", line 50, in get_gnu_linux_distro_conf
        raise Exception("Unknown Gnu/Linux distribution.")
    Exception: Unknown Gnu/Linux distribution.


Its really easy to add support for your Gnu/Linux distro and version:

1- cat the content from /etc/issue, for ex: 

::

    [edvm@edvm-laptop pimp-my-pillow (master)]$ cat /etc/issue
    Ubuntu 15.04 \n \l

    [edvm@edvm-laptop pimp-my-pillow (master)]$


2- Copy and paste a sample setting file, for example:
    https://github.com/edvm/pimp-my-pillow/blob/master/src/pmp/settings/ubuntu.yml

3- The 'etc-issue' value must be the content from your /etc/issue (without the \n \l)

4- Put your setting file (it must end with .yml and must be a valid yaml file) with
the other settings and send the new file you created as a PR! :D 


Be sure to have yaml-devel, python-devel, python-pip and gcc installed
