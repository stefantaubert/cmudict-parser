"""
Remarks:
https://github.com/cmusphinx/cmudict is newer than 0.7b! It has for example 'declarative' but is has unfortunately no MIT-license.
"""

from typing import Dict, List

from tqdm import tqdm

from cmudict_parser.ARPAToIPAMapper import get_ipa_with_stress
from cmudict_parser.CMUDictDownloader import ensure_files_are_downloaded
from cmudict_parser.CMUDictParser import parse


class CMUDict():
  def __init__(self):
    self._loaded = False

  def _load(self, dictionary_dir: str) -> None:
    self._loaded = False
    paths = ensure_files_are_downloaded(dictionary_dir)
    entries = parse(paths)

    self._entries_arpa = entries
    self._entries_ipa = self._convert_to_ipa()
    self._entries_first_ipa = self._extract_first_ipa()
    self._loaded = True

  def _ensure_data_is_loaded(self) -> None:
    if not self._loaded:
      raise Exception("Please load the dictionary first.")

  def _extract_first_ipa(self) -> Dict[str, str]:
    result: Dict[str, str] = {word: ipas[0] for word, ipas in self._entries_ipa.items()}
    return result

  def _convert_to_ipa(self) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {word: [] for word, _ in self._entries_arpa.items()}

    for word, pronunciations in tqdm(self._entries_arpa.items()):
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


def get_dict(download_folder: str = "/tmp") -> CMUDict:
  result = CMUDict()
  result._load(download_folder)
  return result
