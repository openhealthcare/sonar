innovations_r_us
================

Installation
------------
Clone and install the requirements

    git clone https://github.com/openhealthcare/innovations_r_us.git
    pip install -r requirements.txt

Running
-------
Make sure `DEBUG=True` is in your bash environment before running

    export DEBUG=True

Also, make sure [sendgrid](http://sendgrid.com) is set up.  For emails in `DEBUG` use:

    export EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

or

    DEBUG=True EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend python manage.py runserver

