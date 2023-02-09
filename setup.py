import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="causal_chains",
    version="1.0.0",
    author="Henry Leonardi",
    author_email="leonardi.henry@gmail.com",
    description="A package for targeted summarization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/helliun/causal-chains",
    packages=setuptools.find_packages(),
    install_requires=['transformers','sentence-transformers','pydot','tqdm','torch','ipython'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)