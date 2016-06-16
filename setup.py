from setuptools import setup

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

setup(
    name='django-materialize',
    version='0.7.1',
    description='Material design for django forms and admin',
    license='BSD',
    author='Sigurd Gartmann, Jørgen Bergquist',
    author_email='sigurdga-github@sigurdga.no',
    url='http://github.com/strekmann/django-materialize',
    keywords="django",
    packages=['django_materialize',
              'django_materialize.templatetags',
              'django_materialize.admin',
              'django_materialize.admin.templatetags'],
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    install_requires=[
    ],
    classifiers=[
        'Framework :: Django',
        "Framework :: Django :: 1.9",
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
)
