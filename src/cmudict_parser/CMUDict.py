"""
Remarks:
https://github.com/cmusphinx/cmudict is newer than 0.7b! It has for example 'declarative' but is has unfortunately no MIT-license.
"""

from typing import Any, Callable, Dict, List, Optional, Union

from cmudict_parser.CMUDictDownloader import ensure_files_are_downloaded
from cmudict_parser.CMUDictParser import (ARPAPronunciation,
                                          ARPAPronunciations, Word, parse)
from cmudict_parser.SentenceToIPA import sentence_to_ipa as get_ipa_of_sentence

ENG_SPACE = " "
ARPA_SPACE = " "
ARPA_UNKNOWN = "<UNK>"


def join_lists(lists: List[List[Any]], join_with: List[Any]) -> List[Any]:
  if len(lists) == 0:
    return []
  if len(lists) == 1:
    return lists[0]
  result = lists[0]
  for i in range(1, len(lists)):
    result.extend(join_with)
    result.extend(lists[i])
  return result


class CMUDict():
  def __init__(self):
    self._loaded = False

  def _load(self, dictionary_dir: str, silent: bool) -> None:
    self._loaded = False
    paths = ensure_files_are_downloaded(dictionary_dir)
    entries = parse(paths, silent)

    self._entries_arpa = entries
    self._entries_first_arpa = self._extract_first_arpa()
    self._loaded = True

  def _ensure_data_is_loaded(self) -> None:
    if not self._loaded:
      raise Exception("Please load the dictionary first.")

  def _extract_first_arpa(self) -> Dict[Word, ARPAPronunciation]:
    result: Dict[Word, ARPAPronunciation] = {
      word: arpa_pronunciations[0] for word, arpa_pronunciations in self._entries_arpa.items()
    }
    return result

  def sentence_to_arpa_old(self, sentence: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]], use_caching: bool = True) -> str:
    assert sentence is not None
    self._ensure_data_is_loaded()
    return get_ipa_of_sentence(self._entries_first_arpa, sentence, replace_unknown_with, use_caching)

  def sentence_to_arpa(self, sentence: str) -> ARPAPronunciation:
    assert isinstance(sentence, str)
    self._ensure_data_is_loaded()
    tmp = []
    for word in sentence.split(ENG_SPACE):
      if self.contains(word):
        arpa_pronunciation = self.get_first_arpa(word)
        tmp.append(arpa_pronunciation)
      else:
        tmp.append([ARPA_UNKNOWN])
    return join_lists(tmp, join_with=[ARPA_SPACE])

  def contains(self, word: Word) -> bool:
    assert isinstance(word, str)
    self._ensure_data_is_loaded()
    result = word.upper() in self._entries_arpa.keys()
    return result

  def get_first_arpa(self, word: Word) -> ARPAPronunciation:
    assert isinstance(word, str)
    self._ensure_data_is_loaded()
    result = self._entries_first_arpa.get(word.upper(), None)
    if result is None:
      raise Exception(f"The word \"{word}\" was not in the dictionary!")
    return result

  def get_all_arpa(self, word: Word) -> ARPAPronunciations:
    assert isinstance(word, str)
    '''Returns list of ARPAbet pronunciations of the given word.'''
    self._ensure_data_is_loaded()
    result = self._entries_arpa.get(word.upper(), None)
    if result is None:
      raise Exception(f"The word \"{word}\" was not in the dictionary!")
    return result

  def __len__(self) -> int:
    return len(self._entries_arpa)


def get_dict(download_folder: str = "/tmp", silent: bool = False) -> CMUDict:
  result = CMUDict()
  result._load(download_folder, silent)
  return result
