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

  def test_sentence_to_ipa_no_replace_unknown_keep_original(self):
    res = self.cmu_dict.sentence_to_ipa("to to. xxl xxl.", replace_unknown_with=None)

    self.assertEqual("tˈu tˈu. xxl xxl.", res)

  def test_sentence_to_ipa_replace_unknown_with_underscore(self):
    res = self.cmu_dict.sentence_to_ipa("to to. xxl xxl.", replace_unknown_with="_")

    self.assertEqual("tˈu tˈu. ___ ___.", res)

  def test_sentence_to_ipa_replace_unknown_with_nothing(self):
    res = self.cmu_dict.sentence_to_ipa("to to. xxl xxl.", replace_unknown_with="")

    self.assertEqual("tˈu tˈu.  .", res)

  def test_sentence_to_ipa_replace_unknown_with_custom_func(self):
    res = self.cmu_dict.sentence_to_ipa("to to. xxl xxl.", replace_unknown_with=lambda x: x + "X")

    self.assertEqual("tˈu tˈu. xxlX xxlX.", res)

  def test_sentence_to_ipa__double_space__is_kept(self):
    res = self.cmu_dict.sentence_to_ipa("to  to", replace_unknown_with="_")

    self.assertEqual("tˈu  tˈu", res)

  def test_sentence_to_ipa__single_punctuation__is_kept(self):
    res = self.cmu_dict.sentence_to_ipa(".", replace_unknown_with="_")

    self.assertEqual(".", res)

  def test_sentence_to_ipa__too_long_replacement__throws_exception(self):
    try:
      self.cmu_dict.sentence_to_ipa("to", replace_unknown_with="__")
      self.fail()
    except Exception as e:
      self.assertEqual("Parameter replace_unknown_with can only be 0 or 1 char.", e.args[0])

  def test_sentence_to_ipa__minus_sign(self):
    res = self.cmu_dict.sentence_to_ipa("to-to-to", replace_unknown_with="_")

    self.assertEqual("tˈu-tˈu-tˈu", res)

  def test_sentence_to_ipa__minus_sign_different_words(self):
    res = self.cmu_dict.sentence_to_ipa("to-no-so", replace_unknown_with="_")

    self.assertEqual("tˈu-nˈoʊ-sˈoʊ", res)

  def test_sentence_to_ipa__closing_parenthesis(self):
    res = self.cmu_dict.sentence_to_ipa("to to)", replace_unknown_with="_")

    self.assertEqual("tˈu tˈu)", res)

  def test_sentence_to_ipa__opening_parenthesis(self):
    res = self.cmu_dict.sentence_to_ipa("(to to", replace_unknown_with="_")

    self.assertEqual("(tˈu tˈu", res)

  def test_get_ipa_of_word_in_sentence__minus_is_kept(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("-", replace_unknown_with="_")

    self.assertEqual("-", res)

  def test_get_ipa_of_word_in_sentence__single_quotation_mark_is_kept(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("'to", replace_unknown_with="_")

    self.assertEqual("'tˈu", res)

  def test_get_ipa_of_word_in_sentence__double_quotation_mark_is_kept(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("\"to", replace_unknown_with="_")

    self.assertEqual("\"tˈu", res)

  def test_get_ipa_of_word_in_sentence__minus_sign_and_parenthesis(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("(to-to-to)", replace_unknown_with="_")

    self.assertEqual("(tˈu-tˈu-tˈu)", res)

  def test_get_ipa_of_word_in_sentence__double_punctuation_marks(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("((to--to--to))", replace_unknown_with="_")

    self.assertEqual("((tˈu--tˈu--tˈu))", res)

  def test_get_ipa_of_word_in_sentence__big_letter_abbreviation(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("PRS", replace_unknown_with="_")

    self.assertEqual("pˈiˈɑɹˈɛs", res)

  def test_get_ipa_of_word_in_sentence__big_letter_abbreviation_with_punctuation(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("\"PRS)", replace_unknown_with="_")

    self.assertEqual("\"pˈiˈɑɹˈɛs)", res)

  def test_get_ipa_of_word_in_sentence__small_letter_abbreviation_is_not_replaced(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("prs", replace_unknown_with="_")

    self.assertEqual("___", res)

  def test_sentence_to_ipa__mix_of_different_scenarios(self):
    res = self.cmu_dict.sentence_to_ipa("((to-?PRS --to xxl))", replace_unknown_with="_")

    self.assertEqual("((tˈu-?pˈiˈɑɹˈɛs --tˈu ___))", res)

  def test_get_first_ipa__allo(self):
    res = self.cmu_dict.get_first_ipa("'Allo")
    self.assertEqual('ˌɑlˈoʊ', res)

  def test_get_first_ipa__theyre(self):
    res = self.cmu_dict.get_first_ipa("they're")
    self.assertEqual('ðˈɛɹ', res)

  def test_get_ipa_of_word_in_sentence__allo(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("'Allo", replace_unknown_with="_")
    self.assertEqual('ˌɑlˈoʊ', res)

  def test_get_ipa_of_word_in_sentence__theyre(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("they're", replace_unknown_with="_")
    self.assertEqual('ðˈɛɹ', res)

  def test_get_ipa_of_word_in_sentence__cat_o_nine_tails(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("cat-o-nine-tails", replace_unknown_with="_")
    self.assertEqual('kˈætoʊnˌaɪntˌeɪlz', res)

  def test_get_ipa_of_word_in_sentence__to_cat_o_nine_tails_to(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("to-cat-o-nine-tails-to", replace_unknown_with="_")
    self.assertEqual('tˈu-kˈætoʊnˌaɪntˌeɪlz-tˈu', res)

  def test_get_ipa_of_word_in_sentence__ha_ha_ha(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("ha-ha-ha", replace_unknown_with="_")
    self.assertEqual('hˌɑhˌɑhˈɑ', res)

  def test_get_ipa_of_word_in_sentence__day_by_day_to_day(self):
    # day-by-day and day-to-day are both words in the dictionary
    # the code should recognize day-by-day as a word and not day-to-day
    res = self.cmu_dict.get_ipa_of_word_in_sentence("day-by-day-to-day", replace_unknown_with="_")
    self.assertEqual('dˈeɪbaɪdˌeɪ-tˈu-dˈeɪ', res)

  def test_get_ipa_of_word_in_sentence__end_inner_quote(self):
    # this is really in the dictionary
    res = self.cmu_dict.get_ipa_of_word_in_sentence("'end-inner-quote", replace_unknown_with="_")
    self.assertEqual("ˈɛndˈɪnɝkwˈoʊt", res)

  def test_get_ipa_of_word_in_sentence__non_smokers(self):
    # this is really in the dictionary
    res = self.cmu_dict.get_ipa_of_word_in_sentence("non-smokers'", replace_unknown_with="_")
    self.assertEqual('nˈɑnsmˈoʊkɝz', res)

  def test_get_ipa_of_word_in_sentence__cat_o_nine_tails_to_with_punctuation(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("'cat-o-nine-tails-to", replace_unknown_with="_")
    self.assertEqual("'kˈætoʊnˌaɪntˌeɪlz-tˈu", res)

  def test_get_ipa_of_word_in_sentence__apos(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("'", replace_unknown_with="_")
    self.assertEqual("'", res)

  def test_sentence_to_ipa__sentence_with_apos(self):
    res = self.cmu_dict.sentence_to_ipa("'Allo, to they're?", replace_unknown_with="_")
    self.assertEqual("ˌɑlˈoʊ, tˈu ðˈɛɹ?", res)

  def test_get_ipa_of_word_in_sentence__theyre_with_apos_at_beginning_and_question_mark_at_end(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("'they're?", replace_unknown_with="_")
    self.assertEqual("'ðˈɛɹ?", res)

  def test_get_ipa_of_word_in_sentence__theyre_with_apos_at_beginning_and_end(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("'they're'", replace_unknown_with="_")
    self.assertEqual("'ðˈɛɹ'", res)

  def test_get_ipa_of_word_in_sentence__allo_with_apos_at_end(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("'Allo'", replace_unknown_with="_")
    self.assertEqual("ˌɑlˈoʊ'", res)

  def test_get_ipa_of_word_in_sentence__stones_genitive(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("stones'", replace_unknown_with="_")
    self.assertEqual("stˈoʊnz", res)

  def test_get_ipa_of_word_in_sentence__stones_genitive_with_apos_at_beginning(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("'stones'", replace_unknown_with="_")
    self.assertEqual("'stˈoʊnz", res)

  def test_get_ipa_of_word_in_sentence__no_brainer(self):
    res = self.cmu_dict.get_ipa_of_word_in_sentence("no-brainer", replace_unknown_with="_")
    self.assertEqual("nˌoʊbɹˈeɪnɝ", res)

  def test_sentence_to_ipa__etc(self):
    # dict only contains ETC but not ETC.
    res = self.cmu_dict.sentence_to_ipa("etc.", replace_unknown_with="_")
    self.assertEqual("ˌɛtsˈɛtɝʌ.", res)

  def test_sentence_to_ipa__newline_at_end(self):
    res = self.cmu_dict.sentence_to_ipa("no-brainer\n", replace_unknown_with="_")
    self.assertEqual("nˌoʊbɹˈeɪnɝ\n", res)


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
