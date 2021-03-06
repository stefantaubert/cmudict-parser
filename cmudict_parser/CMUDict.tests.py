import unittest
from typing import Optional

from cmudict_parser.CMUDict import CMUDict, get_dict

cmu_dict_instance: Optional[CMUDict] = None


class UnitTests(unittest.TestCase):
  def __init__(self, methodName: str) -> None:
    global cmu_dict_instance
    if cmu_dict_instance is None:
      cmu_dict_instance = get_dict(silent=True)
    self.cmu_dict = cmu_dict_instance
    super().__init__(methodName)

  def test_sentence_to_ipa__with_caching__executes_custom_func_only_once(self):
    input_word = "xyzxyz"
    assert not self.cmu_dict.contains(input_word.upper())

    res = [self.cmu_dict.sentence_to_ipa(
      sentence=input_word,
      replace_unknown_with=lambda _: str(i),
      use_caching=True
    ) for i in range(2)]

    self.assertEqual(["0", "0"], res)

  def test_sentence_to_ipa__without_caching__executes_custom_func(self):
    input_word = "xyzxyz"
    assert not self.cmu_dict.contains(input_word.upper())

    res = [self.cmu_dict.sentence_to_ipa(
      sentence=input_word,
      replace_unknown_with=lambda _: str(i),
      use_caching=False
    ) for i in range(2)]

    self.assertEqual(["0", "1"], res)

  def test_sentence_to_ipa__uses_caching_by_default(self):
    input_word = "xyzxyz"
    assert not self.cmu_dict.contains(input_word.upper())

    res = [self.cmu_dict.sentence_to_ipa(
      sentence=input_word,
      replace_unknown_with=lambda _: str(i)
    ) for i in range(2)]

    self.assertEqual(["0", "0"], res)

  def test_len(self):
    res = len(self.cmu_dict)
    self.assertEqual(125022, res)

  def test_get_all_arpa__to(self):
    res = self.cmu_dict.get_all_arpa("to")
    self.assertEqual(['T UW1', 'T IH0', 'T AH0'], res)

  def test_get_all_ipa__to(self):
    res = self.cmu_dict.get_all_ipa("to")
    self.assertEqual(['tˈu', 'tɪ', 'tʌ'], res)

  def test_get_first_ipa__to(self):
    res = self.cmu_dict.get_first_ipa("to")
    self.assertEqual('tˈu', res)

  def test_get_first_ipa__allo(self):
    res = self.cmu_dict.get_first_ipa("'Allo")
    self.assertEqual('ˌɑlˈoʊ', res)

  def test_sentence_to_ipa_no_replace_unknown_keep_original(self):
    # should return ipa of to and keep xxl
    res = self.cmu_dict.sentence_to_ipa(
      "to to. xxl xxl.", replace_unknown_with=None, use_caching=False)

    self.assertEqual("tˈu tˈu. xxl xxl.", res)

  def test_sentence_to_ipa_replace_unknown_with_underscore(self):
    # should return ipa of to and replace xxl with ___
    res = self.cmu_dict.sentence_to_ipa(
      "to to. xxl xxl.", replace_unknown_with="_", use_caching=False)

    self.assertEqual("tˈu tˈu. ___ ___.", res)

  def test_sentence_to_ipa_replace_unknown_with_nothing(self):
    # should return ipa of to and replace xxl with empty string (but keep space in between)
    res = self.cmu_dict.sentence_to_ipa(
      "to to. xxl xxl.", replace_unknown_with="", use_caching=False)

    self.assertEqual("tˈu tˈu.  .", res)

  def test_sentence_to_ipa_replace_unknown_with_custom_func(self):
    # should return ipa of to and keep xxl with an added X
    res = self.cmu_dict.sentence_to_ipa(
      "to to. xxl xxl.", replace_unknown_with=lambda x: x + "X", use_caching=False)

    self.assertEqual("tˈu tˈu. xxlX xxlX.", res)

  def test_sentence_to_ipa__double_space__is_kept(self):
    # should return ipa of to with a double space in between
    res = self.cmu_dict.sentence_to_ipa("to  to", replace_unknown_with="_", use_caching=False)

    self.assertEqual("tˈu  tˈu", res)

  def test_sentence_to_ipa__single_punctuation__is_kept(self):
    # should return .
    res = self.cmu_dict.sentence_to_ipa(".", replace_unknown_with="_", use_caching=False)

    self.assertEqual(".", res)

  def test_sentence_to_ipa__too_long_replacement__throws_exception(self):
    # should throw exception
    try:
      self.cmu_dict.sentence_to_ipa("ewjoigf", replace_unknown_with="__", use_caching=False)
      self.fail()
    except Exception as e:
      self.assertEqual("Parameter replace_unknown_with can only be 0 or 1 char.", e.args[0])

  def test_sentence_to_ipa__minus_sign(self):
    # should return ipa of to with hyphen in between
    res = self.cmu_dict.sentence_to_ipa("to-to-to", replace_unknown_with="_", use_caching=False)

    self.assertEqual("tˈu-tˈu-tˈu", res)

  def test_sentence_to_ipa__minus_sign_different_words(self):
    # should return ipa of the single words with hyphen in between
    res = self.cmu_dict.sentence_to_ipa("to-no-so", replace_unknown_with="_", use_caching=False)

    self.assertEqual("tˈu-nˈoʊ-sˈoʊ", res)

  def test_sentence_to_ipa__closing_parenthesis(self):
    # should return ipa of to with ) at end
    res = self.cmu_dict.sentence_to_ipa("to to)", replace_unknown_with="_", use_caching=False)

    self.assertEqual("tˈu tˈu)", res)

  def test_sentence_to_ipa__opening_parenthesis(self):
    # should return ipa of to with ( at beginning
    res = self.cmu_dict.sentence_to_ipa("(to to", replace_unknown_with="_", use_caching=False)

    self.assertEqual("(tˈu tˈu", res)

  def test_sentence_to_ipa__minus_is_kept(self):
    # should return hyphen
    res = self.cmu_dict.sentence_to_ipa("-", replace_unknown_with="_", use_caching=False)

    self.assertEqual("-", res)

  def test_sentence_to_ipa__single_quotation_mark_is_kept(self):
    # should return ipa of to with ' at beginning
    res = self.cmu_dict.sentence_to_ipa("'to", replace_unknown_with="_", use_caching=False)

    self.assertEqual("'tˈu", res)

  def test_sentence_to_ipa__double_quotation_mark_is_kept(self):
    # should return ipa of to with \" at beginning
    res = self.cmu_dict.sentence_to_ipa("\"to", replace_unknown_with="_", use_caching=False)

    self.assertEqual("\"tˈu", res)

  def test_sentence_to_ipa__minus_sign_and_parenthesis(self):
    # should return ipa of to with hyphens in between and parenthesis at beginning and end
    res = self.cmu_dict.sentence_to_ipa("(to-to-to)", replace_unknown_with="_", use_caching=False)

    self.assertEqual("(tˈu-tˈu-tˈu)", res)

  def test_sentence_to_ipa__double_punctuation_marks(self):
    # should return ipa of to with double hyphens in between and double parenthesis at beginning and end
    res = self.cmu_dict.sentence_to_ipa(
      "((to--to--to))", replace_unknown_with="_", use_caching=False)

    self.assertEqual("((tˈu--tˈu--tˈu))", res)

  def test_sentence_to_ipa__big_letter_abbreviation(self):
    # should return the ipa of every single letter
    res = self.cmu_dict.sentence_to_ipa("PRS", replace_unknown_with="_", use_caching=False)

    self.assertEqual("pˈiˈɑɹˈɛs", res)

  def test_sentence_to_ipa__big_letter_abbreviation_with_punctuation(self):
    # should return the ipa of every single letter with \" at beginning
    res = self.cmu_dict.sentence_to_ipa("\"PRS)", replace_unknown_with="_", use_caching=False)

    self.assertEqual("\"pˈiˈɑɹˈɛs)", res)

  def test_sentence_to_ipa__small_letter_abbreviation_is_not_replaced(self):
    # should return _ for every single letter
    res = self.cmu_dict.sentence_to_ipa("prs", replace_unknown_with="_", use_caching=False)

    self.assertEqual("___", res)

  def test_sentence_to_ipa__mix_of_different_scenarios(self):
    # should keep the punctuation at the corresponding places, return the ipa of to, the ipa of every single letter in PRS and replace every letter of xxl with _
    res = self.cmu_dict.sentence_to_ipa(
      "((to-?PRS --to xxl))", replace_unknown_with="_", use_caching=False)

    self.assertEqual("((tˈu-?pˈiˈɑɹˈɛs --tˈu ___))", res)

  def test_sentence_to_ipa__allo(self):
    # should get the ipa of 'Allo, no apostrophe should be in ipa
    res = self.cmu_dict.sentence_to_ipa("'Allo", replace_unknown_with="_", use_caching=False)

    self.assertEqual('ˌɑlˈoʊ', res)

  def test_sentence_to_ipa__theyre(self):
    # should get the ipa of they're, no apostrophe should be in ipa
    res = self.cmu_dict.sentence_to_ipa("they're", replace_unknown_with="_", use_caching=False)

    self.assertEqual('ðˈɛɹ', res)

  def test_sentence_to_ipa__cat_o_nine_tails(self):
    # cat-o-nine-tails is really a single word in the dictionary, should return its ipa
    res = self.cmu_dict.sentence_to_ipa(
      "cat-o-nine-tails", replace_unknown_with="_", use_caching=False)

    self.assertEqual('kˈætoʊnˌaɪntˌeɪlz', res)

  def test_sentence_to_ipa__to_cat_o_nine_tails_to(self):
    # should return ipa of to, hyphen, ipa of cat-o-nine-tails, hyphen, ipa of to
    res = self.cmu_dict.sentence_to_ipa(
      "to-cat-o-nine-tails-to", replace_unknown_with="_", use_caching=False)

    self.assertEqual('tˈu-kˈætoʊnˌaɪntˌeɪlz-tˈu', res)

  def test_sentence_to_ipa__ha_ha_ha(self):
    # ha-ha-ha is a word in the dictionary, herefore no hyphen should appear in ipa
    res = self.cmu_dict.sentence_to_ipa("ha-ha-ha", replace_unknown_with="_", use_caching=False)

    self.assertEqual('hˌɑhˌɑhˈɑ', res)

  def test_sentence_to_ipa__day_by_day_to_day(self):
    # day-by-day and day-to-day are both words in the dictionary
    # the code should recognize day-by-day as a word and not day-to-day
    # therefore should return ipa of day-by-day (with no hyphen), hyphen, ipa of to, hyphen, ipa of day
    res = self.cmu_dict.sentence_to_ipa(
      "day-by-day-to-day", replace_unknown_with="_", use_caching=False)

    self.assertEqual('dˈeɪbaɪdˌeɪ-tˈu-dˈeɪ', res)

  def test_sentence_to_ipa__end_inner_quote(self):
    # 'end-inner-qoute is a word in the dictionary, therefore no ' should appear in ipa
    res = self.cmu_dict.sentence_to_ipa(
      "'end-inner-quote", replace_unknown_with="_", use_caching=False)

    self.assertEqual("ˈɛndˈɪnɝkwˈoʊt", res)

  def test_sentence_to_ipa__non_smokers(self):
    # non-smokers' is a word in the dictionary, therefore no ' should appear in ipa
    res = self.cmu_dict.sentence_to_ipa("non-smokers'", replace_unknown_with="_", use_caching=False)

    self.assertEqual('nˈɑnsmˈoʊkɝz', res)

  def test_sentence_to_ipa__cat_o_nine_tails_to_with_punctuation(self):
    # should return apostrophe and ipa of cat-o-nine-tails-to
    res = self.cmu_dict.sentence_to_ipa(
      "'cat-o-nine-tails-to", replace_unknown_with="_", use_caching=False)

    self.assertEqual("'kˈætoʊnˌaɪntˌeɪlz-tˈu", res)

  def test_sentence_to_ipa__apos(self):
    # should return apostrophe
    res = self.cmu_dict.sentence_to_ipa("'", replace_unknown_with="_", use_caching=False)

    self.assertEqual("'", res)

  def test_sentence_to_ipa__sentence_with_apos(self):
    # all apostrophes in the sentence should not appear in the ipa as they belong to the words
    res = self.cmu_dict.sentence_to_ipa(
      "'Allo, to they're?", replace_unknown_with="_", use_caching=False)

    self.assertEqual("ˌɑlˈoʊ, tˈu ðˈɛɹ?", res)

  def test_sentence_to_ipa__theyre_with_apos_at_beginning_and_question_mark_at_end(self):
    # should return apostrophe and ipa of they're
    res = self.cmu_dict.sentence_to_ipa("'they're?", replace_unknown_with="_", use_caching=False)

    self.assertEqual("'ðˈɛɹ?", res)

  def test_sentence_to_ipa__theyre_with_apos_at_beginning_and_end(self):
    # should return ipa of they're with apostrophes at beginning and end
    res = self.cmu_dict.sentence_to_ipa("'they're'", replace_unknown_with="_", use_caching=False)

    self.assertEqual("'ðˈɛɹ'", res)

  def test_sentence_to_ipa__allo_with_apos_at_end(self):
    # should return ipa of 'Allo with apostrophe at end
    res = self.cmu_dict.sentence_to_ipa("'Allo'", replace_unknown_with="_", use_caching=False)

    self.assertEqual("ˌɑlˈoʊ'", res)

  def test_sentence_to_ipa__stones_genitive(self):
    # stones' is a word in the dictionary, no apostrophe should appear in ipa
    res = self.cmu_dict.sentence_to_ipa("stones'", replace_unknown_with="_", use_caching=False)

    self.assertEqual("stˈoʊnz", res)

  def test_sentence_to_ipa__stones_genitive_with_apos_at_beginning(self):
    # stones' is a word in the dictionary, therefore only apostrophe at beginning should appear in ipa
    res = self.cmu_dict.sentence_to_ipa("'stones'", replace_unknown_with="_", use_caching=False)

    self.assertEqual("'stˈoʊnz", res)

  def test_sentence_to_ipa__no_brainer(self):
    # no-brainer is a word in the dictionary, therefore the hyphen should not appear in ipa
    res = self.cmu_dict.sentence_to_ipa("no-brainer", replace_unknown_with="_", use_caching=False)

    self.assertEqual("nˌoʊbɹˈeɪnɝ", res)

  def test_sentence_to_ipa__etc(self):
    # dict only contains ETC but not ETC.
    res = self.cmu_dict.sentence_to_ipa("etc.", replace_unknown_with="_", use_caching=False)

    self.assertEqual("ˌɛtsˈɛtɝʌ.", res)

  def test_sentence_to_ipa__word_with_hyphen_and_newline_at_end(self):
    # should return ipa of no-brainer and \n at end
    res = self.cmu_dict.sentence_to_ipa("no-brainer\n", replace_unknown_with="_", use_caching=False)

    self.assertEqual("nˌoʊbɹˈeɪnɝ\n", res)

  def test_sentence_to_ipa__normal_word_and_newline_at_end(self):
    # should return ipa of no and \n at end
    res = self.cmu_dict.sentence_to_ipa("no\n", replace_unknown_with="_", use_caching=False)

    self.assertEqual("nˈoʊ\n", res)

  def test_sentence_to_ipa__normal_word_and_hyphen_and_newline_at_end(self):
    # should return ipa of no, followed by -\n
    res = self.cmu_dict.sentence_to_ipa("no-\n", replace_unknown_with="_", use_caching=False)

    self.assertEqual("nˈoʊ-\n", res)

  def test_sentence_to_ipa__sentence_with_commas(self):
    # should keep the commas and return the ipa of all the words
    res = self.cmu_dict.sentence_to_ipa(
      "it is not a real gain, for the modern printer throws the gain away by putting inordinately wide spaces between his lines, which, probably,", replace_unknown_with="_", use_caching=False)

    self.assertEqual(
      "ˈɪt ˈɪz nˈɑt ʌ ɹˈil gˈeɪn, fˈɔɹ ðʌ mˈɑdɝn pɹˈɪntɝ θɹˈoʊz ðʌ gˈeɪn ʌwˈeɪ bˈaɪ pˈʌtɪŋ ˌɪnˈɔɹdʌnʌtli wˈaɪd spˈeɪsʌz bɪtwˈin hˈɪz lˈaɪnz, wˈɪʧ, pɹˈɑbʌblˌi,", res)

  def test_sentence_to_ipa__ipa_of_number(self):
    # should return _, as 1 is not in the dictionary
    res = self.cmu_dict.sentence_to_ipa("1", replace_unknown_with="_", use_caching=False)

    self.assertEqual("_", res)

  def test_sentence_to_ipa__big_letter_and_number(self):
    # should return __ as A1 is not in the dictionary (it should be treated as a single word, not like in big letter abbreviation)
    res = self.cmu_dict.sentence_to_ipa("A1", replace_unknown_with="_", use_caching=False)

    self.assertEqual("__", res)

  def test_get_first_ipa__theyre(self):
    res = self.cmu_dict.get_first_ipa("they're")
    self.assertEqual('ðˈɛɹ', res)

  def test_sentence_to_ipa__sentence_with_word_ending_with_apo_and_two_hyphen(self):
    # should return ipa of the words and keep punctuation
    res = self.cmu_dict.sentence_to_ipa(
      "\"'Whose name is'--", replace_unknown_with="_", use_caching=False)

    self.assertEqual("\"'hˈuz nˈeɪm ˈɪz'--", res)

  def test_sentence_to_ipa__sentence_with_word_with_apo_and_two_hyphen_followed_by_another_word(self):
    # should return ipa of the words and keep punctuation
    res = self.cmu_dict.sentence_to_ipa(
      "\"'Whose name is'--is'", replace_unknown_with="_", use_caching=False)

    self.assertEqual("\"'hˈuz nˈeɪm ˈɪz'--ˈɪz'", res)

  def test_sentence_to_ipa__sentence_with_words_with_different_apo_combinations(self):
    # should return ipa of the words and keep punctuation
    res = self.cmu_dict.sentence_to_ipa(
      "\"'Whose'-'stones'''-'Allo''", replace_unknown_with="_", use_caching=False)

    self.assertEqual("\"'hˈuz'-'stˈoʊnz''-ˌɑlˈoʊ''", res)

  def test_sentence_to_ipa__sentence_with_words_with_apos_belonging_to_the_word_but_some_are_not_in_dict__plus_combination_of_apo_and_hyphens_between_words(self):
    # should return ipa of the words which are in dict and keep punctuation where it does not belong to any word
    res = self.cmu_dict.sentence_to_ipa(
      "Suckin'--I mean helpin' people an' fightin' an' all that.", replace_unknown_with="_")

    self.assertEqual("_______--ˈaɪ mˈin ______' pˈipʌl ˈæn' fˈaɪtɪn ˈæn' ˈɔl ðˈæt.", res)

  def test_sentence_to_ipa__sentence_with_words_with_apos_belonging_to_the_word_but_some_are_not_in_dict__plus_combination_of_apo_and_hyphens_between_words2(self):
    # should return ipa of the words which are in dict and keep punctuation where it does not belong to any word
    res = self.cmu_dict.sentence_to_ipa(
      "Fightin'--I mean helpin' people an' suckin' an' all that.", replace_unknown_with="_")

    self.assertEqual("fˈaɪtɪn--ˈaɪ mˈin ______' pˈipʌl ˈæn' ______' ˈæn' ˈɔl ðˈæt.", res)

  def test_sentence_to_ipa__sentence_with_words_with_hypen_in_which_parts_are_unknown(self):
    # should return _ in the length of the unknown parts, keep the hyphens and return ipa for the known words
    res = self.cmu_dict.sentence_to_ipa(
      "higgledy-piggledy, myself-piggledy, higgledy-i", replace_unknown_with="_")

    self.assertEqual("________-________, mˌaɪsˈɛlf-________, ________-ˈaɪ", res)

  def test_sentence_to_ipa__sentence_with_words_with_double_hypen_in_which_parts_are_unknown(self):
    # should return _ in the length of the unknown parts, keep the double hyphens and return ipa for the known words
    res = self.cmu_dict.sentence_to_ipa(
      "higgledy--piggledy, myself--piggledy, higgledy--i", replace_unknown_with="_")

    self.assertEqual("________--________, mˌaɪsˈɛlf--________, ________--ˈaɪ", res)


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
