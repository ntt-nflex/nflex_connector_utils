import versioneer
from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

install_requires = parse_requirements('requirements.txt')
description = """nflex-connector-utils provides a suite of tools to produce data structures when implementing resources connector nflex modules."""  # noqa

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
