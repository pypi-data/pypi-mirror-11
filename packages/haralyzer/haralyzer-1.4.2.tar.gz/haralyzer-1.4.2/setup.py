#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


install_reqs = ['cached-property',
                'numpy',
                'python-dateutil', ]

readme = open('README.rst').read()

setup(
    name='haralyzer',
    version='1.4.2',
    description='A python framework for getting useful stuff out of HAR files',
    long_description=readme,
    author='Justin Crown',
    author_email='justincrown1@gmail.com',
    url='https://github.com/mrname/haralyzer',
    download_url='https://github.com/mrname/haralyzer/tarball/1.0',
    packages=[
        'haralyzer'
    ],
    package_dir={'haralyzer': 'haralyzer'},
    install_requires=install_reqs,
    license='Commercial',
    zip_safe=False,
    keywords='har',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
