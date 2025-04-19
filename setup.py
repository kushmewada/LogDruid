from setuptools import setup, find_packages

setup(
    name="log_druid",
    version="0.1.0",
    description="colored Logs.",
    author="Kush Mewada",
    author_email="kushmewada18@gmail.com",
    packages=find_packages(),  # Automatically find all packages in the folder
    install_requires=[],       # List dependencies here, e.g., ["requests", "numpy"]
    python_requires=">=3.11",
)
