import json
import requests
from bs4 import BeautifulSoup
import locale
from datetime import datetime

## HF papers

BASE_URL = "https://huggingface.co/papers"
page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")
h3s = soup.find_all("h3")
papers = []

def extract_abstraction(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    abstract = soup.find("div", {"class": "pb-8 pr-4 md:pr-16"}).text

    time_element = soup.find("time")
    datetime_str = time_element.get("datetime") if time_element else None
    if datetime_str and not datetime_str.endswith("Z"):
        datetime_str = f"{datetime_str}Z"

    if abstract.startswith("Abstract\n"):
        abstract = abstract[len("Abstract\n") :]
    abstract = abstract.replace("\n", " ")
    return abstract, datetime_str

for h3 in h3s:
    a = h3.find("a")
    title = a.text
    link = a["href"]
    url = f"https://huggingface.co{link}"
    try:
        abstract, datetime_str = extract_abstraction(url)
    except Exception as e:
        print(f"Failed to extract abstract for {url}: {e}")
        abstract, datetime_str = "", None

    papers.append({"title": title, "url": url, "abstract": abstract, "date_published": datetime_str})

feed = {
    "version": "https://jsonfeed.org/version/1",
    "title": "Hugging Face Papers",
    "home_page_url": BASE_URL,
    "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/hf_papers.json",
    "items": sorted(
        [
            {
                "id": p["url"],
                "title": p["title"].strip(),
                "content_text": p["abstract"].strip(),
                "url": p["url"],
                **({"date_published": p["date_published"]} if p["date_published"] else {}),
            }
            for p in papers
        ],
        key=lambda x: x.get("date_published", ""),
        reverse=True,
    ),
}

with open("hf_papers.json", "w") as f:
    json.dump(feed, f)

## HF Blog

BASE_URL = "https://huggingface.co/blog"
page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")
h2s = soup.find_all("h2")
papers = []

def extract_abstraction(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    date = soup.find("div", "mb-6 flex items-center gap-x-4 text-base")
    if date:
        span = date.find('span')
        if span:
            date = span.text.replace("Published\n","").lstrip()
    return date

for h2 in h2s:
    a = h2.find_parents("a",limit=1)[0]
    title = h2.text
    link = a["href"]
    url = f"https://huggingface.co{link}"
    date = extract_abstraction(url)  
    papers.append({"title": title, "url": url, "abstract": abstract, "date_published": date})

feed = {
    "version": "https://jsonfeed.org/version/1",
    "title": "Hugging Face Blog",
    "home_page_url": BASE_URL,
    "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/hf_blog.json",
    "items": 
        [
            {
                "id": p["url"],
                "title": p["title"].strip(),
                "content_text": p["abstract"].strip(),
                "url": p["url"],
                "date_published": p["date_published"],
            }
            for p in papers
        ],
}

with open("hf_blog.json", "w") as f:
    json.dump(feed, f)

## Museumsbund Stellenportal

locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

BASE_URL = "https://www.museumsbund.de/stellenangebote/"
page = requests.get(BASE_URL)
soup = BeautifulSoup(page.content, "html.parser")

h3s = soup.find_all("h3", "teaser__headline--job")
papers = []

def extract_abstraction(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    date = soup.find("h4", "content__sidebar-title").text
    date = date.replace("Veröffentlicht am ","").lstrip()
    dt = datetime.strptime(date, '%d. %B %Y')
    date_published = dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    site_text = soup.find("div","content__main entry-content")
    site_text = site_text.get_text("\n",strip=True)
    return site_text, date_published


for h3 in h3s:
    title = h3.text
    a = h3.find("a")
    link = a["href"]
    url = link
    whodate = h3.find_next("div", "teaser__excerpt teaser__text p-summary e-content").text.replace("\n","")
    whodate = ' '.join(whodate.split())
    print(whodate)
    site_text, date_published = extract_abstraction(url)  
    papers.append({"title": title, "url": url, "abstract": whodate + " | " + site_text, "date_published": date_published})

feed = {
    "version": "https://jsonfeed.org/version/1",
    "title": "Museumsbund Stellenportal",
    "home_page_url": BASE_URL,
    "feed_url": "https://example.org/feed.json",
    "items": 
        [
            {
                "id": p["url"],
                "title": p["title"].strip(),
                "content_text": p["abstract"].strip(),
                "url": p["url"],
                "date_published": p["date_published"],
            }
            for p in papers
        ],
}

with open("mb_jobs.json", "w") as f:
    json.dump(feed, f)
