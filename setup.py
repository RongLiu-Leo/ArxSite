from setuptools import setup, find_packages

setup(
    name="arxsite",
    version="0.2.2",
    description="Generate a Jekyll project website from an arXiv paper",
    author="Rong Liu",
    url="https://github.com/RongLiu-Leo/arxsite",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "arxsite": ["templates/*", "*"],
    },
    install_requires=[
        "requests",
        "jinja2",
        "nltk",
    ],
    entry_points={
        "console_scripts": [
            "arxsite=arxsite.cli:main",
        ],
    },
    python_requires=">=3.9",
)
