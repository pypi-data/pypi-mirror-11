ddah-promises
#############


.. image:: https://api.travis-ci.org/ciudadanointeligente/ddah-promises.svg?branch=master
    :target: https://travis-ci.org/ciudadanointeligente/ddah-promises
    :alt: Build Status

Django's promises egg.

Getting Started
===============

Add "ddah-promises" to INSTALLED_APPS::

    **INSTALLED_APPS** = {
    ...
    'ddah-promises'
    }

Include the ddah-promises URLconf in urls.py::

    url(r'^ddah-promises/', include('ddah-promises.urls'))

Run `python manage.py syncdb` to create ddah-promises's models::

    $ python manage.py syncdb

This project is licensed under the GNU Affero General Public License (AGPL). For more information you can access to the `digital license edition here <http://www.gnu.org/licenses/agpl-3.0.html>`_.


Everything else
===============

For more information about us, our site `Fundación Ciudadano Inteligente <http://www.ciudadanointeligente.org/>`_.
And if you want help with patches, report bugs or replicate our project check `our repositories <https://github.com/ciudadanointeligente/>`_.