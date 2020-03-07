from setuptools import setup, find_packages

from flask_rest import __version__

setup(
    name="flask-rest",
    version=__version__,
    packages=find_packages()
)
