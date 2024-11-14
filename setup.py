# setup.py
from setuptools import setup, find_packages

setup(
    name="worktime",
    version="0.1",
    packages=find_packages(),
    description="Time measuring tool for work",
    long_description=open("README.md").read(),  # Long description from README file
    long_description_content_type="text/markdown",
    author="Taiho Lee",
    author_email="basta@opentutorials.org",
    url="https://github.com/o2-basta/worktime",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: CC BY 4.0",  # License type (in this case a CC license)
        "Operating System :: OS Independent",
    ],
    scripts=["worktime/worktime.py"],
    entry_points={
        "console_scripts": [
            "worktime=worktime:main",
        ],
    },
    python_requires=">=3.6",
)
