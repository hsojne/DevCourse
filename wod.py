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
    "Country" : target_data["Country"],
    "Description" : target_data["Significance"]
})

# df.info()

word_counter = Counter(df["Description"].dropna().str.lower().str.split().sum())
word_counter_df = pd.DataFrame(word_counter.items(), 
                               columns=["Word", "Frequency"]).sort_values(by="Frequency", ascending=False)
word_counter_df["Word"] = word_counter_df["Word"].str.replace('[,\.]', '')

# 전치사 드롭 
unnecessary = [
    'and', 'for', 'its', 'in', 'of', 'the', 'with', 'to', 'by', 'on', 
    'at', 'from', 'about', 'as', 'into', 'over', 'between', 'through', 
    'during', 'before', 'after', 'above', 'below', 'up', 'down', 
    'out', 'off', 'under', 'again', 'further', 'then', 'once', 'a', 'known', 
    'city', "town", "famous"
]

word_counter_df = word_counter_df[~word_counter_df['Word'].isin(unnecessary)]
word_counter_df["word_pct"] = word_counter_df["Frequency"] / np.sum(word_counter_df["Frequency"], axis = 0) * 100


# wordcloud
word_dict = word_counter_df.set_index("Word").to_dict()["Frequency"]

wc = WordCloud(random_state = 123, font_path = 'AppleGothic', width = 400,
               height = 400, background_color = 'white')

wc.generate_from_frequencies(word_dict)


plt.figure(figsize=(7, 7))
plt.imshow(wc)
plt.axis("off")
plt.show()