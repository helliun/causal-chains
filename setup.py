import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="causal_chains",
    version="1.0.13",
    author="Henry Leonardi",
    author_email="leonardi.henry@gmail.com",
    description="A package for extracting causal chains from text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/helliun/causal-chains",
    packages=["causal_chains"],#setuptools.find_packages(),
    #py_modules = ["src/causal_chains"],
    install_requires = ["hatchling","transformers","sentence-transformers","pydot","tqdm"]
,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)