django-pwutils
===================

0.1.17 [2015-XX-XX]
--------------------

0.1.16 [2015-09-22]
--------------------

* Restore support for django-jenkins for projects with django < 1.6
* Drop constraint on Pillow < 2.0


0.1.15 [2015-08-08]
--------------------

* Update django-jenkins in test reqs (drop support for django < 1.6)
* fixed supported django-admin-tools

0.1.14 [2014-11-20]
--------------------

* fixed situation when no databases and caches in test settings
* EmptyField value is not required

0.1.13 [2014-09-29]
--------------------

* update settings to support new django-debug-toolbar
* fixed logging system to easy show only important debug messages
* fixed django to not show http log messages
* inherit devel logging conf from django default logging conf
* use one const PROJECT_ROOT in settings for project home dir

0.1.12 [2014-02-22]
--------------------

* Support new django-jenkins=0.15 and update it requirements for it.

0.1.11 [2013-10-08]
--------------------

* Added delta param to sphinxsearch export command
* In tests move to requirement pylint<1.0, because of astroid bug

0.1.10 [2013-08-12]
--------------------

* TemplateRadioSelect can able to render
  template with request context

0.1.9 [2013-08-09]
--------------------

* patch linklockfile to always get unique name

0.1.8 [2013-07-25]
--------------------

* use lockfile from separate app

0.1.7 [2013-06-21]
--------------------

* log message in gen_sphinx_data command
* do not require SPHINX_PORT setting

* TODO remove search stuff from this app

0.1.6 [2013-05-28]
-------------------------

* added more tests
* require admin-tools>0.5.1
* update requirements for tests
* added predefined settings for jenkins and tests
* added settings for devel

0.1.5
------

* use only timezone aware dates

