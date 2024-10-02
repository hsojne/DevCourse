import pyecharts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from collections import Counter
import seaborn as sns
from wordcloud import WordCloud

# data
data = pd.read_csv("destinations.csv")
target_data = data[["Country", "Cultural Significance","Description"]]

# info
#target_data.info()

# Cultural Significance + Description
target_data["Description"] = target_data["Description"].fillna(" ")
target_data["Significance"] = target_data["Cultural Significance"].map(str) + " " + target_data["Description"]


# total data set
df = pd.DataFrame({
    "Country" : data["Country"],
    "City" : data["Destination"],
    "Description" : target_data["Significance"]
})

unnecessary = [
    'known', 'city', "town", "famous"
]

for word in unnecessary:
    df["Description"] = df["Description"].str.lower().str.replace(word, "").str.strip()



# ---------------------------TI-------------------------------------
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vec = TfidfVectorizer(stop_words='english', max_features=200)

# TF-IDF matrix
tfidf_matrix = tfidf_vec.fit_transform(df['Description'])

# to df
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vec.get_feature_names_out( ), index=data["Country"])
country_top_keywords = tfidf_df.groupby('Country').mean().idxmax(axis=1).reset_index()
country_top_keywords.columns = ['Country', 'Top Keyword']


def top_n_keywords(row, n=3):
    top_keywords = row.sort_values(ascending=False).head(n)
    return list(top_keywords.index)

# 국가별 상위 3개의 키워드 추출
#country_top_keywords = tfidf_df.groupby('Country').apply(lambda row: top_n_keywords(row, 3), axis=1)

print(country_top_keywords)