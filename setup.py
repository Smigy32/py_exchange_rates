import pathlib
from setuptools import setup, find_packages

VERSION = "1.0.0"

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

DESCRIPTION = "A library that allows to get NBU/PrivatBank exchange rates and build a graph of their changes"

setup(
    name="py-exchange-rates",
    version=VERSION,
    author="Illia Smyhunov",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",

    packages=find_packages(),

    project_urls={
        "Source": "https://github.com/Smigy32/py_exchange_rates",
    },
)
