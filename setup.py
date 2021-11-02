"""
https://github.com/cloudtools/troposphere/blob/master/setup.py
https://dzone.com/articles/executable-package-pip-install
"""
import os

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def file_contents(file_name):
    """Given a file name to a valid file returns the file object."""
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(curr_dir, file_name)) as the_file:
        contents = the_file.read()
    print(contents)
    return contents


def get_version():
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    with open(curr_dir + "/toolbox/__init__.py", "r") as init_version:
        for line in init_version:
            if "__version__" in line:
                return str(line.split("=")[-1].strip(" ")[1:-2])


setup(
    name="toolbox",
    version="1.0.0",
    author="mdalvi",
    author_email="milind.dalvi@turingequations.com",
    description="A toolbox of common functions used in various data science with python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdalvi/toolbox",
    license="MIT",
    packages=[
        'toolbox',
        'toolbox.pandas',
        'toolbox.preprocessing'
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.5',
    install_requires=file_contents("requirements.txt"),
    test_suite="tests",
)
