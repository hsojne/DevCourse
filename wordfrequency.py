import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from collections import Counter
import seaborn as sns


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

# --------------------total Fre-------------------------------------

## str split
word_counter = Counter(df["Description"].dropna().str.lower().str.split().sum())
word_counter_df = pd.DataFrame(word_counter.items(), 
                               columns=["Word", "Frequency"]).sort_values(by="Frequency", ascending=False)
word_counter_df["Word"] = word_counter_df["Word"].str.replace('[,\.]', '')

# drop values
unnecessary = [
    'and', 'for', 'its', 'in', 'of', 'the', 'with', 'to', 'by', 'on', 
    'at', 'from', 'about', 'as', 'into', 'over', 'between', 'through', 
    'during', 'before', 'after', 'above', 'below', 'up', 'down', 
    'out', 'off', 'under', 'again', 'further', 'then', 'once', 'a', 'known', 
    'city', "town", "famous"
]

word_counter_df = word_counter_df[~word_counter_df['Word'].isin(unnecessary)]
word_counter_df["word_pct"] = word_counter_df["Frequency"] / np.sum(word_counter_df["Frequency"], axis = 0) * 100

fig, ax = plt.subplots(figsize =(10, 5))
# Horizontal Bar Plot
Word = word_counter_df["Word"].head(10) ; pct = word_counter_df["word_pct"].head(10)
ax.barh(Word, pct)

# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)

# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)

# Add x, y gridlines
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)

# Show top values 
ax.invert_yaxis()

# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5, 
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')

# Add Plot Title
ax.set_title('Word Frequency ratio',
             loc ='left', )

# Show Plot
plt.show()




