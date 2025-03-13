from setuptools import setup, find_packages

setup(
    name="netviewer",
    version="0.1.0",  # We'll add back SCM versioning later
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "diagnostics",
        "PySide6>=6.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A network visualization tool using diagnostics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/netviewer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 