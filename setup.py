import os
import sys
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
requirements = ['httplib2',]

setup(
    name = "python_zipcodes",
    version = "0.0.2",
    description = "",
    long_description = read('README.rst'),
    url = 'https://github.com/fcurella/python_zipcodes',
    license = 'BSD',
    author = 'Flavio Curella',
    author_email = 'flavio.curella@curella.org',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = requirements,
    tests_require = ["nose",],
    test_suite = "nose.collector",
)
