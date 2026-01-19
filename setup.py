from setuptools import setup, find_packages

setup(
    name="wolern",
    version="1.0.0",
    description="Wolern Backend Application",
    author="Your Name",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    python_requires=">=3.12",
    install_requires=[
        [
            line.strip()
            for line in open("backend/requirements.txt")
            if line.strip() and not line.startswith("#")
        ]
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.23.0",
        ]
    },
)
