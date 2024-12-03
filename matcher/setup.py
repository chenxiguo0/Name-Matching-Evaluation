from setuptools import setup, find_packages

setup(
    name="matcher",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "python-Levenshtein",
        "matplotlib",
        "pytest"
    ]
)