import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ciboulette-pkg-Touzan-Dominique", # Replace with your own username
    version="0.0.1",
    author="Touzan Dominique",
    author_email="dtouzan@gmail.com",
    description="Ciboulette package for astronomy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dtouzan/ciboulette",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
