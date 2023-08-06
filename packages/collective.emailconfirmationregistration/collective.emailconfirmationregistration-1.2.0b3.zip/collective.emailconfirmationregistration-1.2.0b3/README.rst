Introduction
============

The purpose of this package is to provide an extra verification step for Plone
when self-registration is enabled.

When you install this product, before a user can register with the Plone site, they
first must verify they have a valid email address. This done by sending the user
an email with a unique verification url that includes a randomly generated code.

This is meant to be a proof-of-concept solution. There are no tests and I haven't
spent a lot of time on it.

Yes, I know very sophisticated spam bots can also automate the email verification
process. To address that, the next step for this package would be to check the email
address against database/API with a known list of bad emails/domains(if there is such a thing).

In any case, I'm hoping that this can be a decent OOTB method for protecting Plone's
self-registration setting.


Installation on plone 4.3
-------------------------
You will need to pin the version of plone.app.users to 2.1.0. plone.app.users 2.2.x is Plone 5 only.


Recaptcha Support
-----------------

This package copies the way collective.registrationcaptcha does recapcha support.

Copy of collective.registrationcaptcha documentation::

It depends on plone.app.discussion and uses it's captcha abstaction facilities.

In order to use a captcha widget, you have to install one - wether by depending on the captchawidgets extra of this package or by installing plone.formwidget.captcha, plone.formwidget.recaptcha (not functional at time of this writing) or collective.z3cform.norobots. Then you have to configure plone.app.discussion to use a captcha widget. You don't need to keep the discussion activated, if you don't want them to be active on your site.


Install with collective.registrationcaptcha
-------------------------------------------

This package will override the functionality of collective.registrationcaptcha. You might as well
remove collective.registrationcaptcha from your site when using this add-on.


Review registrations
--------------------

To turn on reviewing registrations before the user is created on the site
after the user is verified, go to the Configuration registry in
Site setup(http://site-url/portal_registry), search for "plone.review_registrations"
and enable this setting.
