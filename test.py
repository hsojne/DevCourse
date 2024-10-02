import pandas as pd

# 예시 데이터프레임 생성
data = {'text_column': ['  A Renaissance city   ', ' famous for its art, ', 'archite']}
df = pd.DataFrame(data)

words_to_remove = ["city", "for"]


for word in words_to_remove:
    df["text_column"] = df["text_column"].str.replace(word, "").str.strip()

print(df)