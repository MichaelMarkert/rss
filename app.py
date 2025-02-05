import json
import requests
from bs4 import BeautifulSoup

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
