from setuptools import setup

__author__ = 'Fredrik Gjertsen'
__doc__ = open('README.rst').read()
__description__ = 'typesys is a python module meant to make it easier to manange types'

setup(name='typesys',
      version='0.2.9',
      description=__description__,
      long_description=__doc__,
      author=__author__,
      author_email='f.gjertsen@gmail.com',
      url='https://github.com/fredgj/typesys',
      packages=['typesys'],
      license='MIT',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: Implementation :: CPython',
                   'Topic :: Utilities'
                  ],
      keywords='types, type hints, type hinting, type correction, typesystem, typesys')
