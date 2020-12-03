from setuptools import find_packages, setup

setup(
    name="cmudict_parser",
    version="1.0.1",
    url="https://github.com/stefantaubert/cmudict-parser.git",
    author="Stefan Taubert",
    author_email="stefan.taubert@posteo.de",
    description="Python parser for CMUDict files. It returns ARBAbet and IPA transciption of dictionary words.",
    packages=["cmudict_parser"],
    install_requires=["tqdm==4.54.0", "wget==3.2"],
)
