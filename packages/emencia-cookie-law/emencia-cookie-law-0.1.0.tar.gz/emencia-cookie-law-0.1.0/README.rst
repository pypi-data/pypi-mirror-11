.. _Django: https://www.djangoproject.com/
.. _jquery.cookie: https://github.com/carhartl/jquery-cookie

==================
Emencia Cookie Law
==================

A Django app to easily integrate a banner about EU Cookie Law

Display a HTML banner (or whatever you want if you override the template) to inform about *European Cookie Law* with a link for more informations and another link to accept and continue to browse site. Once clicked the accept link push a cookie to the browser so the banner won't never display again.

Links
*****

* Download his `PyPi package <https://pypi.python.org/pypi/emencia-cookie-law>`_;
* Clone it on his `repository <https://github.com/emencia/emencia-cookie-law>`_;

Requires
********

* `Django`_ >= 1.4;
* jQuery >= 1.2;
* `jquery.cookie`_ == 1.4.1;

Install
*******

First install the package ::

    pip install emencia-cookie-law

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        'cookie_law',
        ...
    )

Now you will need to integrate it in your templates.

Optional settings
-----------------

COOKIELAW_COOKIE_NAME
.....................

Default to ``emencia_cookie_law``.

The cookie name pushed to the browser if the user click on the accept link. Note that this name is hardcoded in the shipped Javascript plugin, so if you change it you will have to code another plugin.

COOKIELAW_TEMPLATE
..................

Default to ``cookie_law/banner.html``.

The filepath to the banner template. You don't need to edit this settings to change the banner aspect, just override the template with the same relative filepath in your project templates directory.


Templates integration
---------------------

Recommended way is to have a basic file for all your project templates, often named ``base.html``  or ``skeleton.html``, so you'll just integrate *cookie_law* only once.

#. In your template(s), load the Javascript file: ::

       <script type="text/javascript" src="/static/js/cookie_law/cookie_law.js"></script>
   
   Don't forget *jQuery* and *jquery.cookie* requirements also (if you are using Foundation, they are allready loaded).

#. Load the the cookie_law tag library at top of your template: ::

       {% load cookie_law %}

#. Then call its tag where you want, commonly as the first element in your ``<body/>`` content: ::

       {% cookie_law_banner %}

Default template has been made with Foundation components, if you don't use it or use another CSS Framework, you should override it see `COOKIELAW_TEMPLATE`_.

Because the default template has been done for Foundation, there is no need of any CSS to load.

Usage
*****

Nothing special. The banner display until you accept the game from the button within the banner. 

Once accepted the browser is given a cookie so the user won't see again the banner. The cookie lifetime expires in 10 years since accept.
