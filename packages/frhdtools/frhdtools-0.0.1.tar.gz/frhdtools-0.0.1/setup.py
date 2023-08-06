#setup.py - Free Rider HD Installation script
#by maxmillion18
#http://www.github.com/maxmillion18
#http://www.freeriderhd.com/u/MaxwellNurzia

from setuptools import setup, find_packages

setup(name="frhdtools",
    version="0.0.1",
    description="Library to work with Free Rider HD Tracks",
    long_description="Frhdtools is a library for working with Free Rider HD Tracks.",
    url="https://github.com/maxmillion18/frhdtools",
    author="maxmillion18",
    author_email="icantpostmyemailhere@gmail.com",
    license="MIT License",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
    ],
    keywords="development freeriderhd freerider code track tracks",
    packages=find_packages(exclude=["images"])
)
