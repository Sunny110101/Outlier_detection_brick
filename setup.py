from setuptools import setup, find_packages

setup(
    name="outlier_detection",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "PyYAML>=6.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "kfp>=1.8.14",
        ],
    },
    python_requires=">=3.8",
)