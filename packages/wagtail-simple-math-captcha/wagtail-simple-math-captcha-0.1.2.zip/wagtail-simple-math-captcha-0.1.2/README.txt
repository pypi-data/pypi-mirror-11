Wagtail SimpleMathCaptcha
=========================

A simple math captcha field for Wagtail Form Pages based on Django Simple Math Captcha.
---------------------------------------------------------------------------------------

wagtail-simple-math-captcha provides a way to integrate
`django-simple-math-captcha <https://pypi.python.org/pypi/django-simple-math-captcha>`__
in a Wagtail form. The code is based on
`wagtailsweetcaptcha <https://github.com/jordij/wagtailsweetcaptcha>`__

Installation
------------

1. Install ``wagtail-simple-math-captcha``.
2. Add ``wagtailsimplemathcaptcha`` to ``INSTALLED_APPS`` in your
   ``settings.py``.

Usage
-----

When you install ``wagtail-simple-math-captcha`` you won't get a captcha
field in the available field types in the form builder. To use it you
need to subclass either ``MathCaptchaForm`` or ``MathCaptchaEmailForm``
(replacements for ``AbstractForm`` and ``AbstractEmailForm``
respectively). After you do that the captcha field will appear in your
frontend:

.. code:: python

    from modelcluster.fields import ParentalKey
    from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
        MultiFieldPanel)
    from wagtail.wagtailcore.fields import RichTextField
    from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField

    from wagtailsimplemathcaptcha.models import MathCaptchaEmailForm

    class FormField(AbstractFormField):
        page = ParentalKey('FormPage', related_name='form_fields')

    class FormPage(MathCaptchaEmailForm):
        intro = RichTextField(blank=True)
        thank_you_text = RichTextField(blank=True)
        
        # wagtail-simple-math-captcha configuration
        captcha_label = ""
        captcha_help_text = "Answer this question to prove you're human."

    FormPage.content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email")
    ]

You can configure the field's ``verbose_name`` and ``help_text``
properties by including ``captcha_label`` and ``captcha_help_text``
properties in the class or overriding ``get_captcha_label()`` and
``get_captcha_help_text()`` methods:

.. code:: python

    from modelcluster.fields import ParentalKey
    from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
        MultiFieldPanel)
    from wagtail.wagtailcore.fields import RichTextField
    from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField

    from wagtailsimplemathcaptcha.models import MathCaptchaEmailForm

    class FormField(AbstractFormField):
        page = ParentalKey('FormPage', related_name='form_fields')

    class FormPage(MathCaptchaEmailForm):
        intro = RichTextField(blank=True)
        thank_you_text = RichTextField(blank=True)
        
        # wagtail-simple-math-captcha configuration
        def get_captcha_label(self):
            return ""
        
        def get_captcha_help_text(self):
            return "Answer this question to prove you're human."

    FormPage.content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email")
    ]

The defaults for both ``captcha_label`` and ``captcha_help_text`` is
emty string.
