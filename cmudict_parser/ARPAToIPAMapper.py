import re

_ipa_symbols = {
  #"A": "ə",
  "AA": "ɑ",
  "AE": "æ",
  "AH": "ʌ", # ə
  "AO": "ɔ",
  "AW": "aʊ",
  "AY": "aɪ",
  "B": "b", # 
  "CH": "ʧ",
  "D": "d", # ð
  "DH": "ð",
  "EH": "ɛ",
  "ER": "ɝ", # ər
  "EY": "eɪ",
  "F": "f", #
  "G": "g", #
  "HH": "h",
  "IH": "ɪ",
  "IY": "i",
  "JH": "ʤ", # alt: d͡ʒ
  "K": "k", #
  "L": "l", #
  "M": "m", #
  "N": "n", #
  "NG": "ŋ",  
  "OW": "oʊ",
  "OY": "ɔɪ",
  "P": "p", #
  "R": "ɹ", #
  "S": "s", #
  "SH": "ʃ",
  "T": "t", #
  "TH": "θ",
  "UH": "ʊ",
  "UW": "u",
  "V": "v", #
  "W": "w", #
  "Y": "j",
  "Z": "z", #
  "ZH": "ʒ",
}

_ipa_stresses = {
  "0": "",
  "1": "ˈ",
  "2": "ˌ",
}

_ARPAbet_pattern = "([A-Z]+)(\d*)"

def get_ipa_with_stress(ARPAbet_phoneme: str) -> str:
  res = re.match(_ARPAbet_pattern, ARPAbet_phoneme)
  phon, stress = res.groups()
  ipa_phon = _ipa_symbols[phon]
  has_stress = stress != ''

  if has_stress:
    ipa_stress = _ipa_stresses[stress]
    ipa_phon = "{}{}".format(ipa_stress, ipa_phon)

  return ipa_phon
