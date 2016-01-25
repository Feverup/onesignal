
from setuptools import find_packages
from distutils.core import setup

setup(
    name = 'OneSignalSDK',
    packages=find_packages(exclude=['tests*']), # this must be the same as the name above
    version = '0.1',
    description = 'A Python SDK for OneSignal (http://onesignal.com)',
    author = 'Waqas Younas',
    author_email = 'waqas.younas@gmail.com',
    url = 'https://github.com/gettalent/one-signal-python-sdk', # use the URL to the github repo
    keywords = ['onesignal', 'onesignalsdk', 'sdk'], # arbitrary keywords
    install_requires=[
        'requests',
        'pytest'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
    ]
)