from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f::
    long_description = f.read()

setup(
    name="bitstamp-websocket-client",
    version="2016.10",
    description="Client for the Bitstamp.net websocket API",
    url="https://github.com/bartbroere/bitstamp-python-websocket-client/",
    author="Bart Broere",
    author_email="mail@bartbroere.eu",
    license="MIT",
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Intended Audience :: Developers",
                 "Topic :: Internet",
                 "License :: OSI Approved :: MIT License",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.5",],
    keywords="bitstamp bitstamp.net websocket python client pusher bitcoin exchange",
    packages=["bitstamp"], #TODO try whether this is allowed, or collides with the HTTP version of the Bitstamp client
    install_requires=["pythonpusherclient"], #TODO: or start own branch if changes not published
)
