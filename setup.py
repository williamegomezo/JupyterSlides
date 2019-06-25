import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='JupyterHTMLSlides',
    version='1.0.2',
    author="William Gomez",
    author_email="williamegomezo@gmail.com",
    description="Create slides for your jupyter presentation using HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williamegomezo/JupyterSlides",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
