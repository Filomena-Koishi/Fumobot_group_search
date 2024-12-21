import mwparserfromhell
import json

import requests

url = "https://thwiki.cc/api.php?action=parse&page=%E4%B8%9C%E6%96%B9%E7%9B%B8%E5%85%B3QQ%E7%BE%A4%E7%BB%84%E5%88%97%E8%A1%A8&prop=wikitext&format=json"
response = requests.get(url)
data = response.json()
wikitext = data["parse"]['wikitext']['*']

parsed = mwparserfromhell.parse(wikitext)

data = {
    "title": [str(heading) for heading in parsed.filter_headings()],
    "lists": [str(item) for item in parsed.filter_tags() if item.tag == 'ul'],
    "templates": [str(t) for t in parsed.filter_templates()]
}

# 转换为 JSON 格式
json_data = json.dumps(data, indent=4, ensure_ascii=False)

with open(r'C:\Users\Administrator\bot1\group_list.json', 'w', encoding='utf-8') as file:
    file.write(json_data)
