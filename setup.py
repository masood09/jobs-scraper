from setuptools import find_packages, setup

setup(
    name="jobscraper",
    version="0.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "Flask==3.1.2",
        "pandas",
    ],
    extras_require={
        "dev": [
            "pytest==8.4.2",
            "pytest-cov==7.0.0",
            "flake8==7.3.0",
            "black==25.9.0",
            "isort==6.1.0",
            "python-dotenv==1.0.0",
            "testfixtures==7.1.0",
        ],
    },
    python_requires=">=3.9",
)
