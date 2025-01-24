import requests, urllib.parse, csv, re
from bs4 import BeautifulSoup

URL = 'https://www.ptt.cc/bbs/Lottery/index.html'
OVER_18_HEADERS = {'cookie': 'over18 = 1;'}
NUM_PAGE = 3

def parse(url):
  '''use beautiful soup to parse html file'''
  response = requests.get(url, headers = OVER_18_HEADERS)
  soup = BeautifulSoup(response.text, "html.parser")
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
      print("There's no item with that attribute")
     
     results.append({'title': title, 'push': push, 'article': 'https://www.ptt.cc/' + article})
  
  return results

def parse_next_link(controls):
    '''fetch the link of next page in PTT lottery'''
    controls = soup.select('.action-bar a.btn.wide')
    next_page = controls[1].get('href') # .get('href') or .attrs['href']
    number = re.findall(r'\d+', next_page)
    number_int = int(number[0])
    for index in range(number_int, number_int - NUM_PAGE, -1):
      page_link = 'https://www.ptt.cc/bbs/Lottery/index' + str(index) + '.html'
      return page_link

def publish_time(soup):
  '''link to specific article and parse its datetime'''
  dates = []
  for result in results:
    content = parse(result['article'])
    meta_value = content.find_all('span', class_='article-meta-value')
    if meta_value:
      dates.append(meta_value[3].text.strip())
    else:
      dates.append(None)
      '''<span class="article-meta-value">Tue Jan 21 17:45:18 2025</span>'''
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

def remove_delete_article(combined_results):
    '''remove the deleted articles'''
    article_counts = {}
    filtered_results = []

    for line in combined_results:
        article_url = line['article']

        if article_url in article_counts:
            article_counts[article_url] += 1
        else:
            article_counts[article_url] = 1
    
    for line in combined_results:
        if article_counts[line['article']] == 1:
            filtered_results.append(line)

    return filtered_results

def combine_article_file():
  '''combine keywords and save file'''
  combined_results = combine_all_file(soup)
  filtered_results = remove_delete_article(combined_results)
  article_file = []

  for index in range(len(filtered_results)):
     article_file.append([
        filtered_results[index]['title'],
        filtered_results[index]['push'],
        filtered_results[index]['date'],
     ])
  return article_file
 
def save_to_json(data, input_name):
   '''Save data in CSV format'''
   with open(f"{input_name}.csv", "a", newline='', encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerows(data)
    file.close()

for page in range(NUM_PAGE):
   '''parse the html content'''
   soup = parse(URL)
   results = fetch_data(soup)
   article_file = combine_article_file()
   combined_results = combine_all_file(soup)
   filtered_results = remove_delete_article(combined_results)
   page_link = parse_next_link(controls = soup.select('.action-bar a.btn.wide'))
   '''<div class="action-bar"><a class="btn wide" href="/bbs/Lottery/index1.html">最舊</a>...</div>'''
   URL = page_link
   save_to_json(article_file, 'article')
   



