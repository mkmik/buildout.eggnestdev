# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.4'
name = 'buildout.eggnestdev'


long_description = (
    read('README.txt')
    + '\n' + 
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '======================\n'
    + '\n' +
    read('buildout', 'eggnestdev', 'eggnest.txt')
    )

entry_point = '%s.eggnest:install' % name
entry_points = {"zc.buildout.extension": ["default = %s" % entry_point]}

tests_require=['zc.buildout']

setup(name=name,
      version=version,
      description="buildout extension to auto load eggs",
      long_description=long_description,
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      license='GPL',
      keywords='buildout extension auto load',
      author='Marko Mikulicic',
      author_email='mmikulicic@gmail.com',
      url='http://pypi.python.org/pypi/'+name,
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['buildout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'buildout.eggnestdev.tests.test_suite',
      entry_points=entry_points,
      )

