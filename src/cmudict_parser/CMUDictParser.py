'''
adapted from https://github.com/keithito/tacotron/blob/master/text/cmudict.py
'''

import re
from typing import Dict, List, Set, Tuple

from tqdm import tqdm

''' Regex for alternative pronunciation '''
_alt_re = re.compile(r'\([0-9]+\)')

WORD_AND_PRONUNCIATION_SEP = "  "
ARPA_SYMBOL_SEPARATOR = " "

Word = str
ARPASymbol = str
ARPAPronunciation = List[ARPASymbol]
ARPAPronunciations = List[ARPAPronunciation]
ARPADict = Dict[Word, ARPAPronunciations]


def _read_lines(file: str) -> List[str]:
  with open(file, encoding='latin-1') as f:
    return f.readlines()


def parse(paths: Tuple[str, str, str], silent: bool) -> ARPADict:
  symbols_path, _, dict_path = paths

  symbols_content = _read_lines(symbols_path)
  symbols = _parse_symbols(symbols_content)

  dict_content = _read_lines(dict_path)
  result = _parse_cmudict(dict_content, silent)

  _check_have_unknown_symbols(result, symbols)

  return result


def _parse_cmudict(lines: List[str], silent: bool) -> ARPADict:
  result: ARPADict = dict()
  data = lines if silent else tqdm(lines)
  for line in data:
    line_should_be_processed = _line_should_be_processed(line)

    if line_should_be_processed:
      _process_line(line, result)

  return result


def _process_line(line: str, cmudict: ARPADict) -> None:
  word, pronunciation_arpa = _get_word_and_pronunciation(line)

  if word not in cmudict:
    cmudict[word] = list()

  cmudict[word].append(pronunciation_arpa)


def _get_word_and_pronunciation(line: str) -> Tuple[Word, ARPAPronunciation]:
  parts = line.split(WORD_AND_PRONUNCIATION_SEP)
  word = parts[0]
  word = _remove_double_indicators(word)
  pronunciation = parts[1].strip()
  pronunciation_arpa = pronunciation.split(ARPA_SYMBOL_SEPARATOR)

  return word, pronunciation_arpa


def _remove_double_indicators(word: Word) -> Word:
  ''' example: ABBE(1) => ABBE '''
  result = re.sub(_alt_re, '', word)

  return result


def _line_should_be_processed(line: str) -> bool:
  is_not_empty = len(line)
  is_special_char = line[0] < 'A' or line[0] > 'Z'
  is_apostrophe_part = line[0] == "'"
  result = is_not_empty and (not is_special_char or is_apostrophe_part)

  return result


def _parse_symbols(lines: List[str]) -> Set[ARPASymbol]:
  symbols: List[ARPASymbol] = []

  for line in lines:
    cleaned_line = line.strip()
    symbols.append(cleaned_line)

  symbols_as_set: Set[ARPASymbol] = set(symbols)

  return symbols_as_set


def _check_have_unknown_symbols(entries: ARPADict, symbols: Set[ARPASymbol]) -> None:
  for _, pronunciations in entries.items():
    for p in pronunciations:
      _check_contains_no_unknown_symbols(p, symbols)


def _check_contains_no_unknown_symbols(arpa_pronunciation: ARPAPronunciation, known_arpa_symbols: Set[ARPASymbol]) -> None:
  for arpa_symbol in arpa_pronunciation:
    is_unknown_arpa_symbol = arpa_symbol not in known_arpa_symbols

    if is_unknown_arpa_symbol:
      # CMUs fault: unknown symbol exist in dict
      raise Exception("The dictionary contains symbols which were not in the symbols-file!")
