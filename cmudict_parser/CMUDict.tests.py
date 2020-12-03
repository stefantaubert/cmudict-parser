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

  def test_get_first_ipa__allo(self):
    res = self.cmu_dict.get_first_ipa("'Allo")
    self.assertEqual('ˌɑlˈoʊ', res)

  def test_get_first_ipa__theyre(self):
    res = self.cmu_dict.get_first_ipa("they're")
    self.assertEqual('ðˈɛɹ', res)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
