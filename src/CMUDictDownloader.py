import os
import wget

base_name = "cmudict-0.7b"
symbols_filename = base_name + ".symbols"
phones_filename = base_name + ".phones"
dict_filename = base_name
base_url = "http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/"
url_symbols = base_url + symbols_filename
url_phones = base_url + phones_filename
url_dict = base_url + dict_filename

def ensure_files_are_downloaded(folder: str):
  symbols_path = os.path.join(folder, symbols_filename)
  phones_path = os.path.join(folder, phones_filename)
  dict_path = os.path.join(folder, dict_filename)
  
  os.makedirs(folder, exist_ok=True)

  if not os.path.exists(symbols_path):
    print("Downloading", url_symbols)
    wget.download(url_symbols, folder)

  if not os.path.exists(phones_path):
    print("Downloading", url_phones)
    wget.download(url_phones, folder)

  if not os.path.exists(dict_path):
    print("Downloading", url_dict)
    wget.download(url_dict, folder)

  return (symbols_path, phones_path, dict_path)