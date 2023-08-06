django_ember_toolkit
====================

Tools to integrate develop an Ember app using Django as the backend.

It can:

    *   Generate an Ember app inside your Django project
    *   Preconfigure said app to expect Django REST Framework's JSON data
        format
    *   Automatically generate Ember models based on your Django models
    *   Run Ember automatically alongside your Django development server,
        configuring the Ember app to look for an API endpoint specified in
        Django's `settings.py`.

It makes very few Django-specific changes to the internal Ember project, which
should make it easier to separate the two projects later, if you outgrow the
shared-repo strategy.


Installation
------------

To use django_ember_toolkit, you'll need [Node](https://github.com/joyent/node/wiki/installation)
and [Ember CLI](http://www.ember-cli.com/user-guide/#getting-started). See the
installation instructions at their respective sites for details.

Then just `pip install django_ember_toolkit` and add `django_ember_toolkit` to
your INSTALLED_APPS.


Configuration
-------------

django_ember_toolkit looks in `settings.EMBER_TOOLKIT` for a configuration
dictionary containing:

{
    "API_PATH": "/path/to/api", #the URL at which Ember can find your REST API
    "EMBER_APP_NAME": "some-name", #the name ember-cli should give your app
    "EMBER_APP_PATH": "client", # optional: the filesystem path, relative to
                                # BASE_DIR, where the Ember project should be
                                # stored
    "MODELS_TO_SYNC": ["auth.*", "myapp.Widget"] #  models to use when
                                                    generating Ember models
}

Note: MODELS_TO_SYNC takes a list of model specifiers, each either
"[appname].[ModelClass]" or "[appname].*" (the latter selects all models in the
indicated app)


Usage
-----

django_ember_toolkit exposes a set of new management commands:

*   `create_ember_project`: generates a new Ember app inside your Django
        project, configures it to use Django REST Framework's JSON format,
        and overwrites Ember's environment.js config file to allow
        django_ember_toolkit to easily "push" certain settings into Ember.

*   `generate_ember_config`: generates a backend-config.js file, which is
        loaded by django_ember_toolkit's modified environment.js file. This
        is usually run automatically when you need it.

*   `generate_ember_models`: using ember-cli's scaffolding tools, generates a
        set of client-side models based on the models specified in
        settings.EMBER_TOOLKIT['MODELS_TO_SYNC']. If the models already exist,
        Ember CLI will ask if you want to replace them on an individual basis.

*   `runserver_ember`: runs the Ember development server alongside the Django
        development server.

