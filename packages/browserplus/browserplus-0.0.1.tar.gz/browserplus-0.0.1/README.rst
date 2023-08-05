BrowserPlus
===========

BrowserPlus is an extension of the `mechanize
Browser <http://www.joesourcecode.com/Documentation/mechanize0.2.5/mechanize._mechanize.Browser-class.html>`__
and utilises `lxml <http://lxml.de/>`__ to provide simple methods to
select elements from the current page.

Dependencies
------------

BrowserPlus depends on the following packages:

-  `mechanize <http://wwwsearch.sourceforge.net/mechanize/>`__
-  `lxml <http://lxml.de/>`__
-  `cssselect <https://github.com/SimonSapin/cssselect/>`__

You can install these packages by executing:
``pip install mechanize lxml cssselect``

Setup
-----

To install BrowserPlus, you can either download a copy of the
`browserplus.py <https://raw.githubusercontent.com/vinceau/browserplus/master/browserplus.py>`__
file and put it in the same directory as your project or you can clone
the entire repo into same directory as your project using:

.. code:: bash

    cd my_project
    git clone https://github.com/vinceau/browserplus

Once you have a copy of BrowserPlus, you can import the package and
create an instance using:

.. code:: python

    from browserplus import BrowserPlus
    bp = BrowserPlus()

Usage
-----

Opening a web page
~~~~~~~~~~~~~~~~~~

.. code:: python

    bp.open('http://google.com')

Showing source code
~~~~~~~~~~~~~~~~~~~

.. code:: python

    #print the source code of the current page in a pretty format
    bp.show()

Clicking a link
~~~~~~~~~~~~~~~

If the current web page has the link ``<a href="/login">Login</a>``, you
can click on the link using:

.. code:: python

    bp.go('Login')

Filling in forms
~~~~~~~~~~~~~~~~

Say we had the following form which we wanted to fill out and submit:

.. code:: html

    <form method="post" action="login" id="login_form" name="login_form">
        <input name="username" type="text" />
        <input name="password" type="text" />
        <input name="login_button" type="submit" />
    </form>

Selecting the form
^^^^^^^^^^^^^^^^^^

You can use ``select_form_by()`` to select the form using unique
defining attributes such as id, name, action, etc.

.. code:: python

    #you could do this:
    bp.select_form_by('id', 'login_form')
    #or this:
    bp.select_form_by('name', 'login_form')
    #or this:
    bp.select_form_by('action', 'login')

Setting form values
^^^^^^^^^^^^^^^^^^^

Once the form has been selected, you can set the form values using the
names of the input.

.. code:: python

    bp['username'] = 'admin'
    bp['password'] = 'abc123'

Submitting the form
^^^^^^^^^^^^^^^^^^^

Once you've entered in your desired details, you can submit the form
using:

.. code:: python

    bp.submit()

Finding text
~~~~~~~~~~~~

Sometimes we may want to know whether or not the current web page
contains certain text such as error messages or the like. This can be
done using the ``has()`` method.

.. code:: python

    #ensure login was successful
    msg = 'Login successful'
    assert(bp.has(msg)) 

