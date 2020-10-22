import unittest

from cmudict_parser.CMUDict import get_dict


class UnitTests(unittest.TestCase):

  def test_UH(self):
    di = get_dict()
    # print(len(di))
    print(di.get_all_arpa("test"))
    print(di.get_first_ipa("test"))
    print(di.get_all_arpa("to"))
    print(di.get_all_ipa("to"))


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
