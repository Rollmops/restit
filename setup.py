import os
import re

from setuptools import setup, find_packages

with open(
        os.path.join(os.path.dirname(__file__), "restit", "__init__.py")
) as v_file:
    VERSION = (
        re.compile(r""".*__version__ = ["'](.*?)['"]""", re.S)
            .match(v_file.read())
            .group(1)
    )

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as r_file:
    readme = r_file.read()

setup(
    name="restit",
    author="Erik Tuerke",
    url="https://restit.readthedocs.io/en/latest/",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    description="HTTP REST library including OOP-readiness and Open-API generation",
    long_description=readme,
    install_requires=[
        "marshmallow",
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
