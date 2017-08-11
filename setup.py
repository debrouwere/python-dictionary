import os

from setuptools import find_packages, setup

setup(name='dictionary-helpers',
      version='0.1.0',
      description=("Utility functions for working with dictionaries."),
      #long_description=open('README.rst').read(),
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'
                    ],
      keywords='',
      author='Stijn Debrouwere',
      author_email='stijn@debrouwere.org',
      download_url='http://www.github.com/debrouwere/python-dictionary/tarball/master',
      license='ISC',
      test_suite='dictionary.tests',
      packages=find_packages(),
      requirements=[
        'vectorize',
        'num2words',
        'unicode-slugify',
      ]
      )
