.. role:: python(code)
   :language: python



.. image:: https://travis-ci.org/bielbienne/bst.pygasus.demo.svg?branch=master
    :target: https://travis-ci.org/bielbienne/bst.pygasus.demo

.. contents::

Introduction
============

Pygasus is a new Python 3 framework to build web applications with
`Sencha ExtJS <https://www.sencha.com/products/extjs/#overview>`_. Pygasus is designed to be full
customizable for your project. 

bst.pygasus and all corresponding submodules are licensed under the ZPL 2.1, see LICENSE.txt for details.

Architecture
------------

.. figure:: docs/architecture.png
   :alt: Architecture

   yellow modules are planned to be developed in the near future

The various packages are:

bst.extjs.core
    The core package of the framework that assembles all required packages together.

bst.extjs.datamanager
    The datamanager manages data coming from the client and data sent to the client's browser.

bst.extjs.i18n
    This package handles the translation for multilingual sites and applications.

bst.extjs.scaffolding
    Scaffolding is a package to generate standard models, stores, views and grids for ExtJS. 

bst.extjs.security
    This package provide a default login mask and a pluggable authentication. In the future we also plan to
    implement a role based permission model.

bst.extjs.session
    This package creates a cookie on client browsers and provides a server side session store.

bst.extjs.wsgi
    The layer needed to let the application work as a WSGI server.

bst.extjs.resources
    This package is responsible to share all needed static resources with the client.


Getting started
===============

Recommendation
--------------

The ZCA (Zope component Architectur) is a main element in this framework. If you are not familiar with it, we recommend you first learn its basics. You can follow the links at the bottom of this page. Also other external libraries are already well documented, which is why we didn't want to do that twice.

Buildout
--------

We recommend to setup up a buildout for your project. First it will install all required dependencies and the scripts needed to run a server. The boostrap file can be downloaded at https://bootstrap.pypa.io/bootstrap-buildout.py.

File structure:

.. code::

    buildout
    ├── bootstrap.py
    ├── buildout.cfg
    ├── etc
    │   ├── deploy.ini.in
    │   └── site.zcml.in
    └── dev
        └── myproject

buildout.cfg

.. code:: ini

    [buildout]
    
    extends = 
        https://raw.githubusercontent.com/bielbienne/bst.pygasus.demo/master/sources.cfg
        https://raw.githubusercontent.com/bielbienne/bst.pygasus.demo/master/versions.cfg
    
    develop = dev/myproject  
    parts =
        app
        zcml
        lingua
    
    extensions = mr.developer
    auto-checkout =
        js.extjs
        bst.pygasus.core
        bst.pygasus.wsgi
        bst.pygasus.scaffolding
        bst.pygasus.datamanager
        bst.pygasus.resources
        bst.pygasus.security
        bst.pygasus.session
        bst.pygasus.i18n
        bst.pygasus.demo
    
    [debug_ini]
    recipe = collective.recipe.template
    input = etc/deploy.ini.in
    output = ${buildout:parts-directory}/etc/${:outfile}
    outfile = debug.ini
    
    [zcml]
    recipe = collective.recipe.template
    input = etc/site.zcml.in
    output = ${buildout:parts-directory}/etc/${:outfile}
    outfile = site.zcml
    
    [app]
    recipe = zc.recipe.egg:script
    arguments="${debug_ini:output}"
    eggs =
        bst.pygasus.wsgi
        myproject

    [lingua]
    unzip = true
    recipe = zc.recipe.egg
    eggs =
        lingua
        bst.pygasus.i18n

etc/deploy.ini.in

.. code:: ini

    [zcml]
    path = ${zcml:output}

    [app:main]
    use = egg:bst.pygasus.wsgi#main

    [server:debug]
    use = egg:waitress#http
    host = 127.0.0.1
    port = 5000
    threadpool_workers = 1
    threadpool_spawn_if_under = 1
    threadpool_max_requests = 0

etc/site.zcml.in

