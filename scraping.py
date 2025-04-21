from urllib.request import urlopen, Request
import re
import string
import sys
from os import remove

def open_url(u):
  print('Opening ' + u)
  headers = {'User-Agent' : "Mozilla/5.0"}
  try:
    response = urlopen(Request(u, headers = headers), timeout = 30)
    if(response.status == 404):
      print("Error 404")
    print('> ' + str(response.headers['Content-Length']) + ' bytes')
  except Exception as err:
    print(Exception, err)
  page = response.read()
  return page

def read_webpage(url):
  html_bytes = open_url(url)
  html = html_bytes.decode("utf-8", errors='ignore')
  return html

def download_image(u, filepath):
  with open(filepath, 'xb') as file:
    try:
      file.write(open_url(u))
      print(u + " downloaded to " + filepath)
    except Exception as err:
      print(Exception, err)
      remove(filepath)
      return False

def find_more_strings_i(text, delimiter1, delimiter2):
  rgx_all = '[\w\s]+'
  rgx1 = delimiter1 + rgx_all
  rgx2 = rgx_all + delimiter2
  res1 = [m.start() + len(delimiter1) for m in re.finditer(rgx1, text)]
  res2 = [m.start()                   for m in re.finditer(rgx2, text)]
  if(len(res1) != len(res2)):
    raise Exception("len are different: " + str(len(res1)) + ", " + str(len(res2))) 
  return res1, res2

def find_more_strings(text, delimiter1, delimiter2):
  res1, res2 = find_more_strings_i(text, delimiter1, delimiter2)
  strings = []
  for i in range(len(res1)):
    strings.append(text[res1[i]:res2[i]])
  return strings

def find_string(string, delimiter1, delimiter2):
  rgx = delimiter1 + '.*' + delimiter2
  res = re.search(rgx, string)
  if (res != None):
    res2 = res.group(0)[len(delimiter1):-len(delimiter2)]
  else:
    res2 = None
  return res2

def move_ptr(text, string, i):
  i = text.find(string, i)
  return i

def move_ptr_after(text, string, i):
  i = move_ptr(text, string, i)
  if (i != -1):
    i = i + len(string)
  return i

def find_next(text, start, begin_str, end_str):
  i_begin = move_ptr_after(text, begin_str, start)
  i_end = move_ptr(text, end_str, i_begin)
  return i_begin, i_end
