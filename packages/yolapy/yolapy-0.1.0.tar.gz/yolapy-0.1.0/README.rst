Yola API Python Client
======================

Usage
-----

.. code:: python

    from yolapy.services import Yola


    yola = Yola(
        url='https://wl.qa.yola.net/',
        auth=('username', 'password'))

    yola.create_user(
        email='test@example.com',
        name='Jane',
        surname='Doe',
        partner_id='WL_YOLA',
        preferences={'name': 'value'})

See http://yolapy.readthedocs.org/ for available methods with
documentation.

Development
-----------

To lint your code automatically when you make changes::

    $ cp tube.py.sample tube.py
    $ stir
