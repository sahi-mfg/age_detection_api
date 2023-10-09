import sys
from setuptools import find_packages, setup
from typing import List
from poetry.core.masonry.api import load


def get_requirements() -> List[str]:
    """
    this function will return the list of requirements
    """
    # Load the pyproject.toml file using Poetry's API
    pyproject = load(sys.path[0])

    # Get the list of dependencies from the pyproject.toml file
    requirements = [f"{dep.name}{dep.specifier}" for dep in pyproject.package.dependencies]

    return requirements


setup(
    name="end_to_end_ml_project",
    version="0.0.1",
    author="Sahi",
    author_email="mohamedfrancissahi@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
