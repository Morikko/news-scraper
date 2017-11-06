from ..scraper import lemonde_scraper
import numpy as np
from scipy.sparse import find

def loadTextArticles( features=[],
                      location="data/features"):
    """Load articles to index.
    Return a list with the articles (title, description and content) inside.

    Keyword arguments:
    features -- if provided the json features already in memory
    (optional)
    location -- if no features are provided, the folder where to load the json features (default:"data/features")

    """
    if ( len(features) == 0 ):
        features = lemonde_scraper.loadFeaturesArticlesAsJson( location)


    news_text = []
    for feat in features:
        news_text.append( feat['title'] + '\n' +
                          feat['article_description'] + '\n' +
                          feat['article_content']
                        )
    return news_text
