from ..scraper import lemonde_scraper

import numpy as np
import unicodedata
from scipy.sparse import find
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

class KeywordsRanker:
    def __init__(self, news_features=[], location="data/features"):
        self.news_features = news_features

        self.loadLeMondeTextArticles(location)

        self.loadStopWords()
        self.createTfIdfModel()

    def search(self, query, print_results=True, return_results=False, results_limit=5, all_keywords=False):
        """Search the keywords query inside the data

        Returns:
        list of articles index starting with best results
        list of tfidf scores for each article (ordered like features)

        Keyword arguments:
        query -- keywords
        print_results -- if true, print to the console the results
        results_limit -- # results max to return (default: 5)
        all_keywords -- if true, results should contain all keywords at least
        once (default: False)
        """
        if (self.news_body_tfidf is None):
            raise ValueError("TfIdf model not created, can't search")

        cumul_tfidf = np.zeros((len(self.news_text),1))
        words_index = self.text_clf.steps[0][1].get_feature_names()

        query_adapt = unicodedata.normalize('NFKD', query).encode('ASCII', 'ignore').decode("utf-8")
        query_adapt = query_adapt.lower()

        words_to_query = []
        for w in query_adapt.split():
            if w in words_index:
                words_to_query.append(words_index.index(w))
            """
            elif w in self.stop_words:
                print(w + " is a stop word.")
            else:
                print(w + " doesn't appear in any article.")
            """

        for w_index in words_to_query:
            article_index, _, tfidf_query = find(self.news_body_tfidf[:, w_index])
            for index, a_index in enumerate(article_index):
                cumul_tfidf[a_index] = cumul_tfidf[a_index] + tfidf_query[index]

        # Descending sorting
        results_index_articles = cumul_tfidf.argsort(axis=0)[::-1].flatten()
        results_index_articles = results_index_articles[0:results_limit]

        for i in range(len(results_index_articles)-1, -1, -1):
            if cumul_tfidf[results_index_articles[i]] < 0.01:
                results_index_articles = np.delete(results_index_articles, i)

        if ( print_results ):
            if results_index_articles.size == 0:
                print("No results for: " + query)
            for i, index in enumerate(results_index_articles):
                print(str(i+1) + ". " + self.news_features[index]['title'])
                print(" ----> Score: " + str(cumul_tfidf[index]) )
                print(self.news_features[index]['article_description'].strip())
                print()

        if ( return_results ):
            return results_index_articles, cumul_tfidf

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
                self.stop_words[i] = unicodedata.normalize('NFKD', self.stop_words[i]).encode('ASCII', 'ignore').decode("utf-8")

    def loadLeMondeTextArticles(self, location="data/features"):
        """Prepare Le Monde articles to be indexed.
        Return a list with the articles (title, description and content) inside.

        Keyword arguments:
        features -- if provided the json features already in memory
        (optional)
        location -- if no features are provided, the folder where to load the json features (default:"data/features")
        """
        if (self.news_features is None or len(self.news_features) == 0):
            self.news_features = lemonde_scraper.loadFeaturesArticlesAsJson(location)

        self.news_text = []
        for feat in self.news_features:
            input_text = feat['title'] + '\n' + \
                             feat['article_description'] + '\n' + \
                             feat['article_content']
            # Remove french accents
            input_text = unicodedata.normalize('NFKD', input_text).encode('ASCII', 'ignore').decode("utf-8")
            self.news_text.append( input_text )
