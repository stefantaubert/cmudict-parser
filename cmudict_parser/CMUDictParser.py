'''
adapted from https://github.com/keithito/tacotron/blob/master/text/cmudict.py
'''

import re
from typing import Dict, List, Set, Tuple

from tqdm import tqdm

''' Regex for alternative pronunciation '''
_alt_re = re.compile(r'\([0-9]+\)')


def parse(paths: Tuple[str, str, str], silent: bool) -> Dict[str, List[str]]:
  symbols_path, _, dict_path = paths

  with open(symbols_path, encoding='latin-1') as f:
    _symbols = _parse_symbols(f.readlines())

  with open(dict_path, encoding='latin-1') as f:
    entries = _parse_cmudict(f.readlines(), silent)

  assert_check_to_unknown_symbols(entries, _symbols)

  return entries


def _parse_cmudict(lines: List[str], silent: bool) -> Dict[str, List[str]]:
  result: Dict[str, List[str]] = dict()
  data = lines if silent else tqdm(lines)
  for line in data:
    line_should_be_processed = _line_should_be_processed(line)

    if line_should_be_processed:
      _process_line(line, result)

  return result


def _process_line(line: str, cmudict: Dict[str, List[str]]) -> None:
  word, pronunciation = _get_word_and_pronunciation(line)

  if word not in cmudict:
    cmudict[word] = list()

  cmudict[word].append(pronunciation)


def _get_word_and_pronunciation(line: str) -> Tuple[str, str]:
  parts = line.split('  ')
  word = parts[0]
  word = _remove_double_indicators(word)
  pronunciation = parts[1].strip()

  return word, pronunciation


def _remove_double_indicators(word: str) -> str:
  ''' example: ABBE(1) => ABBE '''
  result = re.sub(_alt_re, '', word)

  return result


def _line_should_be_processed(line: str) -> bool:
  is_not_empty = len(line)
  is_special_char = line[0] < 'A' or line[0] > 'Z'
  is_apostrophe_part = line[0] == "'"
  result = is_not_empty and (not is_special_char or is_apostrophe_part)

  return result


def _parse_symbols(lines: List[str]) -> Set[str]:
  symbols: List[str] = []

  for line in lines:
    cleaned_line = line.strip()
    symbols.append(cleaned_line)

  symbols_as_set: Set[str] = set(symbols)

  return symbols_as_set


def assert_check_to_unknown_symbols(entries: Dict[str, List[str]], _symbols: Set[str]) -> None:
  for _, pronunciations in entries.items():
    for p in pronunciations:
      _assert_contains_no_unknown_symbols(p, _symbols)


def _assert_contains_no_unknown_symbols(pronunciation: str, known_symbols: Set[str]) -> str:
  parts = pronunciation.split(' ')

  for part in parts:
    is_unknown_symbol = part not in known_symbols

    if is_unknown_symbol:
      # CMUs fault: unknown symbol exist in dict
      assert False
