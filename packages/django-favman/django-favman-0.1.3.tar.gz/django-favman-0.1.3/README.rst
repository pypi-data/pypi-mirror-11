django-favman
===============================================

* `Overview`_
* `Quick start`_

.. _Overview: #overview
.. _Quick start: #quick-start

.. _overview:

Overview?
------------------------------------
django-favman is a simple application that let users bookmark their favorites.



.. _quick-start:

Quick start
------------------------------------
In settings.py, add 'favman' to the INSTALLED_APPS 
In urls.py add ``(r'^favorites/', include('favman.urls'))`` to your urlpatterns

In your templates ::

    {% load favman_tags %}
    
    {% favman_media %}
    
    {{object_to_manage}}{% favman_item object=object_to_manage %}


It will create a two-state icon that indicates if the object is in the user favorites.
Clicking on this icon will toggle the state.

The user can also see the list of /favorites/list/

License
=======

django-favman is licensed under the GNU-LGPL

