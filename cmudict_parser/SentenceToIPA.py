"""
Remarks:
https://github.com/cmusphinx/cmudict is newer than 0.7b! It has for example 'declarative' but is has unfortunately no MIT-license.
"""

import string
from typing import Callable, Dict, List, Optional, Union


def sentence_to_ipa(dict: Dict[str, str], sentence: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  if replace_unknown_with is not None and isinstance(replace_unknown_with, str) and len(replace_unknown_with) >= 2:
    raise Exception("Parameter replace_unknown_with can only be 0 or 1 char.")
  words = sentence.split(" ")
  ipa_words = []
  for word in words:
    ipa = get_ipa_of_word_in_sentence(dict, word, replace_unknown_with)
    ipa_words.append(ipa)
  res = " ".join(ipa_words)
  return res

def get_ipa_of_word_in_sentence(dict: Dict[str, str], word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  if any(char in string.punctuation or char == "\n" for char in word):
    ipa = get_ipa_of_words_with_punctuation(dict, word, replace_unknown_with)
  else:
    ipa = get_ipa_of_word_in_sentence_without_punctuation(dict, word, replace_unknown_with)
  return ipa

def get_ipa_of_words_with_punctuation(dict: Dict[str, str], word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  if word == "":
    return ""
  punctuations_before_word=""
  while word != "" and (word[0] in string.punctuation or word[0] =="\n"):
    punctuations_before_word += word[0]
    word = word[1:]
  if word == "":
    return punctuations_before_word
  auxiliary_word = word
  word_without_punctuation = ""
  while auxiliary_word != "" and (auxiliary_word[0].isalpha() or auxiliary_word[0] in "'-"):
    word_without_punctuation += auxiliary_word[0]
    auxiliary_word = auxiliary_word[1:]
  char_at_end = ""
  if word_without_punctuation[-1] in "-'":
    char_at_end = word_without_punctuation[-1]
    word_without_punctuation = word_without_punctuation[:-1]
  word_with_apo_at_beginning = f"'{word_without_punctuation}"
  word_with_apo_at_end = f"{word_without_punctuation}'"
  if punctuations_before_word != "" and word_with_apo_at_beginning.upper() in dict and punctuations_before_word[-1] == "'":
    punctuations_before_word = punctuations_before_word[:-1]
    ipa_of_word_without_punct = f"{get_ipa_of_word_in_sentence_without_punctuation(dict, word_with_apo_at_beginning, replace_unknown_with)}{char_at_end}"
  elif word_with_apo_at_end.upper() in dict and char_at_end == "'":
    ipa_of_word_without_punct = get_ipa_of_word_in_sentence_without_punctuation(dict, word_with_apo_at_end, replace_unknown_with)
  elif "-" in word_without_punctuation and not word_without_punctuation.upper() in dict:
    ipa_of_word_without_punct = get_ipa_of_words_with_hyphen(dict, word_without_punctuation, replace_unknown_with)
  else:
    ipa_of_word_without_punct = f"{get_ipa_of_word_in_sentence_without_punctuation(dict, word_without_punctuation, replace_unknown_with)}{char_at_end}"
  ipa = f"{punctuations_before_word}{ipa_of_word_without_punct}{get_ipa_of_words_with_punctuation(dict, auxiliary_word, replace_unknown_with)}"
  return ipa

def get_ipa_of_words_with_hyphen(dict: Dict[str, str], word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  parts = word.split("-")
  ipa = ""
  for length_of_combination in range(len(parts), 0, -1):
    ipa = find_combination_in_dict(dict, parts, length_of_combination, replace_unknown_with)
    if ipa is not None:
      break
  return ipa

def find_combination_in_dict(dict: Dict[str, str], parts: List[str], length_of_combination, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]):
  for startword_pos in range(len(parts) - length_of_combination + 1):
    combination = parts[startword_pos]
    for pos in range(startword_pos + 1, startword_pos + length_of_combination):
      combination += f"-{parts[pos]}"
    if combination.upper() in dict:
      if startword_pos != 0:
        word_before = parts[0]
      else:
        word_before = ""
      if startword_pos != len(parts) - length_of_combination:
        word_after = parts[startword_pos + length_of_combination]
      else:
        word_after = ""
      for pos_before in range(1, startword_pos):
        word_before += f"-{parts[pos_before]}"
      for pos_after in range(startword_pos + length_of_combination + 1, len(parts)):
        word_after += f"-{parts[pos_after]}"
      if word_before != "" and word_after != "":
        ipa = f"{get_ipa_of_word_in_sentence(dict, word_before, replace_unknown_with)}-{dict[combination.upper()]}-{get_ipa_of_word_in_sentence(dict, word_after, replace_unknown_with)}"
      elif word_before != "":
        ipa = f"{get_ipa_of_word_in_sentence(dict, word_before, replace_unknown_with)}-{dict[combination.upper()]}"
      elif word_after != "":
        ipa = f"{dict[combination.upper()]}-{get_ipa_of_word_in_sentence(dict, word_after, replace_unknown_with)}"
      else:
        ipa = dict[combination.upper()]
      return ipa
  return None

def get_ipa_of_word_in_sentence_without_punctuation(dict: Dict[str, str], word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
  if word == "":
    return ""
  if word.upper() in dict:
    return dict[word.upper()]
  if word.isupper() and word.isalpha():
    ipa = ""
    for char in word:
      ipa += dict[char]
    return ipa
  if replace_unknown_with is None:
    return word
  if isinstance(replace_unknown_with, str):
    return len(word) * replace_unknown_with
  return replace_unknown_with(word)
