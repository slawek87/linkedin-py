# -*- coding: utf-8 -*-
from distutils.core import setup

try:
    with open('README.md', 'r') as f:
        readme = f.read()

    with open('LICENSE.txt', 'r') as f:
        license_ = f.read()
except:
    readme = ''
    license_ = ''

setup(
    name='linkedin-py',
    version='1.0.1',
    packages=['linkedin_py', 'linkedin_py.authentication', 'linkedin_py.authorization', 'linkedin_py.endpoints'],
    url='',
    download_url='https://github.com/slawek87/linkedin-py',
    license=license_,
    author=u'Sławomir Kabik',
    author_email='slawek@redsoftware.pl',
    description='Linkedin-py provides an easy-to-use Python interface for handle Linkedin API requests.',
    long_description=readme,
    keywords=['Python Linkedin', 'Linkedin API', 'Python Linkedin requests', 'Linkedin Python Lib', 'Python Linkedin endpoints'],
    install_requires=['setuptools', 'requests'],
)
