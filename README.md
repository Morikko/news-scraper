# news-scraper-ranking
An example API that provides scraps, save and clean news.

Developed over Python 3 only.

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
```javascript
links, htmls, feats = scraper.lemonde_scraper.scrapLeMonde( links_limit=-1, save_html=True, save_features_json=True)

htmls = scraper.lemonde_scraper.loadArticlesAsHtml("data/html")

feats = scraper.lemonde_scraper.loadFeaturesArticlesAsJson( "data/features" )
```

## Results
I did a successfully scraping on November the 4th: 116 articles extracted.

## Dependencies
 - Beautifoul Soup 4.6
 - urllib

# Clean the data

Goal: cleanse the data to get only relevant information

# Ranking

Goal: Write a method to get the relevant articles from the stored data, when given as input a keyword.
