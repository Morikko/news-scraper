# news-scraper-ranking
An example API that provides scraps, save and clean news.

Developed in Python 3 only.

# Scraper

## Description
The scraper is designed to work with "Le Monde" website. It seeks all the article links (around 150) from the home page that are not part of the subscribed edition.

## Features
For each article, the scraper extracts:
 - Title
 - URL
 - Article category
 - Writer
 - Article description
 - Publish Time
 - Update Time
 - Article content
 - Related article titles

## Store
The fetched articles can be stored in 2 formats:
 - Complete HTML code in data/html/<article_name>.html
 - Extracted elements in data/ext/<article_name>.json

## Useful API
```python
import newstool
links, htmls, feats = newstool.scraper.lemonde_scraper.scrapLeMonde( links_limit=-1, save_html=True, save_features_json=True)

htmls = newstool.scraper.lemonde_scraper.loadArticlesAsHtml("data/html")

feats = newstool.scraper.lemonde_scraper.loadFeaturesArticlesAsJson( "data/features" )
```

## Results
I did a successfully scraping on November the 4th: 116 articles extracted.

## Dependencies
 - beautifulsoup4>=4.6.0

# Ranker

## Description
Take the previously extracted features and search keywords in them.
Return the articles that match the most the keywords.

## Search Engine
The features kept are:
 - Title
 - Article description
 - Article content

All the features and queries are put in lowercase and without accents.

The search ranking system is based on a TfIdf model with sklearn. This basic model is a good starting point for a fast and efficient search engine. 

However, the model is not perfect, it only counts on words occurrences. 
Future improvements could be:
 - Give a note to the articles based on how readable the articles are
 - Add social metrics: comments, social shares to give hot articles first
 - Correct misspelling keywords
 - Learn from users behaviors to improve the search engine 
    (need to access user behavior metrics, not possible in this scraping case) 

## Useful API
```python
import newstool

# Features need to be extracted and saved before in data/features 
kr = newstool.ranking.keywords_ranking.KeywordsRanker()

# Features are in memory
kr = newstool.ranking.keywords_ranking.KeywordsRanker(feats)

kr.search("avion")
kr.search("europe interdit", results_limit=3, all_keywords=True)
```

## Results
Check `notebooks/search_examples.ipynb`

## Dependencies
 - scikit-learn>=0.18.1
 - scipy>=0.19.0
 - numpy>=1.12.0
Might work with smaller versions, but I didn't try.
