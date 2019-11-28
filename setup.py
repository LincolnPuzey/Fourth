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
    license="GNU General Public License v3 (GPLv3)",
    packages=["fourth"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires='>=3.8',
    keywords=["fourth four 4 datetime time date timezone"],
)
