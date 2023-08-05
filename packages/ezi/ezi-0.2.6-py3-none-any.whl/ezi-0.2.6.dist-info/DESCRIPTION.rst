==========
Python Ezi
==========

``ezi`` is a Python interface to the Ezidebit payment gateway.


Example
-------

To add a new direct debit by bank account or credit card:

.. code-block:: python

    >>> from ezi import add_bank_debit, add_card_debit, add_payment, clear_schedule
    >>> add_bank_debit(
    ...    608725, 'Example', 'Person', 'email@example.com', 'invoice-99',
    ...    '200', '2015-03-01', 'Mr Person', '111111', '123456',
    ...    'https://api.demo.ezidebit.com.au/v3-3/pci?singleWsdl',
    ...    'YOUR DIGITAL KEY')

    >>> add_card_debit(
    ...    608725, 'Example', 'Person', 'email@example.com', 'invoice-99',
    ...    '200', '2015-03-01', 'Mr Example', '4444333322221111', '01/16',
    ...    'https://api.demo.ezidebit.com.au/v3-3/pci?singleWsdl',
    ...    'YOUR DIGITAL KEY')

    >>> clear_schedule(
    ...    608725,
    ...    'https://api.demo.ezidebit.com.au/v3-3/nonpci?singleWsdl',
    ...    'YOUR DIGITAL KEY')

    >>> add_payment(
    ...    608725, 'invoice-99', '200', '2015-03-01',
    ...    'https://api.demo.ezidebit.com.au/v3-3/nonpci?singleWsdl',
    ...    'YOUR DIGITAL KEY')

    >>> edit_customer_bank_account(
    ...    608725, 'Mr Example', '111111', '123456',
    ...    'https://api.demo.ezidebit.com.au/v3-3/pci?singleWsdl',
    ...    'YOUR DIGITAL KEY')

    >>> edit_customer_credit_card(
    ...    608725, 'Mr Example', '4444333322221111', '01/16',
    ...    'https://api.demo.ezidebit.com.au/v3-3/pci?singleWsdl',
    ...    'YOUR DIGITAL KEY')


Release History
---------------

0.2.6 (2015-08-13)
++++++++++++++++++

**Improvements**

 - Handle ``suds.WebFault`` and translate to an ``EzidebitError``.


0.2.5 (2015-07-31)
++++++++++++++++++

**Improvements**

 - Add ``HISTORY.rst``.


0.2.4 (2015-07-31)
++++++++++++++++++

**Improvements**

 - Add syntax highlighting to ``README.rst``.


