import re
from typing import Dict

ARPABET_IPA_MAP: Dict[str, str] = {
  # "A": "ə",
  "AA": "ɑ",
  "AE": "æ",
  "AH": "ʌ",  # ə
  "AO": "ɔ",
  "AW": "aʊ",
  "AY": "aɪ",
  "B": "b",
  "CH": "ʧ",
  "D": "d",  # ð
  "DH": "ð",
  "EH": "ɛ",
  "ER": "ɝ",  # ər
  "EY": "eɪ",
  "F": "f",
  "G": "g",
  "HH": "h",
  "IH": "ɪ",
  "IY": "i",
  "JH": "ʤ",  # alt: d͡ʒ
  "K": "k",
  "L": "l",
  "M": "m",
  "N": "n",
  "NG": "ŋ",
  "OW": "oʊ",
  "OY": "ɔɪ",
  "P": "p",
  "R": "ɹ",
  "S": "s",
  "SH": "ʃ",
  "T": "t",
  "TH": "θ",
  "UH": "ʊ",
  "UW": "u",
  "V": "v",
  "W": "w",
  "Y": "j",
  "Z": "z",
  "ZH": "ʒ",
}

IPA_STRESSES: Dict[str, str] = {
  "0": "",
  "1": "ˈ",
  "2": "ˌ",
}

ARPABET_PATTERN: str = re.compile(r"([A-Z]+)(\d*)")


def get_ipa_with_stress(ARPAbet_phoneme: str) -> str:
  res = re.match(ARPABET_PATTERN, ARPAbet_phoneme)
  phon, stress = res.groups()
  ipa_phon = ARPABET_IPA_MAP[phon]
  has_stress = stress != ''

  if has_stress:
    ipa_stress = IPA_STRESSES[stress]
    ipa_phon = f"{ipa_stress}{ipa_phon}"

  return ipa_phon
