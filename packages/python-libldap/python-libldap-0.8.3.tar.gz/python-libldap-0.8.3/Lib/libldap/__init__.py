# -*- coding: utf-8 -*-
# Copyright (C) 2015 Yutaka Kamei
"""libldap package

**libldap** is libldap Python binding.
Following objects are exposed.

LDAP
====

This class has following LDAP operation methods.

* bind_
* unbind_
* search_
* paged_search_
* add
* modify
* delete
* rename
* compare
* whoami
* passwd
* start_tls
* set_option
* get_option
* abandon
* cancel
* result
* search_result

bind
-----

This is the method for LDAP bind operation. If you do not use this method,
the relative LDAP_ instance will operate anonymously.

For example:

.. code::

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')

This method supports asynchronous operation by passing async=True parameter.
Asynchronous operation returns message ID. You can use it like this:

.. code::

    >>> from pprint import pprint
    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> msgid = ld.bind('cn=master,dc=example,dc=com', 'secret', async=True)
    >>> result = ld.result(msgid)
    {'error_message': None,
     'message': 'Invalid credentials',
     'referrals': [],
     'return_code': 49}

If LDAP server has ppolicy overlay, you can set LDAP_CONTROL_PASSWORDPOLICYREQUEST
control like this:

.. code::

    >>> from pprint import pprint
    >>> from libldap import LDAP, LDAPControl, LDAP_CONTROL_PASSWORDPOLICYREQUEST
    >>> c = LDAPControl()
    >>> c.add_control(LDAP_CONTROL_PASSWORDPOLICYREQUEST)
    >>> ld = LDAP('ldap://localhost')
    >>> msgid = ld.bind('cn=master,dc=example,dc=com', 'secret', controls=c, async=True)
    >>> result = ld.result(msgid, controls=c)
    >>> pprint(result)
    {'error_message': None,
     'message': 'Invalid credentials',
     'ppolicy_expire': -1,
     'ppolicy_grace': -1,
     'ppolicy_msg': 'Account locked',
     'referrals': [],
     'return_code': 49}

unbind
------

This is the method for LDAP unbind operation. This terminates the current association,
and free the resources.

.. code::

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.unbind()

search
------

This is the method for LDAP search operation. Required parameter is *base*.

For example:

.. code::

    >>> from pprint import pprint
    >>> from libldap import LDAP, LDAP_SCOPE_SUB
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> entries = ld.search('dc=example,dc=com', LDAP_SCOPE_SUB, '(|(uid=user1)(uid=user2))')
    >>> pprint(entries)
    [{'cn': ['user1'],
      'dn': ['uid=user1,ou=Users,dc=example,dc=com'],
      'gidNumber': ['100'],
      'givenName': ['ONE'],
      'homeDirectory': ['/home/user1'],
      'loginShell': ['/bin/bash'],
      'objectClass': ['inetOrgPerson', 'posixAccount', 'pwdPolicy'],
      'pwdAttribute': ['userPassword'],
      'sn': ['USER'],
      'uid': ['user1'],
      'uidNumber': ['1001'],
      'userPassword': ['secret']},
     {'cn': ['user2'],
      'dn': ['uid=user2,ou=Users,dc=example,dc=com'],
      'gidNumber': ['100'],
      'givenName': ['TWO'],
      'homeDirectory': ['/home/user2'],
      'loginShell': ['/bin/bash'],
      'mail': ['user2@example.com'],
      'objectClass': ['top', 'person', 'posixAccount', 'inetOrgPerson'],
      'sn': ['User'],
      'uid': ['user2'],
      'uidNumber': ['1000'],
      'userPassword': ['{SSHA}6ggrZqsOKRkj3wbBp/GB4tMpbgi+l2JLs3oWCA==']}]

Each entry is dict type and value type is list. **dn** attribute is also included
in entry object.

You can only specified attributes by **attributes** parameter. If `*` or None are
specified, all attributes are fetched. **attrsonly** parameter fetchs attribute names
only (value is empty list).

You can specify **timeout** and **sizelimit** parameter. See ldap.conf(5).

**controls** parameter can be set. Following is LDAP_CONTROL_SORTREQUEST example:

Although LDAP client MUST NOT expect attributes order will be fixed,
you can get ordered attributes by **ordered_attributes** parameter.

search() method support LDAP_CONTROL_SORTREQUEST. You can use like this:

.. code::

    >>> from pprint import pprint
    >>> from libldap import LDAP, LDAPControl, LDAP_CONTROL_SORTREQUEST
    >>> c = LDAPControl()
    >>> c.add_control(LDAP_CONTROL_SORTREQUEST, b'uidNumber')
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> entries = ld.search('dc=example,dc=com', LDAP_SCOPE_SUB,
    ...                     '(|(uid=user1)(uid=user2))', attributes=['uidNumber'],
    ...                     controls=c)
    >>> pprint(entries)
    [{'dn': ['uid=user2,ou=Users,dc=example,dc=com'], 'uidNumber': ['1000']},
     {'dn': ['uid=user1,ou=Users,dc=example,dc=com'], 'uidNumber': ['1001']}]

paged_search
-------------

This is the method for LDAP search operation with LDAP_CONTROL_PAGEDRESULTS.
Of course, you can use LDAP_CONTROL_PAGEDRESULTS with search_() method, but
paged_search() is generator.

.. code::

    >>> from libldap import LDAP, LDAP_SCOPE_SUB
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> entries = ld.paged_search('dc=example,dc=com', LDAP_SCOPE_SUB)
    >>> entries
    <generator object paged_search at 0x7f8d8714fa20>

LDAPControl
===========

You can LDAP control extension by using this class.

For example:

.. code::

    >>> from libldap import LDAP, LDAPControl, LDAP_CONTROL_RELAX
    >>> c = LDAPControl()
    >>> c.add_control(LDAP_CONTROL_RELAX)
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.modify('cn=test,dc=example,dc=com',
    ...           [('pwdAccountLockedTime', [], LDAP_MOD_DELETE)], controls=c)
    >>> 
"""

from .core import *
from .constants import *

# vi: set filetype=rst :
