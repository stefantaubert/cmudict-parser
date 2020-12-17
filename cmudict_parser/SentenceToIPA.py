"""
Remarks:
https://github.com/cmusphinx/cmudict is newer than 0.7b! It has for example 'declarative' but is has unfortunately no MIT-license.
"""

import string
from typing import Callable, Dict, List, Optional, Tuple, Union

PUNCTUATION_AND_LINEBREAK = f"{string.punctuation}\n"


def sentence_to_ipa(dict: Dict[str, str], sentence: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  words = sentence.split(" ")
  ipa_words = [get_ipa_of_word_in_sentence(dict, word, replace_unknown_with) for word in words]
  res = " ".join(ipa_words)
  return res


def get_ipa_of_word_in_sentence(dict: Dict[str, str], word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  if any(char in PUNCTUATION_AND_LINEBREAK for char in word):
    ipa = get_ipa_of_word_with_punctuation(dict, word, replace_unknown_with)
  else:
    ipa = get_ipa_of_word_without_punctuation_or_unknown_words(dict, word, replace_unknown_with)
  return ipa


def get_ipa_of_word_with_punctuation(dict: Dict[str, str], word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  word, punctuation_before_word = extract_punctuation_before_word(word)
  if word == "":
    return punctuation_before_word
  word_without_punctuation, punctuation_after_word = extract_punctuation_after_word_except_hyphen_or_apostrophe(
    word)
  return ipa_of_punctuation_and_words_combined(dict, punctuation_before_word, word_without_punctuation, punctuation_after_word, replace_unknown_with)


def extract_punctuation_before_word(word: str) -> Tuple[str, str]:
  punctuation_before_word = ""
  while word != "" and (word[0] in PUNCTUATION_AND_LINEBREAK):
    punctuation_before_word += word[0]
    word = word[1:]
  return word, punctuation_before_word


def extract_punctuation_after_word_except_hyphen_or_apostrophe(word: str) -> Tuple[str, str]:
  punctuation_after_word = word
  word_without_punctuation = ""
  while punctuation_after_word != "" and (punctuation_after_word[0].isalpha() or punctuation_after_word[0] in "'-"):
    word_without_punctuation += punctuation_after_word[0]
    punctuation_after_word = punctuation_after_word[1:]
  return word_without_punctuation, punctuation_after_word


def ipa_of_punctuation_and_words_combined(dict: Dict[str, str], punctuation_before_word: str, word_without_punctuation: str, punctuation_after_word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  assert word_without_punctuation != "" and word_without_punctuation[0].isalpha()
  word_without_punctuation, char_at_end, word_with_apo_at_beginning, word_with_apo_at_end, word_with_apo_at_end_and_beginning = word_with_apo(
    word_without_punctuation)
  if punctuation_before_word != "" and punctuation_before_word[-1] == "'" and char_at_end == "'" and word_with_apo_at_end_and_beginning.upper() in dict:
    punctuation_before_word = punctuation_before_word[:-1]
    ipa_of_word_without_punct = get_ipa_of_word_without_punctuation_or_unknown_words(
      dict, word_with_apo_at_end_and_beginning, replace_unknown_with)
  elif punctuation_before_word != "" and word_with_apo_at_beginning.upper() in dict and punctuation_before_word[-1] == "'":
    punctuation_before_word = punctuation_before_word[:-1]
    ipa_of_word_without_punct = f"{get_ipa_of_word_without_punctuation_or_unknown_words(dict, word_with_apo_at_beginning, replace_unknown_with)}{char_at_end}"
  elif word_with_apo_at_end.upper() in dict and char_at_end == "'":
    ipa_of_word_without_punct = get_ipa_of_word_without_punctuation_or_unknown_words(
      dict, word_with_apo_at_end, replace_unknown_with)
  elif "-" in word_without_punctuation and not word_without_punctuation.upper() in dict:
    ipa_of_word_without_punct = f"{get_ipa_of_words_with_hyphen(dict, word_without_punctuation, replace_unknown_with)}{char_at_end}"
  else:
    ipa_of_word_without_punct = f"{get_ipa_of_word_without_punctuation_or_unknown_words(dict, word_without_punctuation, replace_unknown_with)}{char_at_end}"
  return value_depending_on_is_alphabetic_value_in_punctuation_after_word(dict, punctuation_before_word, ipa_of_word_without_punct, punctuation_after_word, replace_unknown_with)


def word_with_apo(word_without_punctuation: str) -> Tuple[str, str, str, str, str]:
  if word_without_punctuation[-1] in "-'":
    return word_without_punctuation[:-1], word_without_punctuation[-1], f"'{word_without_punctuation[:-1]}", f"{word_without_punctuation[:-1]}'", f"'{word_without_punctuation[:-1]}'"
  return word_without_punctuation, "", f"'{word_without_punctuation}", f"{word_without_punctuation}'", f"'{word_without_punctuation}'"


def value_depending_on_is_alphabetic_value_in_punctuation_after_word(dict: Dict[str, str], punctuation_before_word: str, ipa_of_word_without_punct: str, punctuation_after_word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  if any(char.isalpha() for char in punctuation_after_word):
    return f"{punctuation_before_word}{ipa_of_word_without_punct}{get_ipa_of_word_with_punctuation(dict, punctuation_after_word, replace_unknown_with)}"
  return f"{punctuation_before_word}{ipa_of_word_without_punct}{punctuation_after_word}"


def get_ipa_of_words_with_hyphen(dict: Dict[str, str], word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  parts = word.split("-")
  ipa = ""
  for length_of_combination in range(len(parts), 0, -1):
    ipa = find_combination_of_certain_length_in_dict(
      dict, parts, length_of_combination, replace_unknown_with)
    if ipa is not None:
      break
  assert ipa is not None
  return ipa


def find_combination_of_certain_length_in_dict(dict: Dict[str, str], parts: List[str], length_of_combination, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> Optional[str]:
  assert all_keys_are_upper(dict)
  for startword_pos in range(len(parts) - length_of_combination + 1):
    combination = recombine_word(parts, startword_pos, startword_pos + length_of_combination)
    word, apos_before, apos_after = strip_apos_at_beginning_and_end_if_they_do_not_belong_to_word(
      dict, combination)
    if word.upper() in dict:
      word_before, hyphen_before = word_and_hyphen_before_or_after(parts, 0, startword_pos)
      word_after, hyphen_after = word_and_hyphen_before_or_after(
        parts, startword_pos + length_of_combination, len(parts))
      return f"{get_ipa_of_word_in_sentence(dict, word_before, replace_unknown_with)}{hyphen_before}{apos_before}{dict[word.upper()]}{apos_after}{hyphen_after}{get_ipa_of_word_in_sentence(dict, word_after, replace_unknown_with)}"
  return None


def strip_apos_at_beginning_and_end_if_they_do_not_belong_to_word(dict: Dict[str, str], word: str) -> Tuple[str, str, str]:
  word, apos_before = strip_apos(word, 0)
  word, apos_after = strip_apos(word, -1)
  if f"{word}'".upper() in dict and apos_after != "":
    word = f"{word}'"
    apos_after = apos_after[:-1]
  if f"'{word}".upper() in dict and apos_before != "":
    word = f"'{word}"
    apos_before = apos_before[:-1]
  return word, apos_before, apos_after


def strip_apos(word: str, pos: int) -> Tuple[str, str]:
  assert pos == 0 or pos == -1
  apos = ""
  while word != "" and word[pos] == "'":
    apos += "'"
    word = word[1:] if pos == 0 else word[:-1]
  return word, apos


def word_and_hyphen_before_or_after(parts: List[str], startpos: int, endpos: int) -> Tuple[str, str]:
  if endpos == 0 or startpos == len(parts):
    return "", ""
  return recombine_word(parts, startpos, endpos), "-"


def recombine_word(parts: List[str], startpos: int, endpos: int) -> str:
  assert startpos >= 0 and startpos < endpos and endpos <= len(parts)
  parts = parts[startpos:endpos]
  word = "-".join(parts)
  return word


def get_ipa_of_word_without_punctuation_or_unknown_words(dict: Dict[str, str], word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  assert all_keys_are_upper(dict)
  if word == "":
    return ""
  if word.upper() in dict:
    return dict[word.upper()]
  if word_is_really_upper(word):
    return big_letters_to_ipa(dict, word)
  if replace_unknown_with is None:
    return word
  if isinstance(replace_unknown_with, str):
    return replace_unknown_with_is_string(word, replace_unknown_with)
  return replace_unknown_with(word)


def replace_unknown_with_is_string(word: str, replace_unknown_with: str) -> str:
  assert isinstance(replace_unknown_with, str)
  if len(replace_unknown_with) >= 2:
    raise ValueError("Parameter replace_unknown_with can only be 0 or 1 char.")
  return len(word) * replace_unknown_with


def word_is_really_upper(word: str) -> bool:
  return word.isupper() and word.isalpha()


def big_letters_to_ipa(dict: Dict[str, str], word: str) -> str:
  assert all_keys_are_upper(dict)
  assert word_is_really_upper(word) or word == ""
  ipa = ""
  for char in word:
    assert char in dict
    ipa += dict[char]
  return ipa


def all_keys_are_upper(dict: Dict[str, str]) -> bool:
  for key in dict.keys():
    if not key.isupper():
      return False
  return True
