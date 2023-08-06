
==================
Leonardo Analytics
==================

The django-analytical application integrates analytics services into a Leonardo project.

Thanks @jcassee

.. contents::
    :local:

Currently Supported Services
----------------------------

* `Chartbeat`_ traffic analysis
* `Clickmap`_ visual click tracking
* `Clicky`_ traffic analysis
* `Crazy Egg`_ visual click tracking
* `Gaug.es`_ realtime traffic tracking
* `Google Analytics`_ traffic analysis
* `GoSquared`_ traffic monitoring
* `HubSpot`_ inbound marketing
* `Intercom`_ live chat and support
* `KISSinsights`_ feedback surveys
* `KISSmetrics`_ funnel analysis
* `Mixpanel`_ event tracking
* `Olark`_ visitor chat
* `Optimizely`_ A/B testing
* `Performable`_ web analytics and landing pages
* `Piwik`_ open source web analytics
* `Reinvigorate`_ visitor tracking
* `SnapEngage`_ live chat
* `Spring Metrics`_ conversion tracking
* `UserVoice`_ user feedback and helpdesk
* `Woopra`_ web analytics

.. _`Chartbeat`: http://www.chartbeat.com/
.. _`Clickmap`: http://getclickmap.com/
.. _`Clicky`: http://getclicky.com/
.. _`Crazy Egg`: http://www.crazyegg.com/
.. _`Gaug.es`: http://gaug.es/
.. _`Google Analytics`: http://www.google.com/analytics/
.. _`GoSquared`: http://www.gosquared.com/
.. _`HubSpot`: http://www.hubspot.com/
.. _`Intercom`: http://www.intercom.io/
.. _`KISSinsights`: http://www.kissinsights.com/
.. _`KISSmetrics`: http://www.kissmetrics.com/
.. _`Mixpanel`: http://www.mixpanel.com/
.. _`Olark`: http://www.olark.com/
.. _`Optimizely`: http://www.optimizely.com/
.. _`Performable`: http://www.performable.com/
.. _`Piwik`: http://www.piwik.org/
.. _`Reinvigorate`: http://www.reinvigorate.net/
.. _`SnapEngage`: http://www.snapengage.com/
.. _`Spring Metrics`: http://www.springmetrics.com/
.. _`UserVoice`: http://www.uservoice.com/
.. _`Woopra`: http://www.woopra.com/

Installation
------------

.. code-block:: bash

    pip install leonardo-module-analytics

or as leonardo bundle

.. code-block:: bash

    pip install django-leonardo["analytics"]

Add ``leonardo_module_analytics`` to APPS list, in the ``local_settings.py``::

    APPS = [
        ...
        'leonardo_module_analytics'
        ...
    ]

    GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-62809705-1'
    GOOGLE_ANALYTICS_SITE_SPEED = True
    GOOGLE_ANALYTICS_ANONYMIZE_IP = True


for configuration specific service see https://pythonhosted.org/django-analytical/services.html#services

Sync static

.. code-block:: bash

    python manage.py sync_all

Read More
---------

* https://github.com/jcassee/django-analytical
* https://github.com/django-leonardo/django-leonardo


