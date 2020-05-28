# cmudict-parser: ARPAbet and IPA for CMUDictionary

Python parser for [CMUDict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) files.
It returns ARBAbet and IPA transciption of dictionary words.

## Installation

`pip install -r requirements.txt`

## Usage

``` python
from src.CMUDict import get_dict

cmudict = get_dict()

print(cmudict.get_all_arpa("to"))
# ['T UW1', 'T IH0', 'T AH0']

print(cmudict.get_all_ipa("to"))
# ['tˈu', 'tɪ', 'tʌ']

print(cmudict.get_first_ipa("to"))
# tˈu
```