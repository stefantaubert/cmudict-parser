# cmudict-parser: ARPAbet and IPA for CMU Dictionary

![Python](https://img.shields.io/github/license/stefantaubert/cmudict-parser)
![Python](https://img.shields.io/badge/python-3.9.0-green.svg)

Python parser for [CMUDict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) files. It returns ARBAbet and IPA transciption of dictionary words.

## Installation

```sh
python3.8 -m pip install pipenv
python3.8 -m pipenv install --ignore-pipfile
```

## Usage

``` python
from cmudict_parser import get_dict

cmudict = get_dict(
    download_folder="/tmp"
)

print(cmudict.get_all_arpa("to"))
# ['T UW1', 'T IH0', 'T AH0']

print(cmudict.get_all_ipa("to"))
# ['tˈu', 'tɪ', 'tʌ']

print(cmudict.get_first_ipa("to"))
# tˈu
```

## Development

```sh
apt install python3-lib2to3
python3.8 -m pip install pipenv
python3.8 -m pipenv install --dev
```

### Add to other project

In the destination project run:

```sh
# if not already done:
python3.8 -m pip install pipenv
# add reference
python3.8 -m pipenv install -e git+https://github.com/stefantaubert/cmudict-parser.git@master#egg=cmudict_parser
```

## Notes

- https://github.com/prosegrinder/python-cmudict Version 0.4.4. is newer than 0.7b!
  - has for example 'declarative' but is GPL!
- https://github.com/cmusphinx/cmudict Version 0.4.4.
