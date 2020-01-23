#!/usr/bin/env python3
"""Setup."""

from decimal import Decimal
from distutils.cmd import Command
from setuptools import setup, find_packages
from setuptools.command.install import install
from typing import List, Tuple
import os
import sys


VERSION = '2.15.3'


# From https://circleci.com/blog/continuously-deploying-python-packages-to-pypi-with-circleci/
class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')
        tag_formatted_version = f'v{VERSION}'

        if tag != tag_formatted_version:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


class CoverageRatchetCommand(Command):
    description = 'Run coverage ratchet'
    user_options: List[Tuple[str, str, str]] = [
    ]

    def initialize_options(self) -> None:
        """Set default values for options."""
        self.coverage_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'metrics',
            'coverage_high_water_mark'
        )

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        """Run command."""
        import xml.etree.ElementTree as ET

        tree = ET.parse("coverage.xml")
        new_coverage = Decimal(tree.getroot().attrib["line-rate"]) * 100

        if not os.path.exists(self.coverage_file):
            with open(self.coverage_file, 'w') as f:
                f.write('0')

        with open(self.coverage_file, 'r') as f:
            high_water_mark = Decimal(f.read())

        if new_coverage < high_water_mark:
            raise Exception(
                f"Coverage used to be {high_water_mark}; down to "
                f"{new_coverage}%.  Fix by viewing 'cover/index.html'")
        elif new_coverage > high_water_mark:
            with open(self.coverage_file, 'w') as f:
                f.write(str(new_coverage))
            print(f"Just ratcheted coverage up to {new_coverage}%")
        else:
            print(f"Code coverage steady at {new_coverage}%")


setup(name='db_facts',
      version=VERSION,
      description='Database connection configuration manager',
      author='Vince Broz',
      author_email='vince.broz@bluelabs.com',
      packages=find_packages(),
      package_data={"db_facts": ["py.typed"]},
      install_requires=['jinja2', 'pyyaml'],
      entry_points={
        'console_scripts': [
            'db_facts = db_facts.__main__:main'
        ],
        "db_facts.jinja_contexts": [
            'base64 = db_facts.base64_jinja_context:pull_base64_jinja_context',
            'env = db_facts.env_jinja_context:pull_env_jinja_context',
        ]
      },
      cmdclass={
          'coverage_ratchet': CoverageRatchetCommand,
          'verify': VerifyVersionCommand,
      },
      scripts=['bin/db-facts'],
      )
