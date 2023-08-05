# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from aldryn_jobs import __version__

REQUIREMENTS = [
    'South<1.1,>=1.0.2',
    'aldryn-apphooks-config>=0.1.3',
    'django-bootstrap3',
    'django-emailit',
    'django-parler',
    'django-standard-form',
    'djangocms-text-ckeditor>= 1.0.10',
    'aldryn-boilerplates',
    'aldryn-common>=0.0.4',
    'aldryn-reversion>=0.1.0',
    'aldryn-translation-tools>=0.0.7',
    # aldryn categories has been added because of a migration dependency
    # which sneaked in somehow and we need it to be properly migrated
    # also it would be used in future (after a switch to this package
    # instead of aldryn-jobs' own categories).
    'aldryn-categories',
    'unidecode',
    'django-multiupload>=0.3',
    'django-sortedm2m',
    'django-admin-sortable2>=0.5.2',
]

py26 = sys.version_info >= (2, 6, 5) and sys.version_info < (2, 7, 0)
if py26:
    REQUIREMENTS += [
        'Django>1.5,<1.7',
        'ordereddict',
    ]

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.6',
    'Framework :: Django :: 1.7',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-jobs',
    version=__version__,
    description='Publish job openings on your site',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-jobs',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
    test_suite="test_settings.run",
)
