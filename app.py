import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

## HF papers

BASE_URL = "https://huggingface.co/papers"
page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")
h3s = soup.find_all("h3")
entries = []

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

    entries.append({"title": title, "url": url, "abstract": abstract, "date_published": datetime_str})

papers_feed = {
    "version": "https://jsonfeed.org/version/1",
    "title": "Hugging Face Papers",
    "home_page_url": "https://huggingface.co/",
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
            for p in entries
        ],
        key=lambda x: x.get("date_published", ""),
        reverse=True,
    ),
}

## HF Blog

BASE_URL = "https://huggingface.co/blog"
page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")
h2s = soup.find_all("h2")
entries = []

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
    i_url = a.find("img", "object-cover")["src"]
    i_url = f"https://huggingface.co{i_url}"
    title = h2.text
    link = a["href"]
    url = f"https://huggingface.co{link}"
    date = extract_abstraction(url)  
    entries.append({"title": title, "i_url": i_url, "url": url, "abstract": abstract, "date_published": date})

blog_feed = {
    "version": "https://jsonfeed.org/version/1",
    "title": "Hugging Face Blog",
    "home_page_url": "https://huggingface.co/",
    "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/hf_blog.json",
    "items": 
        [
            {
                "id": p["url"],
                "image": p["i_url"],
                "title": p["title"].strip(),
                "content_text": p["abstract"].strip(),
                "url": p["url"],
                "date_published": p["date_published"],
            }
            for p in entries
        ],
}

## HF Posts

BASE_URL = "https://huggingface.co/posts?sort=trending"
page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")
articles = soup.find_all("article")
entries = []

for article in articles:
    a = article.find("a")
    title = article.find("span").text
    link = a["href"]
    url = f"https://huggingface.co{link}"
    abstract = article.select_one("div.relative > div.relative.overflow-hidden").get_text("\n", strip=True)
    entries.append({"title": title, "url": url, "abstract": abstract})

posts_feed = {
    "version": "https://jsonfeed.org/version/1",
    "title": "Hugging Face Posts",
    "home_page_url": "https://huggingface.co/",
    "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/hf_posts.json",
    "items": 
        [
            {
                "id": p["url"],
                "title": p["title"].strip(),
                "content_text": p["abstract"].strip(),
                "url": p["url"],
                "date_published": datetime.now().isoformat(),
            }
            for p in entries
        ],
}

## Museumsbund Stellenportal

BASE_URL = "https://www.museumsbund.de/stellenangebote/"
page = requests.get(BASE_URL)
soup = BeautifulSoup(page.content, "html.parser")

h3s = soup.find_all("h3", "teaser__headline--job")
entries = []

def extract_abstraction(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    date = soup.find("h4", "content__sidebar-title").text
    date_published = date.replace("Veröffentlicht am ","").replace("VerĂ¶ffentlicht am ","").lstrip()
    site_text = soup.find("div","content__main entry-content")
    site_text = site_text.get_text("\n",strip=True)
    return site_text, date_published

def strdate2datetime(date_str):
    german_months = {
        'Januar': 1, 'Februar': 2, 'März': 3, 'April': 4, 'Mai': 5, 'Juni': 6,
        'Juli': 7, 'August': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Dezember': 12
    }
    try:
        day, month, year = date_str.split()
        day = day.replace('.', '')
        month_num = german_months[month]
        dt = datetime(int(year), month_num, int(day))
        return dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    except (ValueError, KeyError) as e:
        print(f"Error parsing date '{date_str}': {e}")
        return None

for h3 in h3s:
    title = h3.text
    a = h3.find("a")
    link = a["href"]
    url = link
    whodate = h3.find_next("div", "teaser__excerpt teaser__text p-summary e-content").text.replace("\n","")
    whodate = ' '.join(whodate.split())
    site_text, date_published = extract_abstraction(url)  
    entries.append({"title": title, "url": url, "abstract": whodate + " | " + site_text, "date_published": date_published})

mb_jobs_feed = {
    "version": "https://jsonfeed.org/version/1",
    "title": "Museumsbund Stellenportal",
    "home_page_url": "https://www.museumsbund.de/",
    "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/mb_jobs.json",
    "items": 
        [
            {
                "id": p["url"],
                "title": p["title"].strip(),
                "content_text": p["abstract"].strip(),
                "url": p["url"],
                "date_published": strdate2datetime(p["date_published"]).strip(),
            }
            for p in entries
        ],
}


with open("hf_papers.json", "w") as f:
    json.dump(papers_feed, f)
with open("hf_blog.json", "w") as f:
    json.dump(blog_feed, f)
with open("hf_posts.json", "w") as f:
    json.dump(posts_feed, f)
with open("mb_jobs.json", "w") as f:
   json.dump(mb_jobs_feed, f)
