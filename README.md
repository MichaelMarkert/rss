<link rel="alternate" type="application/rss+xml" title="Hugginface Blog" href="https://michaelmarkert.github.io/rss/hf_blog.xml" />
<link rel="alternate" type="application/rss+xml" title="Hugginface Papers" href="https://michaelmarkert.github.io/rss/hf_papers.xml" />
<link rel="alternate" type="application/rss+xml" title="Hugginface Trending Posts" href="https://michaelmarkert.github.io/rss/hf_posts.xml" />
<link rel="alternate" type="application/rss+xml" title="Museumsbund Stellenportal" href="https://michaelmarkert.github.io/rss/mb_jobs.xml" />
<link rel="alternate" type="application/rss+xml" title="Wikidata 70yrs expired list" href="https://michaelmarkert.github.io/rss/wd_70yrsexp.xml" />
<link rel="alternate" type="application/json" title="Hugginface Blog" href="https://michaelmarkert.github.io/rss/hf_blog.json" />
<link rel="alternate" type="application/json" title="Hugginface Papers" href="https://michaelmarkert.github.io/rss/hf_papers.json" />
<link rel="alternate" type="application/json" title="Hugginface Trending Posts" href="https://michaelmarkert.github.io/rss/hf_posts.json" />
<link rel="alternate" type="application/JSON" title="Museumsbund Stellenportal" href="https://michaelmarkert.github.io/rss/mb_jobs.json" />
<link rel="alternate" type="application/JSON" title="Wikidata 70yrs expired list" href="https://michaelmarkert.github.io/rss/wd_70yrsexp.json" />

# RSS feeds from website generator

Different RSS feeds generated from websites parsed with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) in Python. The JSON Feed and RSS XML files are generated two times a day using Github Actions.

## Available feeds

- **Huggingface Blog**: [JSON Feed](https://michaelmarkert.github.io/rss/hf_blog.json), [RSS XML](https://michaelmarkert.github.io/rss/hf_blog.xml)
- **Huggingface Papers**: [JSON Feed](https://michaelmarkert.github.io/rss/hf_papers.json), [RSS XML](https://michaelmarkert.github.io/rss/hf_papers.xml)
- **Huggingface Trending Posts**: [JSON Feed](https://michaelmarkert.github.io/rss/hf_posts.json), [RSS XML](https://michaelmarkert.github.io/rss/hf_posts.xml)
- **Museumsbund Stellenmarkt**: [JSON Feed](https://michaelmarkert.github.io/rss/mb_jobs.json), [RSS XML](https://michaelmarkert.github.io/rss/mb_jobs.xml)
- **Wikidata [QLever query for all people that died exactly 70 years ago, with their professions](https://qlever.cs.uni-freiburg.de/wikidata/?query=PREFIX+wd%3A+%3Chttp%3A%2F%2Fwww.wikidata.org%2Fentity%2F%3E%0APREFIX+wdt%3A+%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fdirect%2F%3E%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0ASELECT+%3Fperson_id+%3Fperson+%3Fdate+%28GROUP_CONCAT%28%3Fprofession%3B+separator%3D%22%2C+%22%29+AS+%3Fprofessions%29+WHERE+%7B%0A++%3Fperson_id+wdt%3AP31+wd%3AQ5+.%0A++%3Fperson_id+wdt%3AP106+%3Fprofession_id+.%0A++%3Fprofession_id+rdfs%3Alabel+%3Fprofession+.%0A++%3Fperson_id+rdfs%3Alabel+%3Fperson+.%0A++%3Fperson_id+wdt%3AP570+%3Fdate.%0A++%0A++BIND%28YEAR%28NOW%28%29%29+-+70+as+%3FyearToCheck%29%0A++FILTER%28YEAR%28%3Fdate%29+%3D+%3FyearToCheck+%26%26+%0A+++++++++MONTH%28%3Fdate%29+%3D+MONTH%28NOW%28%29%29+%26%26+%0A+++++++++DAY%28%3Fdate%29+%3D+DAY%28NOW%28%29%29%29%0A++FILTER+%28LANG%28%3Fperson%29+%3D+%22en%22%29+.%0A++FILTER+%28LANG%28%3Fprofession%29+%3D+%22en%22%29%0A++%0A%7D%0AGROUP+BY+%3Fperson_id+%3Fperson+%3Fdate)**: [JSON Feed](https://michaelmarkert.github.io/rss/wd_70yrsexp.json), [RSS XML](https://michaelmarkert.github.io/rss/wd_70yrsexp.xml)

## License

This project is licensed under an [MIT license](LICENSE).
