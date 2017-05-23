from pip.req import parse_requirements
from setuptools import setup, find_packages
import uuid

requirements = parse_requirements('requirements.txt', session=uuid.uuid1())
install_requires = [str(r.req) for r in requirements]
description = (
    "nflex-connector-utils provides a suite of tools to produce data "
    "structures when implementing resources connector nflex modules.")

with open('README.md') as f:
    long_description = f.read()

setup(
    name="nflex-connector-utils",
    version="0.1.2",
    description=description,
    long_description=long_description,
    url='http://www.ntt.com',
    author='NTT communications',
    licence='GNU General Public License v2 (GPLv2)',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
    ],
)
