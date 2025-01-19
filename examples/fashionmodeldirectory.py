import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scraping # import ../scraping.py
import csv
import string

def move_ptr(text, string, i):
  i = text.find(string, i)
  return i

def move_ptr_after(text, string, i):
  i = move_ptr(text, string, i)
  if (i != -1):
    i = i + len(string)
  return i

def inch_cm(string, i):
  # Look for third
  i = move_ptr_after(html, string, i)
  i = move_ptr_after(html, string, i)
  i = move_ptr_after(html, string, i)

  string = "<span class=\"DataPoint\">"
  i = move_ptr_after(html, string, i)
  i3 = move_ptr(html, string, i)
  i3 = i3 + len(string)
  string = "</span>"
  i2 = move_ptr(html, string, i)
  i4 = move_ptr(html, string, i3)

  # Inches
  if (html[i:i2].replace('.', '', 1).isdigit()):
    inch = (float(html[i:i2]))
  else:
    inch = 0

  # Centimeters
  if (html[i3:i4].replace('.', '', 1).isdigit()):
    cm = (float(html[i3:i4]))
  elif (html[i3:i4-2].replace('.', '', 1).isdigit()):
    cm = (float(html[i3:i4-2]))
  else:
    cm = 0

  return [inch, cm]





### MAIN ###

models_per_page = 12

letters = list(string.ascii_uppercase)
offset = 23

# Loop over letters
for l in letters[offset:]:
  # create url list
  model_names = []
  model_urls  = []

  # Read all webpages
  url_cnt = 0
  while(1):
    u = "https://www.fashionmodeldirectory.com/models/search/alphabetical_order/" + l + "/?start=" + str(url_cnt)
    html = scraping.read_webpage(u)

    strings = scraping.find_more_strings(html, '<article class=\"PhotoModule TitleInside', '</article>')

    for st in strings:
      model_name = scraping.find_string(st, '<h3 itemprop=\"accountablePerson\">', '</h3>')
      url = scraping.find_string(st, '<div class="Link"><a href=\"', '\" itemprop=\"url\">')
      url = "https:" + url
      print(model_name + ": " + url)
      model_urls.append(url)
      model_names.append(model_name)

    # We stop when the page contains less than 12 models, or we are in an error page with 0 models
    if len(strings) != models_per_page:
      break

    # This works, too, but it is spaghetti code
    #i=0
    #cnt = 0
    #while(cnt < models_per_page):
    #  # Look for names and url of models
    #  string="<article class=\"PhotoModule TitleInside"
    #  i = move_ptr_after(html, string, i)
    #  if (i == -1):
    #    break
    #  string="<div class=\"Link\"><a href=\""
    #  i = move_ptr_after(html, string, i)
    #  string="\" itemprop=\"url\">"
    #  i2 = move_ptr(html, string, i)
    #  url = "https:" + html[i:i2]
    #  i = i2 + len(string)
    #  string="</a></div>"
    #  i2 = move_ptr(html, string, i)
    #  model_name = html[i:i2]
    #  print(model_name + ": " + url)
    #  model_urls.append(url)
    #  model_names.append(model_name)
    #  cnt = cnt + 1
    #if cnt != models_per_page:
    #  break

    url_cnt += models_per_page

  f = open("models" + l + ".csv", 'w')
  writer = csv.writer(f)

  for cnt, url_m in enumerate(model_urls):
    # Example: "https://www.fashionmodeldirectory.com/models/toma_aardenburg/",
    html = scraping.read_webpage(url_m)

    # Nationality
    string = "<div class=\"Nationality\" itemprop=\"nationality\">"
    nationality = scraping.find_string(html, string, '</div>')

    # Birthdate
    date = scraping.find_string(html, '<div itemprop="birthDate">Born ', '</div>')
    if(date == None):
      date = "NA"

    # Look for second ModelMeasurements (if there it is)
    string = "ModelMeasurements"
    i = 0
    i = move_ptr(html, string, i)
    tmp = move_ptr(html, string, i + len(string))
    if tmp != -1:
      i = tmp

    # Measurements
    [height_inch, height_cm] = inch_cm("Height", i)
    [bust_inch, bust_cm]     = inch_cm("Bust", i)
    [waist_inch, waist_cm]   = inch_cm("Waist", i)
    [hips_inch, hips_cm]     = inch_cm("Hips", i)

    # Write csv row
    csv_out = [model_names[cnt], model_urls[cnt], nationality, date, height_cm, bust_cm, waist_cm, hips_cm]
    writer.writerow(csv_out)
    print(csv_out)
  
  f.close()
