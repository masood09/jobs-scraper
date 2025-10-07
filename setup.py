from setuptools import find_packages, setup

setup(
    name="jobscraper",
    version="0.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "Flask==2.3.3",
        "pandas",
    ],
    extras_require={
        "dev": [
            "pytest==8.4.2",
            "pytest-cov==4.1.0",
            "flake8==6.1.0",
            "black==23.9.1",
            "isort==5.12.0",
            "python-dotenv==1.0.0",
            "testfixtures==7.1.0",
        ],
    },
    python_requires=">=3.9",
)
