from setuptools import setup, find_packages
import os
import siteinfo

setup(
    author="Maik Lustenberger",
    name='django-siteinfo',
    license = 'BSD',
    url = 'http://github.com/divio/django-siteinfo',
    version=siteinfo.__version__,
    description='django site meta info app',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    platforms=['OS Independent'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'Django>=1.2.0',
        'django-filer>=0.8',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False
)