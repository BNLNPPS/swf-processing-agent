from setuptools import setup, find_packages

setup(
    name="swf-processing-agent",
    version="0.1.0",
    description="PanDA processing agent for the ePIC streaming workflow testbed",
    author="BNL NPPS Group",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["swf-common-lib"],
    extras_require={
        "test": ["pytest>=6.0", "pytest-cov", "pytest-mock"],
    },
    python_requires=">=3.9",
)
