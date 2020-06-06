import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fourth",
    version="0.0.1",
    author="Lincoln Puzey",
    description="A datetime library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LincolnPuzey/Fourth",
    license="MIT License",
    packages=["fourth"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    keywords=["fourth four 4 datetime time date timezone"],
)
