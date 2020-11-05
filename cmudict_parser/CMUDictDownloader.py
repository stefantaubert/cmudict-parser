import os
from typing import Tuple

import wget

BASE_NAME = "cmudict-0.7b"
SYMBOLS_FILENAME = BASE_NAME + ".symbols"
PHOES_FILENAME = BASE_NAME + ".phones"
DICT_FILENAME = BASE_NAME
BASE_URL = "http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/"
URL_SYMBOLS = BASE_URL + SYMBOLS_FILENAME
URL_PHONES = BASE_URL + PHOES_FILENAME
URL_DICT = BASE_URL + DICT_FILENAME

def ensure_files_are_downloaded(folder: str) -> Tuple[str, str, str]:
  symbols_path = os.path.join(folder, SYMBOLS_FILENAME)
  phones_path = os.path.join(folder, PHOES_FILENAME)
  dict_path = os.path.join(folder, DICT_FILENAME)

  os.makedirs(folder, exist_ok=True)

  if not os.path.exists(symbols_path):
    print("Downloading", URL_SYMBOLS)
    wget.download(URL_SYMBOLS, folder)

  if not os.path.exists(phones_path):
    print("Downloading", URL_PHONES)
    wget.download(URL_PHONES, folder)

  if not os.path.exists(dict_path):
    print("Downloading", URL_DICT)
    wget.download(URL_DICT, folder)

  return (symbols_path, phones_path, dict_path)
