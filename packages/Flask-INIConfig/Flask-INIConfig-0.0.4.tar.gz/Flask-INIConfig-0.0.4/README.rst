Flask-INIConfig
===============

.. contents:: Table of contents


Overview
--------

`Flask-INIConfig`_ is a `Flask`_ extension that adds two additional methods ``from_inifile`` and ``from_inifile_sections`` to the ``Flask.config`` configuration instance for an application. This allows you to load ini files or sections from an ini file directly into the config object.


Installation
------------

Install the extension using ``pip``:

.. code:: bash

    $ pip install flask-iniconfig
    
or ``easy_install``:

.. code:: bash

    $ easy_install flask-iniconfig 
    

Usage
-----

Basic Usage
+++++++++++

You can initialize the extension by calling it's constructor:

.. code:: python

    from flask import Flask
    from flask.ext.iniconfig import INIConfig
    
    app = Flask(__name__)
    INIConfig(app)
    # or use the init_app form
    # INIConfig().init_app(app)
    
    app.config.from_inifile('/path/to/file.ini')
    
    property = (app.config.get('section') or {}).get('property')
    
.. important:: 

    * Property and section names are **case-sensitive**.
    * Typically ConfigParsers normlize settings and property names to be lower case, however that is turned off for the instance that is used by the extension.


``from_inifile``
++++++++++++++++

When you use ``from_inifile`` sections in an ini file are individual properties in the config object. For example if you have the following:

.. code:: ini
          
        [section]
        a_property = 1


you can access it as:

.. code:: python

    section = current_app.config.get('section')
    property = section['a_property']

There is a special section for `Flask`_ apps called ``flask`` which can be used to specify the application properties. So if you have the following:

.. code:: ini

    [flask]
    DEBUG = 1
    
you can use ``current_app.config['DEBUG']`` instead of having to specify the section. All property names in the flask section are converted to upper case just like in `from_inifile_sections`_ but only for the flask section.  


``from_inifile_sections``
+++++++++++++++++++++++++

When you use ``from_inifile_sections`` only the relevant sections and the ``flask`` section, if present, are loaded from the ini file. The other major difference is that instead of ``app.config`` having a property with the name of the section, all properties are tacked on to the ``app.config`` object. 

Moreover **all property names are converted to upper-case** as most extensions and Flask's internal `configuration properties <http://flask.pocoo.org/docs/config/#builtin-configuration-values>`_ are all in upper case.

The only **exception** is when you provide the ``preserve_case`` flag to this method. When given this will preserve the case for all *non-flask* options. Flask options will still be converted to upper case. This allows you to use things like `sqlalchemy <http://sqlalchemy.org>`_'s `engine_from_config <http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#sqlalchemy.engine_from_config>`_ directly with the config object.

This is quite useful if you have one ini file with settings for development, staging, production and test settings you can load only the ones you want which can then be used by flask directly.

For e.g. if you have the following:

.. code:: ini
    
    [flask]
    DEBUG = 1
    
    [common]
    a = 1
    b = 0
    
    [dev]
    b = 2
    
    [prod]
    b = 3
    
and you load it using:

.. code:: python
    
    app.config.from_inifile_sections('/path/to/file.ini', ['common', 'dev'])
    
which would add the properties ``A`` and ``B`` to ``app.config``.


Customizing SafeConfigParser
++++++++++++++++++++++++++++
    
If you want to customize the way the internal `SafeConfigParser`_ works you can use the arguments as specified in the `RawConfigParser`_ constructor documentation.

For example:

.. code:: python

    INIConfig(app, defaults={...}, dict_type=OrderedDict, allow_no_value=True)


Implementation Details
----------------------

The base class that implements the extension is derived from `SafeConfigParser`_ and uses that to load the ini file. Consequently you get the built-in parsing and interpolation capabilities of the parser.

Because ``SafeConfigParser`` does not automatically coerce the values to an appropriate type, `Flask-INIConfig`_ will try to do it's best to do some for you. The following cast attempts are made in order of precedence:

    * `int`_
    * `float`_
    * `boolean`_
    * list, dict or tuple (using `ast.literal_eval <https://docs.python.org/2/library/ast.html#ast.literal_eval>`_)
    
.. note:: 
    * You do not get access to the parser instance directly, however the constructor will accept the arguments to ``SafeConfigParser`` and pass them through.
    * The extension deviates from ``SafeConfigParser``'s treatment of boolean because a type-coercion to `int`_ happens before a type-coercion to `boolean`_. So if you want a boolean set it to one of ``yes, no, on, off, true or false`` only.
    
.. warning:: The extension does not try coerce values to types for keys that are already specified in the application configuration. So if you are overriding configuration properties in an ini file you need to be careful about the actual types.


.. _Flask-INIConfig: http://bitbucket.org/wampeter/flask-iniconfig
.. _Flask: http://flask.pocoo.org/
.. _SafeConfigParser: https://docs.python.org/2/library/configparser.html#safeconfigparser-objects
.. _int: https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser.getint>
.. _float: https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser.getfloat>
.. _boolean: https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser.getboolean
.. _RawConfigParser: https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser
