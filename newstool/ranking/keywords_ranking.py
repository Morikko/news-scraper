from ..scraper import lemonde_scraper
import numpy as np
from scipy.sparse import find
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

class KeywordsRanker:
    def __init__(self, news_text):
        self.news_text = news_text

        self.loadStopWords()
        self.createTfIdfModel()

    def createTfIdfModel(self):
        if (self.news_text is None or len(self.news_text) == 0):
            raise ValueError("Data not loaded, can't prepare the TfIdf model.")

        if (self.stop_words is None or len(self.stop_words) == 0):
            self.stop_words = []

        self.text_clf = Pipeline([('vect', CountVectorizer(stop_words=self.stop_words)),
                                  ('tfidf', TfidfTransformer())])

        self.news_body_tfidf = self.text_clf.fit_transform(self.news_text)

    def loadStopWords(self, location="newstool/ranking/fr_stop_words.txt"):
        """Load a stop words dictionary

        Keyword arguments:
        location -- path to the dictionary
        """
        f = open(location)
        words = f.read()
        self.stop_words = words.split('\n')

        for i in range(len(self.stop_words) - 1, -1, -1):
            if self.stop_words[i] == "" or self.stop_words[i][0] == "#":
                del self.stop_words[i]
            else:
                # Remove accent
                self.stop_words[i] = unicodedata.normalize('NFKD', self.stop_words[i]).encode('ASCII', 'ignore')



def loadLeMondeTextArticles(features=[],
                            location="data/features"):
    """Prepare Le Monde articles to be indexed.
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
