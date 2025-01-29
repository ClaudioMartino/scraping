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

def print_red(string):
  print('\033[91m' + string + '\033[0m')

def read_inches(string):
  if (string.replace('.', '', 1).isdigit()):
    # Simple number
    inch = float(string)
  elif (string.replace('&#039;', '', 1).replace('&quot;', '', 1).replace('.','').isdigit()):
    # Feet and inches (1' = 12")
    # Example: 5&#039;10&quot = 5'10"
    tmp = string.replace('&quot;', '', 1).split('&#039;')
    feet = float(tmp[0])
    inch = float(tmp[1])
    inch = feet * 12 + inch
  else:
    print_red("Can't read inches: " + string)
    inch = 'NA'
  return inch

def read_cm(string):
  if (string.replace('.', '', 1).isdigit()):
    cm = float(string)
    # Simple number
  elif (string[:-2].replace('.', '', 1).isdigit()):
    # Remove CM
    cm = float(string[:-2])
  else:
    print_red("Can't read cm: " + string)
    cm = 'NA'

  return cm

def read_inches_cm(string_inches, string_cm):
  inches = read_inches(string_inches)
  cm = read_cm(string_cm)

  if(isinstance(inches, float) and isinstance(cm, float)):
    # Sometimes cm and inch are reversed by mistake
    # Example: https://www.fashionmodeldirectory.com/models/karen_pillet/
    if(cm < inches):
      print_red("Inch and cm reversed")
      inches, cm = cm, inches

    # 1 centimeter is equal to 0.3937007874 inches
    if(abs(inches - cm * 0.3937007874) > 5):
      print_red('Inch / cm BIG mismatch: ' + str(inches) + ' - ' + str(cm) )
      inches = "NA"
      cm = "NA"

    # Check if values > 0
    if(inches <= 0):
      inches = "NA"
    if(cm <= 0):
      cm = "NA"

  return inches, cm

def data_point(string, i):
  # Look for third occurence of input string
  i = move_ptr_after(html, string, i)
  i = move_ptr_after(html, string, i)
  i = move_ptr_after(html, string, i)

  # Example:
  # <span class="DataPoint">35.5</span>
  # <span class="Separator">/</span>
  # <span class="DataPoint">90</span>

  st = "<span class=\"DataPoint\">"
  b1 = move_ptr_after(html, st, i)
  b2 = move_ptr_after(html, st, b1)
  #b3 = move_ptr_after(html, st, b2)

  st = "</span>"
  e1 = move_ptr(html, st, b1)
  e2 = move_ptr(html, st, b2)
  #e3 = move_ptr(html, st, b3)

  us_string = html[b1:e1]
  eu_string = html[b2:e2]
  #uk_string = html[b3:e3]

   # Treat dress and shoes differently, they are simpler
  inch_cm_strings = ["Height", "Bust", "Waist", "Hips"]
  if (string in inch_cm_strings):
    inch, cm = read_inches_cm(us_string, eu_string)
    return cm
  else:
    if(eu_string.isdigit()):
      return int(eu_string)
    elif(eu_string.replace('.','',1).isdigit()):
      return float(eu_string)
    elif(eu_string == ''):
      return 'NA'
    else:
      return eu_string

def hair_eyes(string, i):
  # Look for third occurence of input string
  i = move_ptr_after(html, string, i)
  i = move_ptr_after(html, string, i)
  i = move_ptr_after(html, string, i)

  # Example: <div class="Wrap">Dark brown</div>
  color = scraping.find_string(html[i:], '<div class=\"Wrap\">', '</div>')

  return color

### MAIN ###

models_per_page = 12

# Loop over letters
letters = list(string.ascii_uppercase)
print(letters)
print(len(letters))

offset = 0
for l in letters[offset:]:
  # create url list
  model_names = []
  model_urls  = []

  # Read webpages
  url_cnt = 0
  while(1):
    u = "https://www.fashionmodeldirectory.com/models/search/alphabetical_order/" + l + "/?start=" + str(url_cnt)
    html = scraping.read_webpage(u)

    # Look for models in page
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

    # Update url
    url_cnt += models_per_page

  tot_models = len(model_urls)
  print("[TOTAL] " + str(tot_models))

  # Open output file
  f = open("models" + l + ".csv", 'w')
  writer = csv.writer(f)

  # Loop over models and read features
  for cnt, url_m in enumerate(model_urls):
    print(str(cnt + 1) + "/" + str(tot_models))
    # Open web page
    # Example: "https://www.fashionmodeldirectory.com/models/toma_aardenburg/",
    html = scraping.read_webpage(url_m)

    # Read nationality
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

    # Colors
    hair = hair_eyes('Hair', i)
    eyes = hair_eyes('Eyes', i)

    # Measurements
    height_cm = data_point("Height", i)
    bust_cm   = data_point("Bust", i)
    waist_cm  = data_point("Waist", i)
    hips_cm   = data_point("Hips", i)
    dress     = data_point("Dress", i)
    shoes     = data_point("Shoes", i)

    # Write csv row
    csv_out = [model_names[cnt], model_urls[cnt], nationality, date, height_cm, bust_cm, waist_cm, hips_cm, dress, shoes, hair, eyes]
    print(csv_out)
    writer.writerow(csv_out)
 
  # Close csv file
  f.close()
