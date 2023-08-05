Django LastPass SAML authenticator
----------------------------------

This is a hacky extension to `django-saml-service-provider`_ that, instead
of onelogin, uses `LastPass Enterprise`_ as an IdP. 

.. _`django-saml-service-provider`: 
    https://github.com/KristianOellegaard/django-saml-service-provider
.. _`LastPass Enterprise`: https://lastpass.com/enterprise_overview.php

Installation
============

Get it from PyPI::

    pip install django-lastpass-sp

Example configuration
=====================

::

    # Check the LastPass SAML metadata for the bits after '.../login/'
    LASTPASS_CONNECTOR_ID = '1234567/abc4'

    # This is the certificate given by LastPass
    # or LASTPASS_CERTIFICATE if you want the cert in your conf
    LASTPASS_CERTIFICATE_FILE = os.path.join(BASE_DIR, 'lastpass.crt')

    # Private key, try it like this:
    # openssl genrsa > samlsp.key
    # or SAML_SP_KEY if you want the key in your conf
    SAML_SP_KEY_FILE = os.path.join(BASE_DIR, 'samlsp.key')

    # Certificate, try with self-signed:
    # openssl req -new -x509 -key samlsp.key -out samlsp.crt -days 365
    # or SAML_SP_CERTIFICATE if you want the key in your conf
    SAML_SP_CERTIFICATE_FILE = os.path.join(BASE_DIR, 'samlsp.crt')

    # Optional!
    # Contact info provided in the metadata
    SAML_SP_CONTACT_INFO = {
        "technical": {
            "givenName": "Admin",
            "emailAddress": "admin@example.com",
        }
    }

    # Optional! 
    # Ditto for organization info
    SAML_SP_ORGANIZATION_INFO = {
        "en-US": {
            "name": "acme",
            "displayname": 'Acme Inc',
            "url": "http://example.com/",
        }
    }

    AUTHENTICATION_BACKENDS = (
        # This is just so you don't block yourself out
        #'django.contrib.auth.backends.ModelBackend',
        # This is the beef
        'sp.auth_backend.SAMLServiceProviderBackend',
    )

    # Optional
    # Create new users with admin and/or staff accounts
    # Both default to False
    LASTPASS_CREATE_ADMIN = True
    LASTPASS_CREATE_STAFF = True


