import requests, urllib.parse, csv, re
from bs4 import BeautifulSoup

URL = 'https://www.ptt.cc/bbs/Lottery/index.html'
OVER_18_HEADERS = {'cookie': 'over18 = 1;'}
NUM_PAGE = 3

# parse article title, like/dislike count, and publish time for every article in PTT lottery board
# EEE MMM DD HH:MM:SS YYYY (Fri Jul 14 23:14:36 2023)
# ArticleTitle,Like/DislikeCount,PublishTime
def parse(url):
  response = requests.get(url, headers = OVER_18_HEADERS)
  soup = BeautifulSoup(response.text, "html.parser")
  return soup

def fetch_data(soup):
  results = []
  elements = soup.select('.r-ent') 

  for element in elements:
     try:
      title = element.find('a').get_text()
      article = element.find('a').get('href')
      push = element.find('span').get_text()

     except AttributeError:
       pass
     
     results.append({'title': title, 'push': push, 'article': 'https://www.ptt.cc/' + article})
  
  return results

def parse_next_link(controls):
    next_page = controls[1].get('href') # .get('href') or .attrs['href']
    number = re.findall('\d+', next_page)
    number_int = int(number[0])
    for index in range(number_int, number_int - NUM_PAGE, -1):
      page_link = 'https://www.ptt.cc/bbs/Lottery/index' + str(index) + '.html'
      return page_link

# soup = parse(URL)
# print(parse_next_link(controls = soup.select('.action-bar a.btn.wide')))

def publish_time(soup):
  
  results = fetch_data(soup)
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

    # content = parse('https://www.ptt.cc/bbs/Lottery/M.1737452720.A.A9D.html')
    # meta_value = content.find_all('span', class_='article-meta-value')[3].text
    # '''<span class="article-meta-value">Tue Jan 21 17:45:18 2025</span>'''

def combine_all_file(soup):
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
   with open(f"{input_name}.csv", "a", newline='', encoding="utf-8-sig") as file: # "a" 不會覆寫檔案
    writer = csv.writer(file)
    writer.writerows(data)
    file.close()

for page in range(NUM_PAGE):
   # parse the html content
   soup = parse(URL)
   combined_results = combine_all_file(soup)
   article_file = combine_article_file()
   page_link = parse_next_link(controls = soup.select('.action-bar a.btn.wide'))
   '''<div class="action-bar"><a class="btn wide" href="/bbs/Lottery/index1.html">最舊</a>...</div>'''
   URL = page_link
   save_to_json(article_file, 'article')
   




