from setuptools import find_packages
from distutils.core import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='onesignal',
    packages=find_packages(exclude=['tests*']),
    version='0.1',
    description='A Python wrapper for OneSignal API (http://onesignal.com)',
    long_description=readme(),
    author='Waqas Younas, Zohaib Ijaz, Ismael de Esteban',
    author_email='waqas.younas@gmail.com, mzohaib.qc@gmail.com, ismael.deesteban@gmail.com',
    url='https://github.com/gettalent/one-signal-python-sdk',
    keywords=['onesignal', 'onesignalsdk'],
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
