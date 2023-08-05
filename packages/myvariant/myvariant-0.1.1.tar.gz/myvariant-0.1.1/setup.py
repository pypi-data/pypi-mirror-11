import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="myvariant",
    version="0.1.1",
    author="Chunlei Wu",
    author_email="cwu@scripps.edu",
    description="Python Client for MyVariant.Info services.",
    license="BSD",
    keywords="biology variant annotation web service client api myvariant",
    url="https://github.com/Network-of-BioThings/myvariant.py",
    packages=['myvariant'],
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    install_requires=[
        'requests>=2.3.0',
    ],
)
