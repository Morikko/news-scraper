"""
Library for scraping news on "Le Monde".
Get the HTML of articles and extract some features (see documentation).
Can load and save the HTML and features files.
"""

import urllib
import bs4


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


def saveArticlesAsHtml(html_articles,
                       location="data/html/"):
    """Save the html code on the disk.
    The html file name is the article title.

    Keyword arguments:
    html_articles -- A list of html articles in string type
    location -- where to save all the files (default: data/html/)
    """


def loadArticlesAsHtml(location):
    """Load the html code from the disk.
    Return a list of html articles in string type.

    Keyword arguments:
    location -- where to open all the files
    """


def saveFeaturesArticlesAsJson(features_articles,
                               location="data/features/"):
    """Save the features json like object from each article on the disk.

    Keyword arguments:
    features_articles -- A list features json like object
    location -- where to save all the files (default: data/features/)
    """


def loadFeaturesArticlesAsJson(location):
    """Load the features json like object from the disk.
    Return a list of features json like object.

    Keyword arguments:
    location -- where to open all the files
    """


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
