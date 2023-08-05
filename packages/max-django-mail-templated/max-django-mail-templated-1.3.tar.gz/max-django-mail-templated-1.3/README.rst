==========
Django-Mail-Templated
==========

This is a fork of `https://github.com/artemrizhov/django-mail-templated
<https://github.com/artemrizhov/django-mail-templated/>`_. that includes support for template extension and supports Django 1.8

.. image:: https://travis-ci.org/maximilianhurl/django-mail-templated.svg
   :target: https://travis-ci.org/maximilianhurl/django-mail-templated


Overview
=================
This is a tiny wrapper around the standard EmailMessage class and send_mail()
function. Just pass template_name and context as the first parameters then use
as normal.

Installation
=================
Run::

    $ pip install max-django-mail-templated

And register the app in your settings file::

    INSTALLED_APPS = (
        ...
        'mail_templated'
    )

Usage
=================
Write a template to send a plain text message. Note that first and last newline
will be removed::

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

Or for an html message::

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> message.
    {% endblock %}

Or for a multipart message you can use both blocks::

    {% block subject %}
    Hello {{ user.name }}
    {% endblock %}

    {% block body %}
    This is a plain text message.
    {% endblock %}

    {% block html %}
    This is an <strong>html</strong> message.
    {% endblock %}

Or leave out some block to set it manually later with EmailMessage class::

    {% block body %}
    This is a plain text message.
    {% endblock %}

Now you can send it::

    from mail_templated import send_mail
    send_mail('email/hello.tpl', {'user': user}, from_email, [user.email])


You can add in BCC like this::

    send_mail('email/hello.tpl', {'user': user}, from_email, [user.email], bcc=[user2.email])

You can also add an attachment like this::

	send_mail('email/hello.tpl', {'user': user}, from_email, [user.email], attachment="file/path.pdf")

Or if you wish to add more control over message creation then use the class form::

    from mail_templated import EmailMessage
    message = EmailMessage('email/hello.tpl', {'user': user}, to=[user.email])
    # ... attach a file, etc
    message.send()

That's all. Please create an issue at GitHub if you have any notes,
...or just email :)

Extends
=================

You can extend templates like so::

	{% extends "email_base.tpl" %}

	{% block subjectcontent %}
	Subject
	{% endblock %}

	{% block bodycontent %}
	 This is a plain text message.
	{% endblock %}

	{% block htmlcontent %}
	This is an <strong>html</strong> message.
	{% endblock %}


and email_base.tpl would look like this::

	{% block subject %}
	{% block subjectcontent %}{% endblock %}
	{% endblock %}

	{% block body %}
	A heading or logo
	{% block bodycontent %}{% endblock %}
	{% endblock %}

	{% block html %}
	A heading or logo
	{% block htmlcontent %}{% endblock %}
	{% endblock %}

**Please note that you must include all blocks in the base template file.**

If you dont include one of the blocks in the base template it will not be shown. So you cannot, for example, move the subject block into the top file.


Tests
=================

To run the unit tests you first need to create a virutal env in project root directory.

    virtualenv env

Then you need to install the test requriements.

    env/bin/pip install -r requirements.txt

Now you can run the unit tests using the following command.

    env/bin/python mail_templated/tests/runtests.py
