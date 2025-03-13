from setuptools import setup, find_packages

setup(
    name="netviewer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PySide6>=6.0.0",
    ],
    python_requires=">=3.8",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Michael",
    author_email="netviewer@mapledyne.com",
    description="A network visualization tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mapledyne/netviewer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
) 