# Django CMS Contact

A contact system for [Django CMS](http://django-cms.org/).

This aplication provide an apphook and a form plugin to allow users to send a contact message.

**WARNING**: I created this to use in a personal website and future versions will have hard changes that will break backward compatibility.

## Table of contents

- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Usage](#usage)
- [Signals](#signals)
- [Templates](#templates)
- [TODO](#todo)
- [License](#license)

## Requirements

* Django 1.7
* Django CMS 3.x

## Quick start

##### 1. Install djangocms-contact:

```
pip install djangocms-contact
```

This will install the dependencies automatically.

##### 2. Add "djangocms_contact" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = (
    ...
    'cms',
    'djangocms_contact',  # You **must** add 'djangocms_contact' **after** 'cms'.
    ...
)
```

##### 3. Migrate to create the application models:

```
python manage.py migrate
```

## Usage

#### Apphook

You need to use [apphooks](http://docs.django-cms.org/en/3.1.2/how_to/apphooks.html) to integrate the application with Django CMS:

* Create a new Django CMS page
* Go to Advanced Settings and select `Contact` under "Application"
* Restart the project instance to properly load urls

This consists of a page with a contact form and a page for success message.

#### Plugin

The form plugin will be available in the CMS frontend ready for use without any additional configuration, but requires the apphook instance. You can put the plugin in any [placeholder](http://docs.django-cms.org/en/3.1.2/introduction/templates_placeholders.html).

## Signals

A `contact_new_message` signal is sent when a message was sent.

Here is an example of how to subscribe to the signal:

```
from django.dispatch import receiver
from djangocms_contanct.signals import contact_new_message

@receiver(contact_new_message)
def my_custom_receiver(sender, name, email, subject, message):
    # Your code.
```

## Templates

A `djangocms_contact/base.html` template is used for all the application templates. The templates extends a `base.html` template and the content is put in a `contact_content` block (and `contact_content` in a `base_content` block). You can override the templates to fit your needs creating a `djangocms_contact` directory in your template directory.

## TODO

* Refactor to allow creating individual and configurable forms.
* Add antispam protections.
* Add support for Django 1.8.

## License

Released under the MIT license.
