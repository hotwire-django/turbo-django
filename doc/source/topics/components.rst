==========
Components
==========


Components are a subclass of `Stream` that simplifies implementation of streams.



Creating a Component
--------------------

Components are a type of stream with a template.  As components are a type of stream, components must be either be created in or imported to `streams.py` to be registered.


Quick example
=============

.. code-block:: python
    :caption: app/streams.py

    from turbo.components import BroadcastComponent

    class AlertBroadcastComponent(BroadcastComponent):

        template_name = "components/sample_broadcast_component.html"


Add a simple template:

    .. code-block:: html
        :caption: templates/components/sample_broadcast_component.html

        {% if alert_content %}
        <div class="alert alert-{{alert_class}}" role="alert">
          {{alert_content}}
        </div>
        {% endif %}

The component can be rendered in one of two ways.

.. code-block:: html
    :caption: templates/view_template.html

    {% load turbo_streams %}

    If an instance of the component is passed in via the view:
    {% turbo_component alert_component %}

    To access the component globally:
    {% turbo_component "app_name:AlertBroadcastComponent" %}


This will insert the contents of `components/sample_broadcast_component.html` on the template.

To stream updated content to the view, open a python terminal, instanciate the component, and render a new update.


.. code-block:: python

    from app_name.streams import AlertBroadcastComponent
    alert_component = AlertBroadcastComponent()
    alert_component.render(
        alert_class='warning',
        alert_content='The server will restart in 10 minutes'
    )


.. admonition:: Multiple identical components

    Using the same component twice in a template, will only update the first component on the page.  This is a current purposeful limitation of the Hotwire framework.  In the above examples, while the components will render initially, only the first component will receive the streamed content.




Full example
=============

.. code-block:: python
    :caption: app/streams.py

    from turbo.components import BroadcastComponent

    class AlertBroadcastComponent(BroadcastComponent):

        template_name = "components/sample_broadcast_component.html"

        def get_context(self):
            """
            Return the default context to render a component.
            """
            return {}

        def user_passes_test(self, user):
            """
            Only allow access to the component stream if the user passes
            this test.
            """
            return user.is_authenticated


.. module:: turbo.components

BroadcastComponent
==================

.. class:: BroadcastComponent

    A broadcast component will stream a template to all users.

Example
-------

.. code-block:: python
    :caption: app/streams.py

    from turbo.components import BroadcastComponent

    class AlertBroadcastComponent(BroadcastComponent):
        template_name = "components/sample_broadcast_component.html"

.. code-block:: html
    :caption: templates/components/sample_broadcast_component.html

    {% if alert_content %}
    <div class="alert alert-{{alert_class}}" role="alert">
      {{alert_content}}
    </div>
    {% endif %}

.. code-block:: html
    :caption: templates/view_template.html

    {% load turbo_streams %}

    {% turbo_component "app_name:AlertBroadcastComponent" %}



To stream an updated template to the component:

.. code-block:: python

    from .streams import AlertBroadcastComponent

    component = AlertBroadcastComponent()
    component.render(
        alert_class='warning',
        alert_content='The server will restart in 10 minutes'
    )


UserBroadcastComponent
======================

.. class:: UserBroadcastComponent

    A user broadcast component will stream a template to a specific user.

Example
-------

.. code-block:: python
    :caption: app/streams.py

    from turbo.components import UserBroadcastComponent

    class CartCountComponent(UserBroadcastComponent):
        template_name = "components/cart_count_component.html"

        def get_context(self):
            return {
                "count": self.user.cart.items_in_cart
            }


.. code-block:: html
    :caption: templates/components/cart_count_component.html

    <button type="button" class="btn btn-primary position-relative">
      Cart

      {% if count %}
      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
        {{count}}
        <span class="visually-hidden">Items in cart</span>
      </span>
      {% endif %}

    </button>


.. code-block:: html
    :caption: templates/view_template.html

    {% load turbo_streams %}

    {% turbo_component "chat:CartCountComponent" request.user %}
    or
    {% turbo_component cart_count_component %}


