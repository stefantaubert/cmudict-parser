'''
adjusted from https://github.com/keithito/tacotron/blob/master/text/cmudict.py
'''

import re

''' Regex for alternative pronunciation '''
_alt_re = re.compile(r'\([0-9]+\)')

def parse(paths) -> dict:
  symbols_path, _, dict_path = paths

  with open(symbols_path, encoding='latin-1') as f:
    _symbols = _parse_symbols(f)

  with open(dict_path, encoding='latin-1') as f:
    entries = _parse_cmudict(f, _symbols)

  assert_check_to_unknown_symbols(entries, _symbols)
  
  return entries

def _parse_cmudict(lines, _symbols) -> dict:
  cmudict = {}
  for line in lines:
    line_should_be_processed = _line_should_be_processed(line)

    if line_should_be_processed:
      _process_line(line, cmudict)

  return cmudict

def _process_line(line: str, cmudict: dict):
  word, pronunciation = _get_word_and_pronunciation(line)

  if word in cmudict:
    cmudict[word].append(pronunciation)
  else:
    cmudict[word] = [pronunciation]

def _get_word_and_pronunciation(line):
  parts = line.split('  ')
  word = parts[0]
  word = _remove_double_indicators(word)
  pronunciation = parts[1].strip()

  return word, pronunciation

def _remove_double_indicators(word):
  ''' example: ABBE(1) => ABBE '''
  result = re.sub(_alt_re, '', word)
  
  return result

def _line_should_be_processed(line):
  is_not_empty = len(line)
  is_special_char = line[0] < 'A' or line[0] > 'Z'
  is_apostrophe_part = line[0] == "'"
  result = is_not_empty and (not is_special_char or is_apostrophe_part)
  
  return result

def _parse_symbols(lines) -> set:
  symbols = []

  for line in lines:
    cleaned_line = line.strip()
    symbols.append(cleaned_line)

  symbols_as_set = set(symbols)

  return symbols_as_set

def assert_check_to_unknown_symbols(entries: dict, _symbols):
  for _, pronunciations in entries.items():
    for p in pronunciations:
      _assert_contains_no_unknown_symbols(p, _symbols)

def _assert_contains_no_unknown_symbols(pronunciation, known_symbols) -> str:
  parts = pronunciation.split(' ')

  for part in parts:
    is_unknown_symbol = part not in known_symbols

    if is_unknown_symbol:
      # CMUs fault: unknown symbol exist in dict
      assert False
