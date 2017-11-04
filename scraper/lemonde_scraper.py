"""
Library for scraping news on "Le Monde".
Get the HTML of articles and extract some features (see documentation).
Can load and save the HTML and features files.
"""

import urllib.request
import bs4
import os
import json


def getArticleLinksFromHomePage(links_limit=-1):
    """Scrap the "Le Monde" home page to find all the article links.
    "Le Monde" home page: "http://www.lemonde.fr".
    Return a list of links.

    Don't seek subscribed edition articles.

    Keyword arguments:
    links_limit -- number of links maximal to return, if -1 return all
    (default -1)
    """
    lemonde_url = "http://www.lemonde.fr"
    lemonde = bs4.BeautifulSoup(urllib.request.urlopen(lemonde_url).read(),
                                "lxml")
    links = []
    for a in lemonde('a'):
        if ( len(links) == links_limit ):
            break
        if len(a('', {'class': 'marqueur_restreint'})) == 0 \
                and "/article/" in a['href']:
            links.append(lemonde_url + a['href'])

    return links


def getHtmlArticleFromArticleLinks(links):
    """Scrap an Article and return a list of HTML code as string.

    Keyword arguments:
    links -- A list with all the article links to scrap
    """
    html_articles = []
    for link in links:
        html_articles.append(bs4.BeautifulSoup( urllib.request.urlopen(link).read(), "lxml" ).prettify())
    return html_articles


def extractFeaturesFromHtmlArticles(html_articles):
    """Return a list of json like object with all the features.
    Extract those features from the article:
     - Title
     - URL
     - Article category
     - Writer
     - Article description
     - Publish Time
     - Update Time
     - Article content
     - Related article titles

    Keyword arguments:
    html_articles -- A list of html articles in string type
    """
    features_articles = []
    for html in html_articles:
        features = {}
        article_lemonde = bs4.BeautifulSoup( html, "lxml" )
        # Title
        if len( article_lemonde('h1', {'class': 'tt2'}) ) > 0:
            features['title'] = article_lemonde('h1', {'class': 'tt2'})[0].text.strip()

        # Simple scrap
        if len( article_lemonde('', {'class':'description-article'}) ) > 0:
            features['article_description'] = article_lemonde('', {'class':'description-article'})[0].text

        if len( article_lemonde('div', {'id': 'articleBody'}) ) > 0:
            features['article_content'] = article_lemonde('div', {'id': 'articleBody'})[0].text.strip()

        related_articles = []
        if len( article_lemonde('aside', {'class':'bloc_base meme_sujet'}) ) > 0:
            for art in article_lemonde('aside', {'class':'bloc_base meme_sujet'})[0]('a'):
                related_articles.append(art.text.strip())
            features['related_articles'] = related_articles

        # Category
        if len ( article_lemonde('meta', {'property': 'og:url'}) ) > 0:
            offset = len("http://www.lemonde.fr")
            lemonde_article_url = article_lemonde('meta', {'property': 'og:url'})[0]['content']
            features['url'] = lemonde_article_url
            slash1 = lemonde_article_url.find('/', offset)+1
            slash2 = lemonde_article_url.find('/', slash1)+1
            if ( slash1 >= 0 and slash2 >= 0):
                features['category'] = lemonde_article_url[slash1:slash2-1]

        # Writer
        if len( article_lemonde('span', {'id': 'publisher'}) ) > 0:
            features['writer'] = article_lemonde('span', {'id': 'publisher'})[0].text.strip()

        # Date
        if len( article_lemonde('time', {'itemprop': 'datePublished'}) ) > 0:
            features['publish_time'] = article_lemonde('time', {'itemprop': 'datePublished'})[0]['datetime']

        if len( article_lemonde('time', {'itemprop': 'dateModified'}) ) > 0:
            features['update_time'] = article_lemonde('time', {'itemprop': 'dateModified'})[0]['datetime']

        features_articles.append( features )
    return features_articles


def saveArticlesAsHtml(html_articles,
                        url_articles,
                       location="data/html/"):
    """Save the html code on the disk.
    The html file name is the article title.

    Keyword arguments:
    html_articles -- A list of html articles in string type
    url_articles -- List of urls, the ones related to the html page
    (same size as html_articles)
    location -- where to save all the files (default: data/html/)
    """
    if not os.path.exists( location ):
        os.makedirs( location )

    for html, url in zip( html_articles, url_articles ):
        last_slash = url[::-1].find("/")
        html_file = location + url[len(url)-last_slash:]
        f = open( html_file, "w")
        f.write(html)
        f.close()

def loadArticlesAsHtml(location):
    """Load the html code from the disk.
    Return a list of html articles in string type.

    Keyword arguments:
    location -- where to open all the files
    """
    if not os.path.exists( location ):
        raise ValueError("Path (" + location + ") to find html pages doesn't exist.")

    if location[len(location)-1] is not "/":
        location = location + "/"

    html_articles = []
    for f_html in os.listdir( location ):
        if ".html" in f_html:
            f = open ( location + f_html, "r" )
            html_articles.append( f.read() )
            f.close()
    return html_articles

def saveFeaturesArticlesAsJson(features_articles,
                               location="data/features/"):
    """Save the features json like object from each article on the disk.

    Keyword arguments:
    features_articles -- A list features json like object
    location -- where to save all the files (default: data/features/)
    """
    if not os.path.exists( location ):
        os.makedirs( location )

    for feat in features_articles:
        last_slash = feat['url'][::-1].find("/")
        json_file = location + feat['url'][len(feat['url'])-last_slash:].replace("html", "json")
        f = open( json_file, "w")
        f.write( json.dumps( feat ) )
        f.close()

def loadFeaturesArticlesAsJson(location):
    """Load the features json like object from the disk.
    Return a list of features json like object.

    Keyword arguments:
    location -- where to open all the files
    """
    if not os.path.exists( location ):
        raise ValueError("Path (" + location + ") to find json features doesn't exist.")

    if location[len(location)-1] is not "/":
        location = location + "/"

    features_articles = []
    for f_json in os.listdir( location ):
        if ".json" in f_json:
            f = open ( location + f_json, "r" )
            features_articles.append( json.loads( f.read() ) )
            f.close()
    return features_articles

def scrapLeMonde(links_limit=-1,
                 subscribed_edition=False,
                 save_html=False,
                 save_features_json=False):
    """Scrap articles from Le Monde and extract features.

    Keyword arguments:
    links_limit -- number of links maximal to return, if -1 return all
    (default -1)
    subscribed_edition -- if subscribed article links should be return
    ( default false)
    save_html -- if save html on disk,
    save_features_json -- if save features on disk
    """
