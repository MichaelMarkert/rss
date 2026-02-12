<link rel="alternate" type="application/rss+xml" title="Hugginface Blog" href="https://michaelmarkert.github.io/rss/hf_blog.xml" />
<link rel="alternate" type="application/rss+xml" title="Hugginface Papers" href="https://michaelmarkert.github.io/rss/hf_papers.xml" />
<link rel="alternate" type="application/rss+xml" title="Hugginface Trending Posts" href="https://michaelmarkert.github.io/rss/hf_posts.xml" />
<link rel="alternate" type="application/rss+xml" title="Museumsbund Stellenportal" href="https://michaelmarkert.github.io/rss/mb_jobs.xml" />
<link rel="alternate" type="application/rss+xml" title="Wikidata 70yrs expired list" href="https://michaelmarkert.github.io/rss/wd_70yrsexp.xml" />
<link rel="alternate" type="application/rss+xml" title="GND 70yrs expired list" href="https://michaelmarkert.github.io/rss/gnd_70yrsexp.xml" />
<link rel="alternate" type="application/json" title="Hugginface Blog" href="https://michaelmarkert.github.io/rss/hf_blog.json" />
<link rel="alternate" type="application/json" title="Hugginface Papers" href="https://michaelmarkert.github.io/rss/hf_papers.json" />
<link rel="alternate" type="application/json" title="Hugginface Trending Posts" href="https://michaelmarkert.github.io/rss/hf_posts.json" />
<link rel="alternate" type="application/JSON" title="Museumsbund Stellenportal" href="https://michaelmarkert.github.io/rss/mb_jobs.json" />
<link rel="alternate" type="application/JSON" title="Wikidata 70yrs expired list" href="https://michaelmarkert.github.io/rss/wd_70yrsexp.json" />
<link rel="alternate" type="application/JSON" title="GND 70yrs expired list" href="https://michaelmarkert.github.io/rss/gnd_70yrsexp.json" />

# RSS feeds from website generator

Different RSS feeds generated from websites parsed with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) or from data sources like Wikidata in Python. The [JSON Feed](https://www.jsonfeed.org/) and [RSS XML](https://www.rssboard.org/rss-specification) files are generated several times a day using Github Actions.

## Available feeds

- **Huggingface Blog**: [JSON Feed](https://michaelmarkert.github.io/rss/hf_blog.json), [RSS XML](https://michaelmarkert.github.io/rss/hf_blog.xml)
- **Huggingface Papers**: [JSON Feed](https://michaelmarkert.github.io/rss/hf_papers.json), [RSS XML](https://michaelmarkert.github.io/rss/hf_papers.xml)
- **Huggingface Trending Posts**: [JSON Feed](https://michaelmarkert.github.io/rss/hf_posts.json), [RSS XML](https://michaelmarkert.github.io/rss/hf_posts.xml)
- **Museumsbund Stellenmarkt**: [JSON Feed](https://michaelmarkert.github.io/rss/mb_jobs.json), [RSS XML](https://michaelmarkert.github.io/rss/mb_jobs.xml)
- **Wikidata SPARQL query for all people that died exactly 70 years ago, with their professions** ([example query for 1955-02-10](https://w.wiki/D2tg)): [JSON Feed](https://michaelmarkert.github.io/rss/wd_70yrsexp.json), [RSS XML](https://michaelmarkert.github.io/rss/wd_70yrsexp.xml)
- **Lobid-GND query for all people that dies exactly 70 years ago, with their professions**:
[JSON Feed](https://michaelmarkert.github.io/rss/gnd_70yrsexp.json), [RSS XML](https://michaelmarkert.github.io/rss/gnd_70yrsexp.xml)

## Status of feeds

Failed to extract abstract for https://huggingface.co/papers/2602.10177: strptime() argument 1 must be str, not None, Failed to extract abstract for https://huggingface.co/papers/2602.10999: strptime() argument 1 must be str, not None, hf_blog_feed not generated, 2026-02-12T14:12:52.

## License

This project is licensed under an [MIT license](LICENSE).
