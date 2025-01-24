import urllib.request, json, csv, re
from bs4 import BeautifulSoup

URL = 'https://www.ptt.cc/bbs/Lottery/index.html'
NUM_PAGE = 3
  
def parse(url):
  '''use urllib and beautiful soup to parse html file'''
  request = urllib.request.Request(url, headers = {
    'cookie': 'over18 = 1',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
  })
  with urllib.request.urlopen(request) as response:
    data = response.read().decode("utf-8")

  soup = BeautifulSoup(data, 'html.parser')
  return soup

def fetch_data(soup):
  '''extract keywords of "title", 'push", "article" and arrange to be a list.'''
  results = []
  elements = soup.select('.r-ent') 

  for element in elements:
     try:
      title = element.find('a').get_text()
      article = element.find('a').get('href')
      push = element.find('span').get_text()

     except AttributeError:
      print("There's no item with that code")
     
     results.append({'title': title, 'push': push, 'article': 'https://www.ptt.cc/' + article})
  
  return results

def parse_next_link(controls):
    '''fetch the link of next page in PTT lottery'''
    next_page = controls[1].get('href') # .get('href') or .attrs['href']
    number = re.findall('\d+', next_page)
    number_int = int(number[0])
    for index in range(number_int, number_int - NUM_PAGE, -1):
      page_link = 'https://www.ptt.cc/bbs/Lottery/index' + str(index) + '.html'
      return page_link

def publish_time(soup):
  '''link to specific article and parse its datetime'''
  results = fetch_data(soup)
  dates = []
  for result in results:
    content = parse(result['article'])
    meta_value = content.find_all('span', class_='article-meta-value')
    if meta_value:
      dates.append(meta_value[3].text.strip())
    else:
      dates.append(None)

  return dates

def combine_all_file(soup):
  '''combine one file with article, push, title and the other file with datetime'''
  results = fetch_data(soup)
  dates = publish_time(soup)

  # Ensure results and dates have the same length
  if len(results) != len(dates):
    raise ValueError("Results and dates must have the same length.")
  
  combined_results = []
  for result, date in zip(results, dates):
    combined_result = result.copy()
    combined_result['date'] = date
    combined_results.append(combined_result)

  return combined_results

def combine_article_file():
  '''combine keywords and save file'''
  article_file = []

  for index in range(len(combined_results)):
     article_file.append([
        combined_results[index]['title'],
        combined_results[index]['push'],
        combined_results[index]['date']
     ])
  return article_file

def save_to_json(data, input_name):
   '''Save data in CSV format'''
   with open(f"{input_name}.csv", "a", newline='', encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerows(data)
    file.close()

for page in range(NUM_PAGE):
   '''parse the html content with the setup number of pages'''
   soup = parse(URL)
   combined_results = combine_all_file(soup)
   article_file = combine_article_file()
   page_link = parse_next_link(controls = soup.select('.action-bar a.btn.wide'))
   URL = page_link
   save_to_json(article_file, 'article')
   




