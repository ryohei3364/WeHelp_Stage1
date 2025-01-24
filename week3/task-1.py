import urllib.request, json, re, csv

Taipei_Tourist_Link_1 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
Taipei_Tourist_Link_2 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

def load_json(url):
  '''load datas from links and prepare to be loaded'''
  with urllib.request.urlopen(url) as url:
      result = json.load(url)
      return result

def arrange_data_1(data_1):
  '''invoke load_json function to load data and arrange raw data from scratch'''
  spot_titles = []
  longitudes = []
  latitudes = []
  serial_list_1 = []
  file_list = []

  for line in data_1["data"]["results"]:
      spot_titles.append(line['stitle']) # SpotTitle
      longitudes.append(line['longitude']) # Longitude
      latitudes.append(line['latitude']) # Latitude
      serial_list_1.append(line['SERIAL_NO']) # District
      file_list.append(line['filelist']) # ImageURL

  return spot_titles, longitudes, latitudes, serial_list_1, file_list

def get_image_urls(file_list):
  '''use regex expression to extract the first url link of images from each line'''
  image_urls = []

  for line in file_list:
    pattern = r'https?:\/\/\S+?\.(?:jpg|jpeg|png|gif)'
    match = re.findall(pattern, str(line), re.I)
    image_urls.append(match[0])
  return image_urls

def sort_data_2(data_2):
  '''Resort data2 with the same sort as data_1'''
  '''data_2: dict -> list -> dict'''

  # create the serial_no list of data_2
  serial_list_2 = [line['SERIAL_NO'] for line in data_2["data"]]

  # search the index of serial_no_list_2 and make two lists with the same sort
  serial_2_indices = [serial_list_2.index(item) for item in serial_list_1 if item in serial_list_2]

  # resort the date_2
  sorted_data_2 = [data_2["data"][index] for index in serial_2_indices]
  return sorted_data_2

def arrange_data_2(sorted_data_2):

  mrt_names = []
  districts = []

  for line in sorted_data_2:
      mrt_names.append(line['MRT']) # StationName
      districts.append(line['address'][4:8].strip()) # District
  return mrt_names, districts

def combine_spot_file():
  '''combine keywords and save file'''
  spot_file = []

  for index in range(len(spot_titles)):
     spot_file.append([
        spot_titles[index],
        districts[index],
        longitudes[index],
        latitudes[index],
        image_urls[index]
     ])
  return spot_file

def combine_mrt_file():
  '''combine keywords and save file'''
  mrt_file = {}

  for index in range(len(mrt_names)):
    if mrt_names[index] not in mrt_file:
      mrt_file[mrt_names[index]] = [spot_titles[index]]
    else:
      mrt_file[mrt_names[index]].append(spot_titles[index])

  for mrt, spots in mrt_file.items():
      spots.insert(0, mrt)
  return mrt_file.values()
  
def save_to_json(data, input_name):
   '''Save data in CSV format'''
   with open(f"{input_name}.csv", "w", newline='', encoding="utf-8-sig") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data)
    

# Load data
data_1 = load_json(Taipei_Tourist_Link_1)
data_2 = load_json(Taipei_Tourist_Link_2)
spot_titles, longitudes, latitudes, serial_list_1, file_list = arrange_data_1(data_1)

# Extract image URLs
image_urls = get_image_urls(file_list)

# Resort the data_2
sorted_data_2 = sort_data_2(data_2)
mrt_names, districts = arrange_data_2(sorted_data_2)

# combine file 
spot_file = combine_spot_file()
mrt_file = combine_mrt_file()

# save file
save_to_json(spot_file, 'spot')
save_to_json(mrt_file, 'mrt')
