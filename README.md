# cmudict-parser: ARPAbet and IPA for CMUDictionary

Python parser for [CMUDict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) files. It returns ARBAbet and IPA transciption of dictionary words.

## Installation

```sh
pip install --user pipenv --python 3.7
pipenv install --ignore-pipfile
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
pip install --user pipenv --python 3.7
pipenv install --dev
```

### Add to other project

In the destination project run:

```sh
# if not already done:
pip install --user pipenv --python 3.7
# add reference
pipenv install -e git+git@github.com:stefantaubert/cmudict-parser.git@master#egg=cmudict_parser
```

## Notes

- https://github.com/prosegrinder/python-cmudict Version 0.4.4. is newer than 0.7b!
  - has for example 'declarative' but is GPL!
  - 
- https://github.com/cmusphinx/cmudict Version 0.4.4.
