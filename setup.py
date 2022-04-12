#!/usr/bin/env python3.6

from setuptools import find_packages, setup

setup(
    name="bloodhound-analyzer",
    version="0.0.9",
    description="Analyze BloodHound data & generate csv reports",
    url="https://github.com/CERN-CERT/bloodhound-analyzer.git",
    author="CERN Computer Security Team",
    license="GPL3",
    keywords=[
        "CLI",
        "BH",
        "Bloodhound",
        "Sharphound",
        "reports",
        "Active",
        "Directory",
    ],
    packages=find_packages(),
    scripts=["bloodhound-analyzer"],
)
