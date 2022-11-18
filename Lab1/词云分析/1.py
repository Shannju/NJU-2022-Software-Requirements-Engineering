import collections
import nltk
import jieba
import re
import pandas as pd
import numpy as np
from sklearn import ensemble
from sklearn import ensemble
from nltk import word_tokenize, pos_tag  # 分词、词性标注
from nltk.corpus import stopwords  # 停用词
from nltk.stem import WordNetLemmatizer  # 词性还原

from nltk.corpus import wordnet

from nltk import word_tokenize

from pyecharts.charts import WordCloud

from collections import Counter
from wordcloud import WordCloud

from pyecharts.globals import SymbolType

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType


from sklearn.feature_extraction.text import CountVectorizer#词袋
from sklearn.feature_extraction.text import TfidfTransformer#tfidf

from Code.main import get_wordnet_pos


def deal_eng(data):
    with open("english stopwords.txt", encoding='utf-8') as f:
        stopwords_list = f.read()

    cutwords1 = word_tokenize(data)  # 分词
    # print (cutwords1)

    interpunctuations = [',', ' ', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#',
                         '$', '%','//','=','{','}','...','``','i','1','2','3',"''","'s",'>','<','0',"'",'-','+','--','...','/','use']  # 定义符号列表
    cutwords2 = [word for word in cutwords1 if word not in interpunctuations]  # 去除标点符
    # print(cutwords2)
    cutwords25 = [word for word in cutwords2 if word not in stopwords_list]  # 去除标点符号
    stops = set(stopwords.words("english"))
    cutwords3 = [word for word in cutwords25 if word not in stops]  # 判断分词在不在停用词列表内
    # print(cutwords3)
    tagged_words = pos_tag(cutwords3)
    wnl = WordNetLemmatizer()
    cutwords4 = []
    for tag in tagged_words:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        cutwords4.append(wnl.lemmatize(tag[0], pos=wordnet_pos))  # 词形还原
    return cutwords4
def remove_punctuation(line):
    line = str(line)
    if line.strip() == '':
        return ''
    rule = re.compile(u"[^a-zA-Z0-9\u4E00-\u9FA5] ")
    line = rule.sub(' ', line)
    return line

df = pd.read_csv('qa11.csv')

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf8').readlines()]
    return stopwords

# 加载停用词
stopwords = stopwordslist("english stopwords.txt")
df['question']=df['question'].apply(remove_punctuation)
# for i in range(len(df)):
#     if str(df['question'][i]).isdigit() == True:
#         df['question'][i] = " "
for i in range(len(df)):
    df['question'][i] = df['question'][i].lower()

df['question']=df['question'].apply(lambda x:" ".join([w for w in list(word_tokenize(x)) if w not in stopwords]))
print(df)

#词向量转换
count_vect = CountVectorizer()
X = count_vect.fit_transform(df['question'])

#tf-idf
tfidf_transformer = TfidfTransformer()
X_tfidf = tfidf_transformer.fit_transform(X)
print(X_tfidf)

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# '利用SSE选择k'
SSE = []  # 存放每次结果的误差平方和
for k in range(1, 9):
    estimator = KMeans(n_clusters=k)  # 构造聚类器
    estimator.fit(X_tfidf)
    SSE.append(estimator.inertia_)
X = range(1, 9)
plt.xlabel('k')
plt.ylabel('SSE')
plt.plot(X, SSE, 'o-')
plt.show()
# K均值聚类
model_kmeans = KMeans(n_clusters=8,random_state=1)  # 创建聚类模型对象
model_kmeans.fit(X_tfidf)  # 训练模型

# 聚类结果
cluster_labels = model_kmeans.labels_  # 聚类标签结果
print(cluster_labels)
#结果拼接
labels=pd.DataFrame(cluster_labels,columns=['标签'])
shuju=pd.concat([df['question'],labels],axis=1)
print(shuju)

cat_desc = dict()
biaoqian_values=[0,1,2,3,4,5,6]#聚类标签
for i in biaoqian_values:
    text = shuju.loc[shuju['标签'] == i, 'question']
    text = (' '.join(map(str, text))).split(' ')
    cat_desc[i] = text
print(cat_desc[2])#打印2类词汇
#词云图
#查看词云

def generate_wordcloud(tup):
    wordcloud = WordCloud(background_color='white',
                          font_path='simhei.ttf',
                          max_words=50, max_font_size=40,
                          random_state=42
                          ).generate(str(tup))
    return wordcloud
fig, axes = plt.subplots(4, 2, figsize=(30, 38))

k = 0
for i in range(4):
    for j in range(2):
        most10 = Counter(cat_desc[k]).most_common(20)#10个高频词
        ax = axes[i, j]
        ax.imshow(generate_wordcloud(most10), interpolation="bilinear")
        ax.axis('off')   #坐标视为不可见,但坐标系的title视为可见.
        ax.set_title("{} class".format(k), fontsize=15)

        if k<6:
           k += 1

plt.show()

