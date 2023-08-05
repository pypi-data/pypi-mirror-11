/*
 * A Python binding for libldap.
 *
 * Copyright (C) 2015 Yutaka Kamei
 *
 */

#include "libldap.h"


PyObject *
LDAPObject_whoami(LDAPObject *self, PyObject *args)
{
	int msgid;
	int rc;

	LDAP_BEGIN_ALLOW_THREADS
	rc = ldap_whoami(self->ldap, NULL, NULL, &msgid);
	LDAP_END_ALLOW_THREADS
	if (rc != LDAP_SUCCESS) {
		PyErr_SetString(LDAPError, ldap_err2string(rc));
		return NULL;
	}

	/* NOTE: Result of this operation returns {'data': 'user', 'data_length': 4}
	 *       "data_length == 0" means anonymous user
	 */

	return PyLong_FromLong(msgid);
}

/* vi: set noexpandtab : */
