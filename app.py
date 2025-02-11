import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from rfeed import *
from xml.etree import ElementTree as ET
import textwrap

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
        date = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")

        if abstract.startswith("Abstract\n"):
            abstract = abstract[len("Abstract\n") :]
        abstract = abstract.replace("\n", " ")
        return abstract, date

    for h3 in h3s:
        a = h3.find("a")
        title = a.text
        link = a["href"]
        url = f"https://huggingface.co{link}"
        try:
            abstract, date = extract_abstraction(url)
        except Exception as e:
            print(f"Failed to extract abstract for {url}: {e}")
            abstract, date = "", datetime.now()

        entries.append({"title": title, "image_url": "", "url": url, "abstract": abstract, "date_published": date})

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
                    "date_published": p["date_published"].isoformat(),
                }
                for p in entries
            ],
    }
    if not papers_feed['items']:
        papers_feed['items'] = [{"id": "1","title": "Something is wrong - no hf papers feed generated","date_published": datetime.now().isoformat(),}] 
    
    rss_papers_feed = Feed(
        title = "Hugging Face Papers",
        link = "https://huggingface.co/",
        description = "This is a website scraping RSS feed for the HuggingFace Papers.",
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
    rss_papers_feed = rss_papers_feed.rss()
    
    return papers_feed, rss_papers_feed

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

        abstract = article.select_one("div.blog-content").get_text("\n", strip=True)
        abstract = textwrap.shorten(abstract, width=1000, placeholder="...")

        date = article.find("div", "mb-6 flex items-center gap-x-4 text-base")
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
            abstract, date = "", datetime.now()
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
                    "date_published": p["date_published"].isoformat(),
                }
                for p in entries
            ],
    }
    if not blog_feed['items']:
        blog_feed['items'] = [{"id": "1","title": "Something is wrong - no hf blog feed generated","date_published": datetime.now().isoformat(),}] 

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
        abstract = article.select_one("div.relative > div.relative.overflow-hidden").get_text("\n", strip=True)
        abstract = textwrap.shorten(abstract, width=1000, placeholder="...")
        entries.append({"title": title, "image_url": "", "url": url, "abstract": abstract, "date_published": datetime.now()})

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
                    "date_published": p["date_published"].isoformat(),
                }
                for p in entries
            ],
    }
    if not posts_feed['items']:
        posts_feed['items'] = [{"id": "1","title": "Something is wrong - no hf papers feed generated","date_published": datetime.now().isoformat(),}]
    
    rss_posts_feed = Feed(
        title = "Hugging Face Posts",
        link = "https://huggingface.co/",
        description = "This is a website scraping RSS feed for the Hugginface trending posts.",
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
    rss_posts_feed = rss_posts_feed.rss()
    
    return posts_feed, rss_posts_feed

# Museumsbund Stellenportal
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
        date = datetime(int(year), month_num, int(day))
        return date

    for h3 in h3s:
        title = h3.text
        a = h3.find("a")
        link = a["href"]
        url = link
        whodate = h3.find_next("div", "teaser__excerpt teaser__text p-summary e-content").text.replace("\n","")
        whodate = ' '.join(whodate.split())
        site_text, date_published = extract_abstraction(url)  
        try:
            date_published = strdate2datetime(date_published)
        except:
            date_published = datetime.now()
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
                    "date_published": p["date_published"].isoformat(),
                }
                for p in entries
            ],
    }
    if not mb_jobs_feed['items']:
        mb_jobs_feed['items'] = [{"id": "1","title": "Something is wrong - no Museumsbund jobs feed generated","date_published": datetime.now().isoformat(),}]

    rss_mb_jobs_feed = Feed(
        title = "Museumsbund Stellenportal",
        link = "https://www.museumsbund.de/",
        description = "This is a website scraping RSS feed for the Museumsbund Stellenportal.",
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
    rss_mb_jobs_feed = rss_mb_jobs_feed.rss()

    return mb_jobs_feed, rss_mb_jobs_feed

# Wikidate Death List
def generate_wd_death_list():
    url = "https://qlever.cs.uni-freiburg.de/api/wikidata?query=PREFIX+wd%3A+%3Chttp%3A%2F%2Fwww.wikidata.org%2Fentity%2F%3E%0APREFIX+wdt%3A+%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fdirect%2F%3E%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0ASELECT+%3Fperson_id+%3Fperson+%3Fdate+%28GROUP_CONCAT%28%3Fprofession%3B+separator%3D%22%2C+%22%29+AS+%3Fprofessions%29+WHERE+%7B%0A++%3Fperson_id+wdt%3AP31+wd%3AQ5+.%0A++%3Fperson_id+rdfs%3Alabel+%3Fperson+.%0A++%3Fperson_id+wdt%3AP570+%3Fdate.%0A++%0A++OPTIONAL+%7B+%3Fperson_id+wdt%3AP106+%3Fprofession_id+.%0A++++%3Fprofession_id+rdfs%3Alabel+%3Fprofession+.%0A++++FILTER%28LANG%28%3Fprofession%29+%3D+%22en%22%29%0A+%7D%0A++%0A++BIND%28YEAR%28NOW%28%29%29+-+70+as+%3FyearToCheck%29%0A++FILTER%28YEAR%28%3Fdate%29+%3D+%3FyearToCheck+%26%26+%0A+++++++++MONTH%28%3Fdate%29+%3D+MONTH%28NOW%28%29%29+%26%26+%0A+++++++++DAY%28%3Fdate%29+%3D+DAY%28NOW%28%29%29%29%0A++FILTER+%28LANG%28%3Fperson%29+%3D+%22en%22%29+.%0A%0A++%0A%7D%0AGROUP+BY+%3Fperson_id+%3Fperson+%3Fdate+%3Fprofessions+%0AOrder+BY+%3Fperson"
    response = requests.get(url)
    data = response.json()
    now = datetime.now()
    
    entries = []

    for result in data['results']['bindings']:
        entries.append({"title": result['person']['value'], "image_url": "", "url": result['person_id']['value'], "abstract": result['professions']['value'] + " | " + result['date']['value'].split("T")[0], "date_published": now})
    
    wd_death_feed = {
        "version": "https://jsonfeed.org/version/1",
        "title": "Wikidata 70yrs expired list",
        "home_page_url": "https://wikidata.org",
        "feed_url": "https://raw.githubusercontent.com/MichaelMarkert/rss/refs/heads/main/mb_jobs.json",
        "items": 
            [
                {
                    "id": p["url"],
                    "image": p["image_url"],
                    "title": p["title"].strip(),
                    "content_text": p["abstract"],
                    "url": p["url"],
                    "date_published": p["date_published"].isoformat(),
                }
                for p in entries
            ],
    }
    if not wd_death_feed['items']:
        wd_death_feed['items'] = [{"id": "1","title": "Something is wrong - no Wikidata feed generated","date_published": datetime.now().isoformat(),}]

    rss_wd_death_feed = Feed(
        title = "Wikidata 70yrs expired list",
        link = "https://wikidata.org",
        description = "This is a website scraping RSS feed for wikidata entries of people that died 70 years ago.",
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
    rss_wd_death_feed = rss_wd_death_feed.rss()

    return wd_death_feed, rss_wd_death_feed   

try:
    papers_feed, rss_papers_feed = generate_hf_papers()
    with open("hf_papers.json", "w") as f:
        json.dump(papers_feed, f)
    with open("hf_papers.xml", "w") as f:
        f.write(rss_papers_feed)
except:
    print("hf_papers_feed not generated")

try:
    blog_feed, rss_blog_feed = generate_hf_blog()
    with open("hf_blog.json", "w") as f:
        json.dump(blog_feed, f)
    with open("hf_blog.xml", "w") as f:
        f.write(rss_blog_feed)
except:
    print("hf_blog_feed not generated")

try:
    posts_feed, rss_posts_feed = generate_hf_posts()
    with open("hf_posts.json", "w") as f:
        json.dump(posts_feed, f)
    with open("hf_posts.xml", "w") as f:
        f.write(rss_posts_feed)
except:
    print("hf_posts_feed not generated")

try:
    mb_jobs_feed, rss_mb_jobs_feed = generate_mb_jobs()
    with open("mb_jobs.json", "w") as f:
        json.dump(mb_jobs_feed, f)
    with open("mb_jobs.xml", "w") as f:
        f.write(rss_mb_jobs_feed)
except:
    print("mb_jobs_feed not generated")

try:
    wd_death_feed, rss_wd_death_feed = generate_wd_death_list()
    with open("wd_70yrsexp.json", "w") as f:
        json.dump(wd_death_feed, f)
    with open("wd_70yrsexp.xml", "w") as f:
        f.write(rss_wd_death_feed)
except:
    print("wd_70yrsexp_feed not generated")
