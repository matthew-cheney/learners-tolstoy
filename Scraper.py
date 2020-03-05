import requests as r
import time
from tqdm import tqdm
import re

BASE_URL = 'http://tolstoy.ru'

def scrapeData(target_url, filename):

    final_url = BASE_URL + target_url

    h = {'user-agent': 'Matthew Cheney (m.cheney95@outlook.com)'}

    response = r.get(final_url, headers=h)

    new_url = re.findall(r'href="(.*epub)"', response.content.decode('utf-8'))[0]
    # print(BASE_URL + new_url)

    new_final_url = BASE_URL + new_url

    response = r.get(new_final_url, headers=h)

    with open(filename, mode='wb') as f:
        f.write(response.content)

file_path = "raw_htmls"

with open('links.txt', 'r') as f:
    links = f.read()

links = links.split('\n')

a_links = links[:67]
links = links[67:]
print(len(links))
i = 68
try:
    for link in tqdm(links):
        # print(link)
        scrapeData(link, f'tolstoy_ru/epubs/tom-{i:02d}.epub')
        i += 1
        time.sleep(3)
except IndexError:
    print(link)
# for i in tqdm(range(1, 91)):
#     scrapeData(f"{i:02d}", file_path + f"/tolstoy_complete_works_tom_{i:02d}.html")
#     time.sleep(3)

print("Done")