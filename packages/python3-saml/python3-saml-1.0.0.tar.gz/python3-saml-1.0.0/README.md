OneLogin’s SAML Python Toolkit (python3 compatible)
===================================================

Add SAML support to your Python softwares using this library. Forget
those complicated libraries and use that open source library provided
and supported by OneLogin Inc.

This version supports Python3, exists an alternative version that only support Python2: python-saml


Why add SAML support to my software?
------------------------------------

SAML is an XML-based standard for web browser single sign-on and is
defined by the OASIS Security Services Technical Committee. The standard
has been around since 2002, but lately it is becoming popular due its
advantages:

-  **Usability** - One-click access from portals or intranets, deep
   linking, password elimination and automatically renewing sessions
   make life easier for the user.
-  **Security** - Based on strong digital signatures for authentication
   and integrity, SAML is a secure single sign-on protocol that the
   largest and most security conscious enterprises in the world rely on.
-  **Speed** - SAML is fast. One browser redirect is all it takes to
   securely sign a user into an application.
-  **Phishing Prevention** - If you don’t have a password for an app,
   you can’t be tricked into entering it on a fake login page.
-  **IT Friendly** - SAML simplifies life for IT because it centralizes
   authentication, provides greater visibility and makes directory
   integration easier.
-  **Opportunity** - B2B cloud vendor should support SAML to facilitate
   the integration of their product.

General description
-------------------

OneLogin’s SAML Python toolkit let you build a SP (Service Provider)
over your Python application and connect it to any IdP (Identity
Provider).

Supports:

-  SSO and SLO (SP-Initiated and IdP-Initiated).
-  Assertion and nameId encryption.
-  Assertion signature.
-  Message signature: AuthNRequest, LogoutRequest, LogoutResponses.
-  Enable an Assertion Consumer Service endpoint.
-  Enable a Single Logout Service endpoint.
-  Publish the SP metadata (which can be signed).

Key features:

-  **saml2int** - Implements the SAML 2.0 Web Browser SSO Profile.
-  **Session-less** - Forget those common conflicts between the SP and
   the final app, the toolkit delegate session in the final app.
-  **Easy to use** - Programmer will be allowed to code high-level and
   low-level programming, 2 easy to use APIs are available.
-  **Tested** - Thoroughly tested.
-  **Popular** - OneLogin’s customers use it. Add easy support to your
   django/flask web projects.


Installation
------------

Dependences
~~~~~~~~~~

 * python 2.7 // python 3.3
 * xmlsec Python bindings for the XML Security Library.
 * isodate An ISO 8601 date/time/duration parser and formater

Review the setup.py file to know the version of the library that python3-saml is using


Code
~~~~

Option 1. Download from github
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The toolkit is hosted on github. You can download it from:

-  Lastest release:
   https://github.com/onelogin/python3-saml/releases/latest
-  Master repo: https://github.com/onelogin/python3-saml/tree/master

Copy the core of the library (src/onelogin/saml2 folder) and merge the
setup.py inside the python application. (each application has its
structure so take your time to locate the Python SAML toolkit in the
best place).

Option 2. Download from pypi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The library is hosted in pypi, you can find the python-saml package at
https://pypi.python.org/pypi/python3-saml

You can install it executing:

::

     pip install python3-saml
