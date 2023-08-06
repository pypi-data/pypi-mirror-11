from setuptools import setup
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='wheelr',
    version=0.1,
    url='https://github.com/cloudify-cosmo/wheelr',
    author='Gigaspaces',
    author_email='cosmo-admin@gigaspaces.com',
    license='LICENSE',
    platforms='All',
    description='Creates Python Wheel Archives.',
    long_description=read('README.rst'),
    packages=['wheelr'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'wheelr = wheelr.wheelr:main',
        ]
    },
    install_requires=[
        "wheel==0.24.0",
        "click==4.0"
    ]
)