.. code:: xml

    <configure xmlns="http://namespaces.zope.org/zope">
        <include package="myproject" />
    </configure>

Run your buildout. (You must first create your own project as shown in next part)

.. code:: bash

    $ cd buildout
    $ python3 boostrap.py
    $ ./bin/buildout


Create an application
---------------------

Proposed File Structure
~~~~~~~~~~~~~~~~~~~~~~~

We propose the following file structure inside your python egg:

.. code::

    ├── app
    │   ├── application.js
    │   ├── controller
    │   │   ├── Card.js
    │   │   └── Main.js
    │   ├── resources
    │   │   └── css
    │   │       └── styles.css
    │   └── view
    │       ├── CardView.js
    │       └── MainView.js
    ├── configure.zcml
    ├── extjs.py
    ├── handler.py
    ├── __init__.py
    ├── locales
    │   ├── bb.extjs.demo.pot
    │   └── fr
    │       └── LC_MESSAGES
    │           ├── bst.pygasus.demo.mo
    │           └── bst.pygasus.demo.po
    ├── model.py
    └── schema.py


setup configure.zcml
~~~~~~~~~~~~~~~~~~~~

.. code:: xml

    <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:grok="http://namespaces.zope.org/grok"
               xmlns:i18n="http://namespaces.zope.org/i18n"
               i18n_domain="myproject">
    
        <include package="bst.pygasus.core" />
    
        <grok:grok package="." />
    
        <i18n:registerTranslations directory="locales" />
    
    </configure>


