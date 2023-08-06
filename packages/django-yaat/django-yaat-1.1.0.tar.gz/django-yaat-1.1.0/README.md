# django-yaat

[![Documentation Status](https://readthedocs.org/projects/django-yaat/badge/?version=latest)](http://django-yaat.readthedocs.org/en/latest/)

This is the [django-restify-framework](https://github.com/lovasb/django-restify) resource of the 
[yaat](https://github.com/slapec/yaat) AngularJS module.

# Requirements

This module is developed in Python 3.4.2. Backwards compatibility is not guaranteed (tests are welcome).

- `Django>=1.8.4`

    Might work with older versions. I haven't tried.
    
- `django-restify-framework==0.22`

    This is the library django-yaat is built on.
    
- `django-ordered-model`

    This is required to store the order of columns of each resource (if the resource is statefull).
    
## Development requirements

`pip install -r requirements.txt`

It will also install tools for documentation generation.

## Run tests

`python runtests.py`
