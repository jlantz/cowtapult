from setuptools import setup, find_packages
import sys, os

version = '0.1a1'

# -*- Classifiers -*-

classes = """
    Development Status :: 5 - Production/Stable
    License :: OSI Approved :: BSD License
    Topic :: System :: Distributed Computing
    Topic :: Software Development :: Object Brokering
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.6
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.2
    Programming Language :: Python :: 3.3
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Programming Language :: Python :: Implementation :: Jython
    Operating System :: OS Independent
    Operating System :: POSIX
    Operating System :: Microsoft :: Windows
    Operating System :: MacOS :: MacOS X
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

setup(name='cowtapult',
      version=version,
      description="cowtapult",
      long_description="""\
Enterprise class infrastructure for reliably sending data from Python to Salesforce or Salesforce to Python""",
      classifiers=classifiers,
      keywords='python salesforce celery simple-salesforce',
      author='Jason Lantz',
      author_email='jason@muselab.com',
      url='http://github.com/jlantz/cowtapult',
      license='New BSD License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'celery',
        'simple-salesforce',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
