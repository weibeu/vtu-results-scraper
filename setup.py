import re
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def __get_version():
    with open("vtu_captcha/__init__.py") as file:
        return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)


def __get_requirements():
    with open("requirements.txt") as file:
        return file.readlines()


requirements = __get_requirements()
version = __get_version()
setuptools.setup(
    name="vtu-results-scraper",
    version=version,
    author="Weibeu",
    author_email="deepakrajko14@gmail.com",
    description="VTU captcha solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weibeu/vtu-results-scraper",
    project_urls={
        "Bug Tracker": "https://github.com/weibeu/vtu-results-scraper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=requirements,
)
