from nltk.corpus import stopwords
import pandas as pd
import re

class Cleaner():
    def __init__(self):
        self.min_length = 4
        self.max_length = 120
        
    def clean_data(self, df):
        df["Docs"] = df.apply(lambda x: self._clean_doc(x.values[0]), axis=1)
        df = self._clean_corpus(df)
        return df
    
        
    def _clean_corpus(self, df):
        df = self._clean_duplicated_docs(df.dropna())
        return df.reset_index(drop=True)

    def _clean_doc(self, text):
        raw_df = self._build_data_frame(text)
        try:
            clean_text = (
                raw_df.pipe(self._min_length_control)
                .pipe(self._transform_to_lowercase)
                .pipe(self._replace_scape_chars)
                .pipe(self._remove_urls)
                .pipe(self._remove_twitter_mentions)
                .pipe(self._remove_special_chars)
                .pipe(self._replace_special_chars_with_space)
                .pipe(self._remove_numbers)
                .pipe(self._remove_repeated_tokens)
                .pipe(self._remove_twitter_retweets)
                .pipe(self._remove_stopwords)
                .pipe(self._length_control)
            )
            return clean_text
        except:
            return None
        
    def _clean_duplicated_docs(self, df):
        # df = df.drop_duplicates(subset=['Docs'])
        df = df.drop_duplicates()
        return df

    def _build_data_frame(self, text):
        raw_df = pd.DataFrame()
        raw_df['text'] = [text]
        return raw_df
    
    def _remove_stopwords(self, df):
        """
        Function for removing stopwords from spanish and unique characters
        """
        # print([word for word in df.text.values[0] if
        #                   word not in stopwords.words('spanish') and
        #                   len(word) > 1])
        text = ' '.join([word for word in df.text.values[0].split() if
                          word not in stopwords.words('spanish') and
                          len(word) > 1])
        return self._build_data_frame(text)

    def _length_control(self, df):
        """
        Function for controlling minimun and maximun length
        """
        length = len(df.text.values[0].split(' '))

        if length < self.min_length:
            return
        if length > self.max_length:
            df.text =  ' '.join(df.text.values[0].split(' ')[:self.max_length])
        return df.text.values[0]

    def _min_length_control(self, df):
        """
        Function for controlling minimun and maximun length
        """
        length = len(df.text.values[0].split(' '))
        if length < self.min_length:
            return
        return df

    def _replace_scape_chars(self, df):
        """
        Function for replacing scape chars like ENTER \ n for spaces 
        """
        df.text = df.text.values[0].replace('\n', ' ')
        return df


    def _remove_urls(self, df):
        """
        Function for removing urls from tweets
        """
        df.text = re.sub('(https?:)?\/\/[\w\.\/-]+', '', df.text.values[0])
        return df

    def _transform_to_lowercase(self, df):
        """
        Function for converting all chars to lowercase
        """
        df.text = df.text.values[0].lower()
        return df

    def _remove_special_chars(self, df):
        """
        Function for removing special chars like
        commas, periods, exclamations, ask marks and more
        """
        pattern = r'[~,#%:´"@“”"&()\/|¿+\.!¡\?¿;«»<>]'
        df.text = re.sub(pattern, '', df.text.values[0])
        return df

    def _replace_special_chars_with_space(self, df):
        """
        Function for removing special chars like
        commas, periods, exclamations, ask marks and more
        """
        pattern = r'-'
        df.text = re.sub(pattern, ' ', df.text.values[0])
        return df

    def _remove_twitter_mentions(self, df):
        """
        Function for replacing twitter mentions to users like @username
        """
        pattern = r'(^|[^@\w])@(\w{1,25})'
        df.text = re.sub(pattern, '', df.text.values[0])
        return df
    
    def _remove_twitter_retweets(self, df):
        """
        Function for removing rt word in retweets followed by __USERNAME__
        """
        pattern = r'\brt\b'
        df.text = re.sub(pattern, '', df.text.values[0])
        return df

    def _remove_numbers(self, df):
        """
        Function for replacing numberic characters by a unique token
        """
        pattern = r'((?:\d+\.?)?\d+,?\d+ | \d+)'
        df.text = re.sub(pattern, '', df.text.values[0])
        return df

    def _remove_repeated_tokens(self, df):
        """
        Function for removing repited words or Tokens
        """
        pattern = r'\b(\w+)(?:\W+\1\b)+'
        df.text = re.sub(pattern, r'\1', df.text.values[0])
        return df

