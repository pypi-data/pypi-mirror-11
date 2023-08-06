# -*- coding: utf-8 -*-
# Copyright (C) 2015 Yutaka Kamei
"""libldap package

**libldap** is libldap Python binding.
Following objects are exposed.

LDAP
====

This class has following LDAP operation methods.

* `__init__`_
* bind_
* unbind_
* search_
* paged_search_
* add_
* modify_
* delete_
* rename_
* compare_
* whoami_
* passwd_
* start_tls
* set_option
* get_option
* abandon
* cancel
* result
* search_result

__init__
--------

LDAP constructor receives uri parameter.
Example.

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')

LDAP class supports context manager. You can write your code like this:

    >>> from libldap import LDAP, LDAP_SCOPE_BASE
    >>> with LDAP('ldap://localhost') as ld:
    ...   ld.bind('cn=master,dc=example,dc=com', 'secret')
    ...   ld.search('dc=example,dc=com', LDAP_SCOPE_BASE)
    ...

If LDAP constructor receives bind_user and bind_password parameters
when you use context manager, LDAP instance executes bind() method automatically.
Otherwise LDAP instance is still anonymous.

    >>> from libldap import LDAP, LDAP_SCOPE_BASE
    >>> with LDAP('ldap://localhost', 'cn=master,dc=example,dc=com', 'secret') as ld:
    ...   ld.search('dc=example,dc=com', LDAP_SCOPE_BASE)
    ...

After closing **with statement**, LDAP instance executes unbind() method.

bind
-----

This is the method for LDAP bind operation. If you do not use this method,
the relative LDAP_ instance will operate anonymously.

For example:

.. code-block:: python

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')

This method supports asynchronous operation by passing async=True parameter.
Asynchronous operation returns message ID. You can use it like this:

.. code-block:: python

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

.. code-block:: python

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

.. code-block:: python

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.unbind()

search
------

This is the method for LDAP search operation. Required parameter is *base*.

For example:

.. code-block:: python

    >>> from pprint import pprint
    >>> from libldap import LDAP, LDAP_SCOPE_SUB
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> entries = ld.search('dc=example,dc=com', LDAP_SCOPE_SUB, '(|(uid=user1)(uid=user2))')
    >>> [entry.dn for entry in entries]
    ['uid=user1,ou=Users,dc=example,dc=com', 'uid=user2,ou=Users,dc=example,dc=com']
    >>> pprint(entries)
    [{'cn': [b'user1'],
      'gidNumber': [b'100'],
      'givenName': [b'ONE'],
      'homeDirectory': [b'/home/user1'],
      'loginShell': [b'/bin/bash'],
      'objectClass': [b'inetOrgPerson', b'posixAccount', b'pwdPolicy'],
      'pwdAttribute': [b'userPassword'],
      'sn': [b'USER'],
      'uid': [b'user1'],
      'uidNumber': [b'1001'],
      'userPassword': [b'secret']},
     {'cn': [b'user2'],
      'gidNumber': [b'100'],
      'givenName': [b'TWO'],
      'homeDirectory': [b'/home/user2'],
      'loginShell': [b'/bin/bash'],
      'mail': [b'user2@example.com'],
      'objectClass': [b'top', b'person', b'posixAccount', b'inetOrgPerson'],
      'sn': [b'\xe3\x83\xa6\xe3\x83\xbc\xe3\x82\xb6\xe3\x83\xbc'],
      'uid': [b'user2'],
      'uidNumber': [b'1002'],
      'userPassword': [b'{SSHA}j3mvviOTZ1Or8dtvn/PRVjX1igZFnUnp']}]



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

.. code-block:: python

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
    [{uidNumber: [b'1000']}, {uidNumber: [b'1001']}, {uidNumber: [b'1001']}]

paged_search
-------------

This is the method for LDAP search operation with LDAP_CONTROL_PAGEDRESULTS.
Of course, you can use LDAP_CONTROL_PAGEDRESULTS with search_() method, but
paged_search() is generator.

.. code-block:: python

    >>> from libldap import LDAP, LDAP_SCOPE_SUB
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> entries = ld.paged_search('dc=example,dc=com', LDAP_SCOPE_SUB)
    >>> entries
    <generator object paged_search at 0x7f8d8714fa20>

add
---

This is the method for LDAP add operation. Add method requires dn and
LDAP attributes parameters. LDAP attributes type is [(str, [str])].

Following is LDIF entry that we want to add.

::

    dn: cn=group1,ou=Groups,dc=example,dc=com
    objectClass: top
    objectClass: posixGroup
    cn: group1
    gidNumber: 100
    description Test Group 1


If you add above entry, convert into following Python code.

.. code-block:: python

    [
        ('objectClass', ['top', 'posixGroup']),
        ('cn', ['group1']),
        ('gidNumber', ['100']),
        ('description', ['Test Group 1']),
    ]


Example.

.. code-block:: python

    >>> from libldap import LDAP, LDAP_SCOPE_SUB
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.add('cn=group1,ou=Groups,dc=example,dc=com', [
    ...     ('objectClass', ['top', 'posixGroup']),
    ...     ('cn', ['group1']),
    ...     ('gidNumber', ['100']),
    ...     ('description', ['Test Group 1']),
    ... ])


modify
------

This is the method for LDAP modify operation. Modify method requires dn and
changes parameters. Changes type is [(str, [str], int)].

Following is LDIF entry that we want to modify.

::

    dn: cn=group1,ou=Groups,dc=example,dc=com
    changetype: modify
    add: memberUid
    memberUid: user1
    -
    replace: description
    description: Test Group One

If you modify above entry, convert into following Python code.

.. code-block:: python

    [
        ('memberUid', ['user1'], LDAP_MOD_ADD),
        ('description', ['Test Group One'], LDAP_MOD_REPLACE),
    ]

Example.

.. code-block:: python

    >>> from libldap import LDAP, LDAP_MOD_ADD, LDAP_MOD_REPLACE
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.modify('cn=group1,ou=Groups,dc=example,dc=com', [
    ...     ('memberUid', ['user1'], LDAP_MOD_ADD),
    ...     ('description', ['Test Group One'], LDAP_MOD_REPLACE),
    ... ])

delete
-------

This is the method for LDAP delete operation. Delete method requires dn parameter.

Example.

.. code-block:: python

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.delete('cn=group1,ou=Groups,dc=example,dc=com')

rename
------

This is the method for LDAP rename operation. Rename method requires dn and
newrdn parameters. newparent and deleteoldrdn are optional parameters. if
newparent parameter is None, newparent is same suffix with dn parameter.

Example.

.. code-block:: python

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.rename('uid=test-user,ou=Users,dc=example,dc=com', 'cn=test-user')

.. note::

    If deleteoldrdn is True, old RDN attribute will be deleted. This may cause
    'Object class violation (65)' Exception. Default deleteoldrdn value is False.


compare
--------

This is the method for LDAP compare operation. Compare method requires dn, attribute
and value parameters. It returns boolean, specified attribute description and value
to compare to those found in the entry or not.

Example.

.. code-block:: python

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.compare('cn=group1,ou=Groups,dc=example,dc=com', 'description', 'Test Group 1')
    True

whoami
------

This is the method for LDAP whoami extended operation.
If LDAP instance executes whoami() before binding, 'anonymous' string value is
returned.

Example.

.. code-block:: python

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.whoami()
    'dn:cn=master,dc=example,dc=com'

passwd
-------

This is the method for LDAP passwd extended operation.
Passwd method requires user parameter. oldpw and newpw parameters are optional.
If oldpw is None, authentication will be skipped. If newpw is None, random password
will be set.

Passwd method returns new password if succeeded.

.. code-block:: python

    >>> from libldap import LDAP
    >>> ld = LDAP('ldap://localhost')
    >>> ld.bind('cn=master,dc=example,dc=com', 'secret')
    >>> ld.passwd('uid=user3,ou=Users,dc=example,dc=com')
    'VWE4zPvT'
    >>> ld.passwd('uid=user3,ou=Users,dc=example,dc=com', 'VWE4zPvT')
    'PcMnf6uY'
    >>> ld.passwd('uid=user3,ou=Users,dc=example,dc=com', 'invalid')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/kamei/git/python-libldap/test-stage/libldap/core.py", line 624, in passwd
        raise LDAPError(**result)
    libldap.core.LDAPError: Server is unwilling to perform (53)

LDAPControl
===========

You can LDAP control extension by using this class.

For example:

.. code-block:: python

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
