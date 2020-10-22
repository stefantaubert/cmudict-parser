from setuptools import setup, find_packages

setup(
    name='cmudict_parser',
    version='1.0.0',
    url='https://github.com/stefantaubert/cmudict-parser.git',
    author='Stefan Taubert',
    author_email='stefan.taubert@posteo.de',
    description='Python parser for CMUDict files. It returns ARBAbet and IPA transciption of dictionary words.',
    packages=["cmudict_parser"],
    install_requires=["tqdm", "wget"],
)