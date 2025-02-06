import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from rfeed import *
from xml.etree import ElementTree as ET

## HF papers
def generate_hf_papers():
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

        entries.append({"title": title, "image_url": "", "url": url, "abstract": abstract, "date_published": datetime_str})

    papers_feed = {
        "version": "https://jsonfeed.org/version/1",
        "title": "Hugging Face Papers",
        "home_page_url": "https://huggingface.co/",
        "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/hf_papers.json",
        "items": 
            [
                {
                    "id": p["url"],
                    "image": p["image_url"],
                    "title": p["title"].strip(),
                    "content_text": p["abstract"].strip(),
                    "url": p["url"],
                    "date_published": p["date_published"],
                }
                for p in entries
            ],
    }
    if not papers_feed['items']:
        papers_feed['items'] = [{"id": "1","title": "Something is wrong - no hf papers feed generated","date_published": datetime.now().isoformat(),}] 
    return papers_feed

## HF Blog
def generate_hf_blog():
    BASE_URL = "https://huggingface.co/blog"
    page = requests.get(BASE_URL)

    soup = BeautifulSoup(page.content, "html.parser")
    h2s = soup.find_all("h2")
    entries = []

    def extract_abstract_date(url):
        page = requests.get(url)
        article = BeautifulSoup(page.content, "html.parser")

        abstract = article.select_one("div.blog-content").get_text("\n", strip=True)[:1000]

        date = soup.find("div", "mb-6 flex items-center gap-x-4 text-base")
        if date:
            span = date.find('span')
            if span:
                date = span.text.replace("Published\n","").lstrip()
                month, day, year = date.replace(",", "").split()
                months = {
                    'January': 1, 'February': 2, 'March': 3, 'April': 4,
                    'May': 5, 'June': 6, 'July': 7, 'August': 8,
                    'September': 9, 'October': 10, 'November': 11, 'December': 12
                }
                date = datetime(int(year), months[month], int(day))
        return abstract, date

    for h2 in h2s:
        a = h2.find_parents("a",limit=1)[0]
        i_url = a.find("img", "object-cover")["src"]
        i_url = f"https://huggingface.co{i_url}"
        title = h2.text
        link = a["href"]
        url = f"https://huggingface.co{link}"
        try:
            abstract, date = extract_abstract_date(url)  
        except:
            abstract, date = "", ""
        entries.append({"title": title, "image_url": i_url, "url": url, "abstract": abstract, "date_published": date})

    blog_feed = {
        "version": "https://jsonfeed.org/version/1",
        "title": "Hugging Face Blog",
        "home_page_url": "https://huggingface.co/",
        "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/hf_blog.json",
        "items": 
            [
                {
                    "id": p["url"],
                    "image": p["image_url"],
                    "title": p["title"].strip(),
                    "content_text": p["abstract"].strip(),
                    "url": p["url"],
                    "date_published": p["date_published"],
                }
                for p in entries
            ],
    }
    if not blog_feed['items']:
        blog_feed['items'] = [{"id": "1","title": "Something is wrong - no hf papers feed generated","date_published": datetime.now().isoformat(),}] 

    rss_blog_feed = Feed(
        title = "Hugging Face Blog",
        link = "https://huggingface.co/",
        description = "This is a website scraping RSS feed for the HuggingFace Blog.",
        items = [
            Item(
                title = p["title"].strip(),
                description = p["abstract"].strip(),
                pubDate = p["date_published"],
                link = p["url"],
                guid = Guid(p["url"]),
            )
            for p in entries
        ]
    )
    rss_blog_feed = rss_blog_feed.rss()

    return blog_feed, rss_blog_feed

## HF Posts
def generate_hf_posts():
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
        abstract = article.select_one("div.relative > div.relative.overflow-hidden").get_text("\n", strip=True)[:500]
        entries.append({"title": title, "image_url": "", "url": url, "abstract": abstract, "date_published": datetime.now().isoformat()})

    posts_feed = {
        "version": "https://jsonfeed.org/version/1",
        "title": "Hugging Face Posts",
        "home_page_url": "https://huggingface.co/",
        "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/hf_posts.json",
        "items": 
            [
                {
                    "id": p["url"],
                    "image": p["image_url"],
                    "title": p["title"].strip(),
                    "content_text": p["abstract"].strip(),
                    "url": p["url"],
                    "date_published": p["date_published"],
                }
                for p in entries
            ],
    }
    if not posts_feed['items']:
        posts_feed['items'] = [{"id": "1","title": "Something is wrong - no hf papers feed generated","date_published": datetime.now().isoformat(),}]
    return posts_feed

## Museumsbund Stellenportal
def generate_mb_jobs():
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
        site_text = soup.find("div","content__main entry-content").get_text("\n",strip=True)
        return site_text, date_published

    def strdate2datetime(date_str):
        german_months = {
            'Januar': 1, 'Februar': 2, 'März': 3, 'April': 4, 'Mai': 5, 'Juni': 6,
            'Juli': 7, 'August': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Dezember': 12
        }
        day, month, year = date_str.split()
        day = day.replace('.', '')
        month_num = german_months[month]
        dt = datetime(int(year), month_num, int(day))
        return dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')

    for h3 in h3s:
        title = h3.text
        a = h3.find("a")
        link = a["href"]
        url = link
        whodate = h3.find_next("div", "teaser__excerpt teaser__text p-summary e-content").text.replace("\n","")
        whodate = ' '.join(whodate.split())
        site_text, date_published = extract_abstraction(url)  
        try:
            date_published = strdate2datetime(date_published).strip()
        except:
            date_published = ""
        entries.append({"title": title, "image_url": "", "url": url, "abstract": whodate + " | " + site_text, "date_published": date_published})

    mb_jobs_feed = {
        "version": "https://jsonfeed.org/version/1",
        "title": "Museumsbund Stellenportal",
        "home_page_url": "https://www.museumsbund.de/",
        "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/mb_jobs.json",
        "items": 
            [
                {
                    "id": p["url"],
                    "image": p["image_url"],
                    "title": p["title"].strip(),
                    "content_text": p["abstract"].strip(),
                    "url": p["url"],
                    "date_published": p["date_published"],
                }
                for p in entries
            ],
    }
    if not mb_jobs_feed['items']:
        mb_jobs_feed['items'] = [{"id": "1","title": "Something is wrong - no hf papers feed generated","date_published": datetime.now().isoformat(),}]
    return mb_jobs_feed

papers_feed = generate_hf_papers()
blog_feed, rss_blog_feed = generate_hf_blog()
posts_feed = generate_hf_posts()
mb_jobs_feed = generate_mb_jobs()

with open("hf_papers.json", "w") as f:
    json.dump(papers_feed, f)
with open("hf_blog.json", "w") as f:
    json.dump(blog_feed, f)
with open("hf_blog.xml", "w") as f:
    f.write(rss_blog_feed)
with open("hf_posts.json", "w") as f:
    json.dump(posts_feed, f)
with open("mb_jobs.json", "w") as f:
   json.dump(mb_jobs_feed, f)
