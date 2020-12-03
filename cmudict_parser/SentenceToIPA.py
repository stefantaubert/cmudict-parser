"""
Remarks:
https://github.com/cmusphinx/cmudict is newer than 0.7b! It has for example 'declarative' but is has unfortunately no MIT-license.
"""

import string
from typing import Callable, List, Optional, Union

from cmudict_parser.CMUDict import get_dict


class SentenceToIPA():
  def __init__(self, silent):
    self.cmu_dict = get_dict(silent = silent)

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
      if any(char in string.punctuation or char == "\n" for char in word):
        ipa = self.get_ipa_of_words_with_punctuation(word, replace_unknown_with)
      else:
        ipa = self.get_ipa_of_word_in_sentence_without_punctuation(word, replace_unknown_with)
      return ipa

  def get_ipa_of_words_with_punctuation(self, word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
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
    if punctuations_before_word != "" and self.cmu_dict.contains(word_with_apo_at_beginning) and punctuations_before_word[-1] == "'":
      punctuations_before_word = punctuations_before_word[:-1]
      ipa_of_word_without_punct = f"{self.get_ipa_of_word_in_sentence_without_punctuation(word_with_apo_at_beginning, replace_unknown_with)}{char_at_end}"
    elif self.cmu_dict.contains(word_with_apo_at_end) and char_at_end == "'":
      ipa_of_word_without_punct = self.get_ipa_of_word_in_sentence_without_punctuation(word_with_apo_at_end, replace_unknown_with)
    elif "-" in word_without_punctuation and not self.cmu_dict.contains(word_without_punctuation):
      ipa_of_word_without_punct = self.get_ipa_of_words_with_hyphen(word_without_punctuation, replace_unknown_with)
    else:
      ipa_of_word_without_punct = f"{self.get_ipa_of_word_in_sentence_without_punctuation(word_without_punctuation, replace_unknown_with)}{char_at_end}"
    ipa = f"{punctuations_before_word}{ipa_of_word_without_punct}{self.get_ipa_of_words_with_punctuation(auxiliary_word, replace_unknown_with)}"
    return ipa

  def get_ipa_of_words_with_hyphen(self, word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
    parts = word.split("-")
    for length_of_combination in range(len(parts), 0, -1):
      ipa = self.find_combination_in_dict(parts, length_of_combination, replace_unknown_with)
      if ipa is not None:
        break
    return ipa

  def find_combination_in_dict(self, parts: List[str], length_of_combination, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]):
    for startword_pos in range(len(parts) - length_of_combination + 1):
      combination = parts[startword_pos]
      for pos in range(startword_pos + 1, startword_pos + length_of_combination):
        combination += f"-{parts[pos]}"
      if self.cmu_dict.contains(combination):
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
          ipa = f"{self.get_ipa_of_word_in_sentence(word_before, replace_unknown_with)}-{self.cmu_dict.get_first_ipa(combination)}-{self.get_ipa_of_word_in_sentence(word_after, replace_unknown_with)}"
        elif word_before != "":
          ipa = f"{self.get_ipa_of_word_in_sentence(word_before, replace_unknown_with)}-{self.cmu_dict.get_first_ipa(combination)}"
        elif word_after != "":
          ipa = f"{self.cmu_dict.get_first_ipa(combination)}-{self.get_ipa_of_word_in_sentence(word_after, replace_unknown_with)}"
        else:
          ipa = self.cmu_dict.get_first_ipa(combination)
        return ipa
    return None

  def get_ipa_of_word_in_sentence_without_punctuation(self, word: str, replace_unknown_with: Optional[Union[str, Callable[[str], str]]]) -> str:
    if word == "":
      return ""
    if self.cmu_dict.contains(word):
      return self.cmu_dict.get_first_ipa(word)
    if word.isupper() and word.isalpha():
      ipa = ""
      for char in word:
        ipa += self.cmu_dict.get_first_ipa(char)
      return ipa
    if replace_unknown_with is None:
      return word
    if isinstance(replace_unknown_with, str):
      return len(word) * replace_unknown_with
    return replace_unknown_with(word)