Create an application context (extjs.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from fanstatic import Library
    from fanstatic import Resource
    from bst.pygasus.core import ext
        
    library = Library('demo', 'app')

    class DemoContext(ext.ApplicationContext):
    
        title = 'Demo'
        application = 'bst.pygasus.demo.Application'
        namespace = 'bst.pygasus.demo'
        resources = Resource(library, 'application.js',
                             depends=[ext.extjs_resources])


Register additional ExtJS paths (extjs.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ExtJS needs to know where additional ExtJS-Classes can be loaded. This is why each namespace used in ExtJS needs to be registred. In this example we regstister two namespaces for 'bst.pygasus.demo.view' and 'bst.pygasus.demo.controller'. The path usually begins with 'fanstatic', followed by your library name (e.g. "demo") ( :python:`Library('demo', 'app')` ) and then, at the end, a subdirectory.

.. code:: python

    class ViewClassPathMapping(ext.ClassPathMapping):
        namespace = 'bst.pygasus.demo.view'
        path = 'fanstatic/demo/view'

    class ViewClassPathMapping(ext.ClassPathMapping):
        namespace = 'bst.pygasus.demo.contoller'
        path = 'fanstatic/demo/controller'


Define a schema (schema.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

With this schema different ExtJS-Classes like form, store or model, are auto generated on the fly. Look at the package bst.pygasus.scaffolding for the supported types and class generation. Feel free to extend this with your own generators of ExtJS classes for your project. This schema will also be used to transform json to a python model or vice versa.

.. code:: python

    from bst.pygasus.core import ext
        
    from zope import schema
    from zope.interface import Interface
    
    @ext.scaffolding('Card', 'Magic the Gathering')
    class ICard(Interface):
        id = schema.Id(title='ID', required=False)
    
        name = schema.TextLine(title='Name', required=True)

        costs = schema.Int(title='Costs', required=False)

        publication = schema.Date(title='Publication', required=True)


Create a Model (model.py)
~~~~~~~~~~~~~~~~~~~~~~~~~

The model is used to transfer data from the server to client and back.

.. code:: python

    from bst.pygasus.core import ext
    from bst.pygasus.demo import schema
    from zope.schema.fieldproperty import FieldProperty

    class Card(ext.Model):
        ext.schema(schema.ICard)
        
        id = FieldProperty(ICard['id'])
        name = FieldProperty(ICard['name'])
        costs = FieldProperty(ICard['costs'])
        publication = FieldProperty(ICard['publication'])


Create a handler for CRUD requests (handler.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The handler for an definded model provides the CRUD operations. Now it is up to you to implement whatever you need in these methods.

.. code:: python

    class CardHandler(ext.AbstractModelHandler):
        ext.adapts(model.Card, IRequest)
    
        def get(self, model, batch):
            start, limit = self.slice()
            property, direction = self.sort()
    
            return cardIndexer.search_index(start, limit, property, direction)
    
        def create(self, model, batch):
            model.id = cardIndexer.get_next_id()
            cardIndexer.extend_index(model)
    
            return [model], 1
    
        def update(self, model, batch):
            cardIndexer.update_index(model)
    
            return [model], 1
    
        def delete(self, model, batch):
            cardIndexer.reduce_index(model)
    
            return [model], 1



i18n (Internationalization)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usually you define a domain name for each package. In order to do that you create an instance of MessageFactory in the __init__.py file:

.. code:: python

    from zope.i18nmessageid import MessageFactory

    _ = MessageFactory('bst.pygasus.demo')

Now you can use translation messages anywhere you want to translate a string to multiple languages:

.. code:: python

    publication = schema.Date(title=_('publication_title', default='Publication'), required=True)


If you want use translations in ExtJS, it works similar to translations in python. Simply write a variable at the top of the file and pass the domain name in the MessageFactory:

.. code:: javascript

    var _ = i18n('bst.pygasus.demo');

    Ext.define('bst.pygasus.demo.view.MainView', {
        extend: 'Ext.container.Viewport',
    
        ....

Now you can translate messages with the variable defined anywhere in the class:

.. code:: javascript

    items: [{
        xtype: 'button',
        action: 'save',
        text: _('tr_save', 'Save'),
    },


You can use the lingua package to crawl translation from python and ExtJS files and generate a .pot file with it. This application is already installed by  buildout. After generating a .pot file you can use different kinds of gettext tools to merge and build the final .po and .mo files for each language:

.. code:: bash

    ./bin/pot-create –d <domain> -o <filename>.pot <source>


Using Scaffolding
~~~~~~~~~~~~~~~~~

Scaffolding provides default ExtJS-classes that can be directly used. Use the the "required" attribute to load a scaffolding class. In follow example we have defined the xtype to "DisplayCard". This will generate a read only view with all fields from the schema ICard.

.. code:: javascript

    Ext.define('bst.pygasus.demo.view.CardView', {
        extend: 'Ext.window.Window',
    
        requires: [
            'scaffolding.display.Card'
        ],
    
        itemId: 'cardView',
        layout: 'vbox',
    
        initComponent: function() {
            var me = this;
            
            me.items = [{
                xtype: 'DisplayCard',
                itemId: 'displayCard',
                title: '',
                maxWidth: '500'
            },
            {
                xtype: 'button',
                text: 'Delete',
                action: 'delete'
            }];
    
            me.bodyPadding = '5 5 5 5';
    
            me.callParent(arguments);
        }
    
    });

As an another example we use buffered store from scaffolding:

.. code:: javascript

    Ext.define('bst.pygasus.demo.controller.Main', {
        extend: 'Ext.app.Controller',
        
        requires: [
            'scaffolding.bufferedstore.Card'
        ],
        
        ....



Demo application
----------------
We have a demo application that you can easily install with a buildout file. If you are interested, please follow the instruction at `bst.pygasus.demo <https://github.com/bielbienne/bst.pygasus.demo>`_.


External References
===================

* http://zopeinterface.readthedocs.org/en/latest/
* http://zopecomponent.readthedocs.org/en/latest/
* https://www.python.org/dev/peps/pep-0333/
* https://pypi.python.org/pypi/martian
* https://pypi.python.org/pypi/zc.buildout/2.4.0
* http://grok.zope.org/documentation/tutorial/grok-poller-tutorial/adapters
* http://www.fanstatic.org/en/latest/


About us
========
We are the IT Services of Biel/Bienne, Switzerland.
http://foss.biel-bienne.ch/blog/
