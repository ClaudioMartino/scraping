import scraping

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
