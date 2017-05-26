from pip.req import parse_requirements
import uuid
import versioneer
from setuptools import setup, find_packages

requirements = parse_requirements('requirements.txt', session=uuid.uuid1())
install_requires = [str(r.req) for r in requirements]
description = """
    nflex-connector-utils provides a suite of tools to produce data
    structures when implementing resources connector nflex modules."""

long_description = """
nflex-connector-utils provides a suite of tools to produce data structures
when implementing resources connector nflex modules.
See readthedocs_ for the documentation and github_ for the source.

.. _github: https://github.com/ntt-nflex/nflex_connector_utils
.. _readthedocs: http://nflex-connector-utils.readthedocs.io/en/latest/index.html
"""  # noqa

setup(
    name="nflex-connector-utils",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
