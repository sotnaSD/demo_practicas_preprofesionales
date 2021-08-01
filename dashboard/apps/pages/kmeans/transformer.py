
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

class Transformer():
    def __init__(self):
        pass
    
    def encode_data(self, method, docs):
        if method == 'TF-IDF':
            encoded_data = self._vectorize_data_with_TFIDF(docs)
        else:
            encoded_data = self._vectorize_data_with_BOW(docs)
            
        return  encoded_data
    
    def _vectorize_data_with_TFIDF(self, docs):
        """"
        Function to encode the data with TF-IDF
        """
        print('  Vectorizing data...\n')
        tfidf = TfidfVectorizer()
        encoded_data = tfidf.fit_transform(docs)
        return encoded_data

    def _vectorize_data_with_BOW(self, docs):
        """"
        Function to encode the data with BOW
        """
        print('  Vectorizing data...\n')
        bow = CountVectorizer()
        encoded_corpus = bow.fit_transform(docs)
        return encoded_corpus