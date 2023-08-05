from setuptools import setup, find_packages
import os

version = '1.0.1'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='bst.pygasus.wsgi',
      version=version,
      description="WSGI Interface for bst.pygasus framework",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'License :: OSI Approved :: Zope Public License',
          'Operating System :: OS Independent',
          'Development Status :: 4 - Beta'
      ],
      keywords='pygasus web framework extjs',
      author='codeix',
      author_email='samuel.riolo@biel-bienne.ch',
      url='https://github.com/bielbienne/bst.pygasus.wsgi',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['bst', 'bst.pygasus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Paste',
          'PasteDeploy',
          'waitress',
          'transaction'
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'console_scripts': ['serve = bst.pygasus.wsgi.server:run'],
          'paste.app_factory': ['main = bst.pygasus.wsgi.server:make_app',
                                'debug = bst.pygasus.wsgi.server:make_debug']
      },
      )
