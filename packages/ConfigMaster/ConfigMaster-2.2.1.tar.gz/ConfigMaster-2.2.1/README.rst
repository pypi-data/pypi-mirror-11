ConfigMaster
------------

|Build Status| |PyPI version| |PyPI DailyDownloads|

What is ConfigMaster?
---------------------

| ConfigMaster is a simple library for accessing config files
  programmatically. No longer will you have to mess with list lookups
  and dict lookups when you wish to load a config file.
| Instead, objects in the file are accessed as simple class attributes.

What is supported
~~~~~~~~~~~~~~~~~

ConfigMaster supports the following formats built-in:

-  YAML Config Files (through the ``PyYAML`` module)
-  JSON Config Files (through ``json``)
-  INI Config Files (through ``ConfigParser``)
-  Networked versions of YAML/JSON files.

Support for different types of config files grows all the time - feel
free to fork and add support!

TODO
~~~~

-  [STRIKEOUT:Add in support for python ConfigParser formats] *Added in
   version 1.4.0*
-  [STRIKEOUT:Add in networked JSON support] *Added in version 1.3.0*
-  Add more docstrings
-  Make proper documentation
-  [STRIKEOUT:Add tests] *Added in version 1.3.1*

How to install
~~~~~~~~~~~~~~

| For the latest stable version uploaded to PyPI, use:
| ``pip install configmaster``

| For the latest stable version uploaded to bitbucket, use:
| ``pip install git+https://github.com/SunDwarf/configmaster``

| For the latest dev version, use:
| ``pip install git+https://github.com/SunDwarf/configmaster@dev``

After installing, running the tests is recommended.

``py.test -rfEsxXw -v --strict test.py``

How to use
~~~~~~~~~~

ConfigMaster handles everything for you. Simply specify the location of
your file, and the values will be automatically loaded for you.

::

    >>> from configmaster import YAMLConfigFile  
    >>> cfg = YAMLConfigFile.YAMLConfigFile("test.yml") # Created automatically if it doesn't exist  

Networked config files are supported too.

::

    >>> from configmaster import JSONConfigFile
    >>> cfg = JSONConfigFile.NetworkedJSONConfigFile("http://example.com/data.json")

To access config values, get the attribute you want from the config
object stored.

::

    # YAML data is {"a": 1, "b": [1, 2], "c": {"d": 3}}  
    >>> cfg.config.a  
    1  
    >>> cfg.config.b[1]  
    2  
    >>> cfg.config.c.d  
    3    

To populate your config data, just pass a dict to initial\_populate. If
the file is empty, this gives it default values, and returns True. If it
isn't, nothing happens. *Note: This will fail with an
exc.NetworkedFileException on networked files!*

::

    >>> pop = cfg.initial_populate({"a": 1, "b": [1, 2], "c": {"d": 3})
    >>> if pop: cfg.dump() and cfg.reload() # Dump data and reload from disk.

To save your data, run .dump().

::

    >>> cfg.dump()

Have a networked file that you need to save? Use the method
save\_to\_file.

::

    >>> cfg.save_to_file("example.json")

Need to get the raw dict form of a ConfigKey? Use .dump() on that!

::

    >>> cfg.config.dump()
    {"a": 1, "b": [1, 2], "c": {"d": 3}
    >>> cfg.config.c.dump()
    {"d": 3}

.. |Build Status| image:: https://travis-ci.org/SunDwarf/ConfigMaster.svg?branch=master
   :target: https://travis-ci.org/SunDwarf/ConfigMaster
.. |PyPI version| image:: https://img.shields.io/pypi/v/ConfigMaster.svg
   :target: https://pypi.python.org/pypi/ConfigMaster/
.. |PyPI DailyDownloads| image:: https://img.shields.io/pypi/dd/ConfigMaster.svg
   :target: https://pypi.python.org/pypi/ConfigMaster/
