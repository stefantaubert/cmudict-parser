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


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
