"""
Remarks:
https://github.com/cmusphinx/cmudict is newer than 0.7b! It has for example 'declarative' but is has unfortunately no MIT-license.
"""

import string
from string import punctuation
from typing import Callable, Dict, List, Optional, Union
from unittest.case import skip

from tqdm import tqdm

from cmudict_parser.ARPAToIPAMapper import get_ipa_with_stress
from cmudict_parser.CMUDictDownloader import ensure_files_are_downloaded
from cmudict_parser.CMUDictParser import parse


class CMUDict():
  def __init__(self):
    self._loaded = False

  def _load(self, dictionary_dir: str, silent: bool) -> None:
    self._loaded = False
    paths = ensure_files_are_downloaded(dictionary_dir)
    entries = parse(paths, silent)

    self._entries_arpa = entries
    self._entries_ipa = self._convert_to_ipa(silent)
    self._entries_first_ipa = self._extract_first_ipa()
    self._loaded = True

  def _ensure_data_is_loaded(self) -> None:
    if not self._loaded:
      raise Exception("Please load the dictionary first.")

  def _extract_first_ipa(self) -> Dict[str, str]:
    result: Dict[str, str] = {word: ipas[0] for word, ipas in self._entries_ipa.items()}
    return result

  def _convert_to_ipa(self, silent: bool) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {word: [] for word, _ in self._entries_arpa.items()}
    items = self._entries_arpa.items() if silent else tqdm(self._entries_arpa.items())
    for word, pronunciations in items:
      for pronunciation in pronunciations:
        phonemes = pronunciation.split(' ')
        ipa_phonemes = [get_ipa_with_stress(phoneme) for phoneme in phonemes]
        ipa = ''.join(ipa_phonemes)
        result[word].append(ipa)

    return result

  def contains(self, word: str) -> bool:
    self._ensure_data_is_loaded()
    result = word.upper() in self._entries_arpa.keys()
    return result

  def sentence_to_ipa(self, sentence: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
    if replace_unknown_with is not None and isinstance(replace_unknown_with, str) and len(replace_unknown_with) >= 2:
      raise Exception("Parameter replace_unknown_with can only be 0 or 1 char.")
    words = sentence.split(" ")
    ipa_words = []
    for word in words:
      ipa = self.get_ipa_of_word_in_sentence(word, replace_unknown_with)
      ipa_words.append(ipa)
    res = " ".join(ipa_words)
    return res

  def get_ipa_of_word_in_sentence(self, word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
      if any(char in string.punctuation for char in word):
        ipa = self.get_ipa_of_words_with_punctuation(word, replace_unknown_with)
      else:
        ipa = self.get_ipa_of_word_in_sentence_without_punctuation(word, replace_unknown_with)
      return ipa

  def get_ipa_of_words_with_punctuation(self, word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
    if word == "":
      return ""
    punctuations_before_word=""
    while word[0] in string.punctuation:
      punctuations_before_word = punctuations_before_word + word[0]
      word = word[1:]
      if word == "":
        break
    if word != "":
      auxiliary_word = word
      word_without_punctuation = ""
      while auxiliary_word[0].isalpha() or auxiliary_word[0]=="'" or auxiliary_word[0]=="'":
        word_without_punctuation = word_without_punctuation + auxiliary_word[0]
        auxiliary_word = auxiliary_word[1:]
        if auxiliary_word == "":
          break
      char_at_end = ""
      if word_without_punctuation[-1] == "-" or word_without_punctuation[-1] == "'":
        char_at_end = word_without_punctuation[-1]
        word_without_punctuation = word_without_punctuation[:-1]
      if self.contains("'" + word_without_punctuation) and punctuations_before_word[-1] == "'":
        punctuations_before_word = punctuations_before_word[:-1]
        ipa_of_word_without_punct = self.get_ipa_of_word_in_sentence_without_punctuation("'" + word_without_punctuation, replace_unknown_with) + char_at_end
      elif self.contains(word_without_punctuation + "'") and char_at_end == "'":
        ipa_of_word_without_punct = self.get_ipa_of_word_in_sentence_without_punctuation(word_without_punctuation + "'", replace_unknown_with)
      else:
        ipa_of_word_without_punct = self.get_ipa_of_word_in_sentence_without_punctuation(word_without_punctuation, replace_unknown_with) + char_at_end
      ipa = f"{punctuations_before_word}{ipa_of_word_without_punct}{self.get_ipa_of_words_with_punctuation(auxiliary_word, replace_unknown_with)}"
    else:
      ipa = punctuations_before_word
    return ipa

  def get_ipa_of_word_in_sentence_without_punctuation(self, word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
    ipa = ""
    if word != "":
      if self.contains(word):
        ipa = self.get_first_ipa(word)
      elif word.isupper():
        for char in word:
          ipa = ipa + self.get_first_ipa(char)
      else:
        if replace_unknown_with is None:
          ipa = word
        else:
          if isinstance(replace_unknown_with, str):
            ipa = len(word) * replace_unknown_with#f"{len(word) * replace_unknown_with}"
          else:
            ipa = replace_unknown_with(word)
    return ipa

  def get_first_ipa(self, word: str) -> str:
    self._ensure_data_is_loaded()
    return self._entries_first_ipa[word.upper()]

  def get_all_ipa(self, word: str) -> List[str]:
    self._ensure_data_is_loaded()
    return self._entries_ipa[word.upper()]

  def get_all_arpa(self, word) -> List[str]:
    '''Returns list of ARPAbet pronunciations of the given word.'''
    self._ensure_data_is_loaded()
    return self._entries_arpa[word.upper()]

  def __len__(self) -> int:
    return len(self._entries_arpa)


def get_dict(download_folder: str = "/tmp", silent: bool = False) -> CMUDict:
  result = CMUDict()
  result._load(download_folder, silent)
  return result
