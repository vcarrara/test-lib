from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as stream:
    long_description = stream.read()

setup(
    name="olympuslib",
    version="0.0.12",
    author="Namkin",
    description="Data utils library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vcarrara/test-lib",
    packages=find_packages(include=['olympuslib', 'olympuslib.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[]
)
