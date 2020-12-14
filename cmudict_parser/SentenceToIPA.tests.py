import unittest
from typing import Optional

from cmudict_parser.CMUDict import CMUDict
from cmudict_parser.SentenceToIPA import (
    big_letters_to_ipa,
    extract_punctuation_after_word_except_hyphen_or_apostrophe,
    extract_punctuation_before_word,
    find_combination_of_certain_length_in_dict, get_ipa_of_word_in_sentence,
    get_ipa_of_word_with_punctuation,
    get_ipa_of_word_without_punctuation_or_unknown_words,
    get_ipa_of_words_with_hyphen, ipa_of_punctuation_and_words_combined,
    recombine_word, replace_unknown_with_is_string, sentence_to_ipa,
    value_depending_on_is_alphabetic_value_in_punctuations_after_word,
    word_and_hyphen_before_or_after, word_is_really_upper, word_with_apo)


class UnitTests(unittest.TestCase):
  def __init__(self, methodName: str) -> None:
    super().__init__(methodName)

  # region big_letters_to_ipa
  def test_big_letters_to_ipa__only_big_letters__returns_combination_of_values(self):
    input_dict = {"A": "a", "P": "x", "R": "y", "S": "z"}
    res = big_letters_to_ipa(input_dict, "PRS")

    self.assertEqual("xyz", res)

  def test_big_letters_to_ipa__empty_string__returns_empty_string(self):
    input_dict = {"A": "a", "P": "x", "R": "y", "S": "z"}
    res = big_letters_to_ipa(input_dict, "")

    self.assertEqual("", res)

  # endregion

  # region word_is_really_upper

  def test_word_is_really_upper__word_with_number__returns_false(self):
    res = word_is_really_upper("PRS1")

    self.assertEqual(False, res)

  def test_word_is_really_upper__word_with_small_letters__returns_false(self):
    res = word_is_really_upper("PRs")

    self.assertEqual(False, res)

  def test_word_is_really_upper__only_big_letters__returns_true(self):
    res = word_is_really_upper("PRS")

    self.assertEqual(True, res)

  # endregion

  # region get_ipa_of_word_without_punctuation_or_unknown_words

  def test_get_ipa_of_word_without_punctuation_or_unknown_words__word_in_dict__returns_value(self):
    input_dict = {"PRS": "abc", "P": "x", "R": "y", "S": "z"}
    res = get_ipa_of_word_without_punctuation_or_unknown_words(
      input_dict, "PRS", replace_unknown_with="_")

    self.assertEqual("abc", res)

  def test_get_ipa_of_word_without_punctuation_or_unknown_words__word_not_in_dict_with_only_upper_letters__returns_combination_of_values(self):
    input_dict = {"PSR": "abc", "P": "x", "R": "y", "S": "z"}
    res = get_ipa_of_word_without_punctuation_or_unknown_words(
      input_dict, "PRS", replace_unknown_with="_")

    self.assertEqual("xyz", res)

  def test_get_ipa_of_word_without_punctuation_or_unknown_words__word_not_in_dict_replace_unknown_with_None__returns_word(self):
    input_dict = {"PSR": "abc", "P": "x", "R": "y", "S": "z"}
    res = get_ipa_of_word_without_punctuation_or_unknown_words(
      input_dict, "prs", replace_unknown_with=None)

    self.assertEqual("prs", res)

  def test_get_ipa_of_word_without_punctuation_or_unknown_words__word_not_in_dict_replace_unknown_with_underline__returns_word(self):
    input_dict = {"PSR": "abc", "P": "x", "R": "y", "S": "z"}
    res = get_ipa_of_word_without_punctuation_or_unknown_words(
      input_dict, "prs", replace_unknown_with="_")

    self.assertEqual("___", res)

  def test_get_ipa_of_word_without_punctuation_or_unknown_words__replace_unknown_with_string_with_more_than_one_char_and_word_not_in_dict__throws_exception(self):
    self.assertRaises(ValueError, replace_unknown_with_is_string, "prs", replace_unknown_with="123")

  def test_gget_ipa_of_word_without_punctuation_or_unknown_words__word_not_in_dict_replace_unknown_with_costum_func__returns_word(self):
    input_dict = {"PSR": "abc", "P": "x", "R": "y", "S": "z"}
    res = get_ipa_of_word_without_punctuation_or_unknown_words(
      input_dict, "prs", replace_unknown_with=lambda x: x + "123")

    self.assertEqual("prs123", res)

  # endregion

  # region recombine_word

  def test_recombine_word__startpos_is_zero_endpos_is_one__returns_first_word(self):
    parts = ["cat", "o", "nine", "tails"]
    res = recombine_word(parts, 0, 1)

    self.assertEqual("cat", res)

  def test_recombine_word__everything_except_first_and_last_word__returns_words_in_the_middle_connected_with_hyphens(self):
    parts = ["cat", "o", "nine", "tails"]
    res = recombine_word(parts, 1, len(parts) - 1)

    self.assertEqual("o-nine", res)

  def test_recombine_word__everything_except_first_word__returns_last_three_words_connected_with_hyphens(self):
    parts = ["cat", "o", "nine", "tails"]
    res = recombine_word(parts, 1, len(parts))

    self.assertEqual("o-nine-tails", res)

  # endregion

  # region word_and_hyphen_before_or_after

   # should return hyphen

  def test_word_and_hyphen_before_or_after__startpos_is_zero_endpos_is_one__returns_first_word_and_hyphen(self):
    parts = ["cat", "o", "nine", "tails"]
    res = word_and_hyphen_before_or_after(parts, 0, 1)

    self.assertEqual("cat", res[0])
    self.assertEqual("-", res[1])

  def test_word_and_hyphen_before_or_after__everything_except_first_and_last_word__returns_words_in_the_middle_connected_with_hyphens_and_hyphen(self):
    parts = ["cat", "o", "nine", "tails"]
    res = word_and_hyphen_before_or_after(parts, 1, len(parts) - 1)

    self.assertEqual("o-nine", res[0])
    self.assertEqual("-", res[1])

  def test_word_and_hyphen_before_or_after__everything_except_first_word__returns_last_three_words_connected_with_hyphens_and_hyphen(self):
    parts = ["cat", "o", "nine", "tails"]
    res = word_and_hyphen_before_or_after(parts, 1, len(parts))

    self.assertEqual("o-nine-tails", res[0])
    self.assertEqual("-", res[1])

   # should not return hyphen

  def test_word_and_hyphen_before_or_after__endpos_is_zero__returns_empty_word_and_no_hyphen(self):
    parts = ["cat", "o", "nine", "tails"]
    res = word_and_hyphen_before_or_after(parts, 1, 0)

    self.assertEqual("", res[0])
    self.assertEqual("", res[1])

  def test_word_and_hyphen_before_or_after__startpos_is_length_of_list__returns_empty_word_and_no_hyphen(self):
    parts = ["cat", "o", "nine", "tails"]
    res = word_and_hyphen_before_or_after(parts, len(parts), 0)

    self.assertEqual("", res[0])
    self.assertEqual("", res[1])

  # endregion

  # region find_combination_of_certain_length_in_dict

  def test_find_combination_of_certain_length_in_dict__length_too_long__returns_none(self):
    parts = ["to", "cat", "o", "nine", "tails", "to"]
    input_dict = {"CAT-O-NINE-TAILS": "xyz", "TO": "a"}
    res = find_combination_of_certain_length_in_dict(input_dict, parts, 5, "_")

    self.assertIsNone(res)

  def test_find_combination_of_certain_length_in_dict__right_length_start_in_middle__returns_combination_of_values(self):
    parts = ["to", "cat", "o", "nine", "tails", "to"]
    input_dict = {"CAT-O-NINE-TAILS": "xyz", "TO": "a"}
    res = find_combination_of_certain_length_in_dict(input_dict, parts, 4, "_")

    self.assertEqual("a-xyz-a", res)

  def test_find_combination_of_certain_length_in_dict__right_length_start_at_beginning__returns_combination_of_values(self):
    parts = ["cat", "o", "nine", "tails", "to"]
    input_dict = {"CAT-O-NINE-TAILS": "xyz", "TO": "a"}
    res = find_combination_of_certain_length_in_dict(input_dict, parts, 4, "_")

    self.assertEqual("xyz-a", res)

  def test_find_combination_of_certain_length_in_dict__right_length_combination_reaches_end__returns_combination_of_values(self):
    parts = ["to", "cat", "o", "nine", "tails"]
    input_dict = {"CAT-O-NINE-TAILS": "xyz", "TO": "a"}
    res = find_combination_of_certain_length_in_dict(input_dict, parts, 4, "_")

    self.assertEqual("a-xyz", res)

  def test_find_combination_of_certain_length_in_dict__only_single_words__returns_combination_of_values(self):
    parts = ["to", "no", "so"]
    input_dict = {"NO": "x", "SO": "y", "TO": "z"}
    res = find_combination_of_certain_length_in_dict(input_dict, parts, 1, "_")

    self.assertEqual("z-x-y", res)

  # endregion

  # region get_ipa_of_words_with_hyphen

  def test_get_ipa_of_words_with_hyphen__three_words__returns_combination_of_values(self):
    input_word = "to-cat-o-nine-tails-to"
    input_dict = {"CAT-O-NINE-TAILS": "xyz", "TO": "a"}
    res = get_ipa_of_words_with_hyphen(input_dict, input_word, "_")

    self.assertEqual("a-xyz-a", res)

  def test_get_ipa_of_words_with_hyphen__two_words_with_longer_one_at_beginning__returns_combination_of_values(self):
    input_word = "cat-o-nine-tails-to"
    input_dict = {"CAT-O-NINE-TAILS": "xyz", "TO": "a"}
    res = get_ipa_of_words_with_hyphen(input_dict, input_word, "_")

    self.assertEqual("xyz-a", res)

  def test_get_ipa_of_words_with_hyphen__two_words_with_longer_one_at_end__returns_combination_of_values(self):
    input_word = "to-cat-o-nine-tails"
    input_dict = {"CAT-O-NINE-TAILS": "xyz", "TO": "a"}
    res = get_ipa_of_words_with_hyphen(input_dict, input_word, "_")

    self.assertEqual("a-xyz", res)

  def test_get_ipa_of_words_with_hyphen__only_single_words__returns_combination_of_values(self):
    input_word = "to-no-so"
    input_dict = {"NO": "x", "SO": "y", "TO": "z"}
    res = get_ipa_of_words_with_hyphen(input_dict, input_word, "_")

    self.assertEqual("z-x-y", res)

  # endregion

  # region value_depending_on_is_alphabetic_value_in_punctuations_after_word

  def test_value_depending_on_is_alphabetic_value_in_punctuations_after_word__word_with_alphabetic_values_in_punctuations_after_word_which_are_not_in_dict__returns_input_ipa_and_first_char_of_punctuations_after_word_and_underlines_for_rest(self):
    input_dict = {"A": "e", "B": "f", "C": "g"}
    punctuation_before_word = ""
    ipa_of_word_without_punctuation = "abc"
    punctuations_after_word = "#abc"

    res = value_depending_on_is_alphabetic_value_in_punctuations_after_word(
      input_dict, punctuation_before_word, ipa_of_word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("abc#___", res)

  def test_value_depending_on_is_alphabetic_value_in_punctuations_after_word__word_with_alphabetic_values_in_punctuations_after_word_which_are_in_dict__returns_input_ipa_and_first_char_of_punctuations_after_word_and_ipa_of_upper_letters(self):
    input_dict = {"A": "e", "B": "f", "C": "g"}
    punctuation_before_word = ""
    ipa_of_word_without_punctuation = "abc"
    punctuations_after_word = "#ABC"

    res = value_depending_on_is_alphabetic_value_in_punctuations_after_word(
      input_dict, punctuation_before_word, ipa_of_word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("abc#efg", res)

  def test_value_depending_on_is_alphabetic_value_in_punctuations_after_word__word_without_alphabetic_values_in_punctuations_after_word__returns_input_ipa_and_keeps_punctuations_after_word_as_they_are(self):
    input_dict = {"A": "e", "B": "f", "C": "d"}
    punctuation_before_word = ""
    ipa_of_word_without_punctuation = "abc"
    punctuations_after_word = "#!'-'"

    res = value_depending_on_is_alphabetic_value_in_punctuations_after_word(
      input_dict, punctuation_before_word, ipa_of_word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("abc#!'-'", res)

  # endregion

  # region word_with_apo

  def test_word_with_apo__no_apo_or_hyphen_at_end__returns_word__empty_char__and_word_with_apo_at_beginning_or_end(self):
    input_word = "stones"
    res = word_with_apo(input_word)

    self.assertEqual(5, len(res))
    self.assertEqual(input_word, res[0])
    self.assertEqual("", res[1])
    self.assertEqual("'" + input_word, res[2])
    self.assertEqual(input_word + "'", res[3])
    self.assertEqual("'" + input_word + "'", res[4])

  def test_word_with_apo__apo_at_end__returns_word_without_apo_at_end__apo__and_word_with_apo_at_beginning_or_end(self):
    input_word = "stones'"
    res = word_with_apo(input_word)

    self.assertEqual(5, len(res))
    self.assertEqual("stones", res[0])
    self.assertEqual("'", res[1])
    self.assertEqual("'stones", res[2])
    self.assertEqual(input_word, res[3])
    self.assertEqual("'" + input_word, res[4])

  def test_word_with_apo__apo_at_beginning__returns_word_with_apo_at_beginning__empty_string__word_with_one_more_apo_at_beginning__and_word_with_apo_at_end(self):
    input_word = "'stones"
    res = word_with_apo(input_word)

    self.assertEqual(5, len(res))
    self.assertEqual("'stones", res[0])
    self.assertEqual("", res[1])
    self.assertEqual("'" + input_word, res[2])
    self.assertEqual(input_word + "'", res[3])
    self.assertEqual("'" + input_word + "'", res[4])

  # endregion

  # region ipa_of_punctuation_and_words_combined

  def test_ipa_of_punctuation_and_words_combined__word_with_apo_at_beginning__returns_value_of_this_word_plus_punctutations_at_beginning_and_end_but_not_the_apo_that_belongs_to_word(self):
    input_dict = {"ALLO": "a", "'ALLO": "b"}
    punctuations_before_word = "$-''"
    word_without_punctuation = "allo"
    punctuations_after_word = "+*"
    res = ipa_of_punctuation_and_words_combined(
      input_dict, punctuations_before_word, word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("$-'b+*", res)

  def test_ipa_of_punctuation_and_words_combined__last_char_of_punctuations_before_word_is_apo_but_word_not_in_dict___returns_underlines_instead_of_word_and_keeps_punctuations(self):
    input_dict = {"ALLO": "a", "'ALLO": "b"}
    punctuations_before_word = "$-''"
    word_without_punctuation = "bllo"
    punctuations_after_word = "+*"
    res = ipa_of_punctuation_and_words_combined(
      input_dict, punctuations_before_word, word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("$-''____+*", res)

  def test_ipa_of_punctuation_and_words_combined__word_with_apo_at_end_is_in_dict___returns_value_of_this_word_plus_punctutations_at_beginning_and_end(self):
    input_dict = {"ALLO": "a", "'ALLO": "b", "ALLO'": "c"}
    punctuations_before_word = "$-"
    word_without_punctuation = "allo'"
    punctuations_after_word = "+*"
    res = ipa_of_punctuation_and_words_combined(
      input_dict, punctuations_before_word, word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("$-c+*", res)

  def test_ipa_of_punctuation_and_words_combined__word_has_apo_at_end_but_is_in_dict___returns_value_of_this_word_plus_punctutations_at_beginning_and_end(self):
    input_dict = {"ALLO": "a", "'ALLO": "b"}
    punctuations_before_word = "$-"
    word_without_punctuation = "allo'"
    punctuations_after_word = "+*"
    res = ipa_of_punctuation_and_words_combined(
      input_dict, punctuations_before_word, word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("$-a'+*", res)

  def test_ipa_of_punctuation_and_words_combined__word_with_hyphen_and_is_in_dict___returns_value_of_this_word_plus_punctutations_at_beginning_and_end(self):
    input_dict = {"AL-LO": "a", "AL": "b", "LO": "c"}
    punctuations_before_word = "$-"
    word_without_punctuation = "al-lo"
    punctuations_after_word = "+*"
    res = ipa_of_punctuation_and_words_combined(
      input_dict, punctuations_before_word, word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("$-a+*", res)

  def test_ipa_of_punctuation_and_words_combined__word_with_hyphen_and_is_not_in_dict_but_its_parts_are___returns_value_of_the_word_parts_connected_with_hyphen_plus_punctutations_at_beginning_and_end(self):
    input_dict = {"ALLO": "a", "AL": "b", "LO": "c"}
    punctuations_before_word = "$-"
    word_without_punctuation = "al-lo"
    punctuations_after_word = "+*"
    res = ipa_of_punctuation_and_words_combined(
      input_dict, punctuations_before_word, word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("$-b-c+*", res)

  def test_ipa_of_punctuation_and_words_combined__word_with_hyphen_and_is_not_in_dict_but_one_of_its_parts_are___returns_value_of_this_part_and_underlines_for_the_part_not_in_dict_connected_with_hyphen_plus_punctutations_at_beginning_and_end(self):
    input_dict = {"ALLO": "a", "AL": "b", "O": "c"}
    punctuations_before_word = "$-"
    word_without_punctuation = "al-lo"
    punctuations_after_word = "+*"
    res = ipa_of_punctuation_and_words_combined(
      input_dict, punctuations_before_word, word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("$-b-__+*", res)

  def test_ipa_of_punctuation_and_words_combined__normal_word_without_hyphen_or_apo___returns_value_of_word_plus_punctutations_at_beginning_and_end(self):
    input_dict = {"ALLO": "a", "AL": "b", "O": "c"}
    punctuations_before_word = "$-"
    word_without_punctuation = "allo"
    punctuations_after_word = "+*"
    res = ipa_of_punctuation_and_words_combined(
      input_dict, punctuations_before_word, word_without_punctuation, punctuations_after_word, "_")

    self.assertEqual("$-a+*", res)

  # endregion

  # region extract_punctuation_before_word

  def test_extract_punctuation_before_word__no_punctuation_before_word__returns_input_and_empty_string(self):
    input_word = "allo#'!"
    res = extract_punctuation_before_word(input_word)

    self.assertEqual(input_word, res[0])
    self.assertEqual("", res[1])

  def test_extract_punctuation_before_word__punctuation_before_word__returns_punctuation_before_word_and_rest(self):
    input_word = "&!allo#'!"
    res = extract_punctuation_before_word(input_word)

    self.assertEqual("allo#'!", res[0])
    self.assertEqual("&!", res[1])

  # endregion

  # region extract_punctuation_after_word_except_hyphen_or_apostrophe

  def test_extract_punctuation_after_word_except_hyphen_or_apostrophe__no_punctuation_after_word__returns_input_and_empty_string(self):
    input_word = "allo"
    res = extract_punctuation_after_word_except_hyphen_or_apostrophe(input_word)

    self.assertEqual(input_word, res[0])
    self.assertEqual("", res[1])

  def test_extract_punctuation_after_word_except_hyphen_or_apostrophe__apostrophe_after_word__returns_word_with_hyphen__and__remaining_punctuation(self):
    input_word = "allo'!"
    res = extract_punctuation_after_word_except_hyphen_or_apostrophe(input_word)

    self.assertEqual("allo'", res[0])
    self.assertEqual("!", res[1])

  def test_extract_punctuation_after_word_except_hyphen_or_apostrophe__punctuation_after_word_but_not_hyphen_or_apostrophe__returns_word__and__punctuation(self):
    input_word = "allo#!"
    res = extract_punctuation_after_word_except_hyphen_or_apostrophe(input_word)

    self.assertEqual("allo", res[0])
    self.assertEqual("#!", res[1])

  # endregion

  # region get_ipa_of_word_with_punctuation

  def test_get_ipa_of_word_with_punctuation__word_with_hyphen_that_belongs_to_word__returns_value(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "A-B"
    res = get_ipa_of_word_with_punctuation(input_dict, input_word, "_")

    self.assertEqual("ab", res)

  def test_get_ipa_of_word_with_punctuation__word_with_apo_in_the_middle_that_is_not_in_dict__returns_underlines(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "A'B"
    res = get_ipa_of_word_with_punctuation(input_dict, input_word, "_")

    self.assertEqual("___", res)

  def test_get_ipa_of_word_with_punctuation__word_with_apo_at_beginning_and_hyphen_that_belong_to_word__returns_value(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "'A-B"
    res = get_ipa_of_word_with_punctuation(input_dict, input_word, "_")

    self.assertEqual("g", res)

  def test_get_ipa_of_word_with_punctuation__word_with_apo_atend_and_hyphen_that_belong_to_word__returns_value(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "A-B'"
    res = get_ipa_of_word_with_punctuation(input_dict, input_word, "_")

    self.assertEqual("h", res)

  def test_get_ipa_of_word_with_punctuation__word_with_apos_at_beginning_and_end_and_hyphen_that_belong_to_word__returns_value(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "'A-B'"
    res = get_ipa_of_word_with_punctuation(input_dict, input_word, "_")

    self.assertEqual("i", res)

  def test_get_ipa_of_word_with_punctuation__word_without_hyphen_or_apo_but_with_hash_and_new_line__returns_hash_value_and_new_line(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "#A\n"
    res = get_ipa_of_word_with_punctuation(input_dict, input_word, "_")

    self.assertEqual("#c\n", res)

  def test_get_ipa_of_word_with_punctuation__two_words_separated_by_punctuation_but_not_by_space_and_punctuation_at_beginning_and_end__returns_values_of_the_word_and_keeps_punctuation(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "#A#B#"
    res = get_ipa_of_word_with_punctuation(input_dict, input_word, "_")

    self.assertEqual("#c#d#", res)

  # endregion

  # region get_ipa_of_word_in_sentence

  def test_get_ipa_of_word_in_sentence__word_without_punctuation__returns_value(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "A"
    res = get_ipa_of_word_in_sentence(input_dict, input_word, "_")

    self.assertEqual("c", res)

  def test_get_ipa_of_word_in_sentence__word_with_punctuation_that_belongs_to_word__returns_value(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "'A"
    res = get_ipa_of_word_in_sentence(input_dict, input_word, "_")

    self.assertEqual("e", res)

  def test_get_ipa_of_word_in_sentence__word_with_punctuation_that_belongs_not_to_word__returns_value_and_punctuation(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "-'A-"
    res = get_ipa_of_word_in_sentence(input_dict, input_word, "_")

    self.assertEqual("-e-", res)

  # endregion

  # region sentence_to_ipa

  def test_sentence_to_ipa__senrds__return_combination_of_values(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "'A-B#'"
    res = sentence_to_ipa(input_dict, input_word, "_")

    self.assertEqual("g#'", res)

  def test_sentence_to_ipa__sentence_with_existing_words__return_combination_of_values(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "A B 'A A-B 'A-B' 'A-B#' A"
    res = sentence_to_ipa(input_dict, input_word, "_")

    self.assertEqual("c d e ab i g#' c", res)

  def test_sentence_to_ipa__sentence_with_words_not_in_dict_but_one_of_them_is_only_in_capital_letters__return_underlines_and_values_for_letters(self):
    input_dict = {"A-B": "ab", "A": "c", "B": "d", "'A": "e",
                  "B'": "f", "'A-B": "g", "A-B'": "h", "'A-B'": "i"}
    input_word = "abc BA"
    res = sentence_to_ipa(input_dict, input_word, "_")

    self.assertEqual("___ dc", res)

  # endregion


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
