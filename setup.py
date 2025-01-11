"""
Setup script for the Habit Tracker App.

This script is used to package and distribute the Habit Tracker application.
It specifies project metadata, dependencies, and other configuration details
necessary for installation and usage.

Author: Daniela de Sousa Silva
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="habit-tracker-app",
    version="1.0.0",
    author="Daniela de Sousa Silva", 
    description="A command-line habit tracker to create, manage, and analyze daily and weekly habits.",
    url="https://github.com/sousa-daniela/oofpp_habits_project",
    packages=find_packages(include=["database", "models", "analytics", "tests", "*"]),
    classifiers=[
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "tabulate>=0.9.0",
        "pytest>=7.0.0",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "habit-tracker=app:display_main_menu",  # Allows running the app via `habit-tracker` command
        ],
    },
)