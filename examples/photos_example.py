import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scraping # import ../scraping.py

# Read webpage
url = 'https://www.ilpost.it/2025/01/17/limite-due-mandati-presidenti-regione-zaia-de-luca-corte-costituzionale/'
html = scraping.read_webpage(url)

# Look for strings
strings = scraping.find_more_strings(html, '<div id="attachment_', 'alt=\"\" width=')

for i, st in enumerate(strings):
  # Look for one string
  img_src = scraping.find_string(st, 'src=\"', '\"')

  # Download image
  filepath = 'tmp/' + str(i).zfill(4) + ".jpg"
  scraping.download_image(img_src, filepath)
