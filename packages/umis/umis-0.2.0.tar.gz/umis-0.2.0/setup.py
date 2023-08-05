import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name='umis',
        version='0.2.0',
        description='Package for estimating UMI counts in Transcript Tag Counting data.',
        packages=find_packages(),
        install_requires=['click', 'pysam>=0.8.3', 'pandas'],
        entry_points = {
            'console_scripts': ['umis=umis:umis']
        },
        url='https://github.com/vals/umis',
        author='Valentine Svensson',
        author_email='valentine@nxn.se',
        long_description=read('README.md'),
        package_data = {
        '': ['examples/*/*.json']
        }
    )
