import collections
import nltk
import jieba
import re
from nltk import word_tokenize, pos_tag  # 分词、词性标注
from nltk.corpus import stopwords  # 停用词
from nltk.stem import WordNetLemmatizer  # 词性还原

from nltk.corpus import wordnet

from nltk import word_tokenize

from pyecharts.charts import WordCloud

from pyecharts.globals import SymbolType

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

# 中文：去除分词结果中的无用词汇

def deal_txt(seg_list_exact):

  result_list = []

  with open('stop_words.txt', encoding='utf-8') as f:

    con = f.readlines()

    stop_words = set()

    for i in con:

      i = i.replace("\n", "")  # 去掉读取每一行数据的\n

      stop_words.add(i)

  for word in seg_list_exact:

    # 设置停用词并去除单个词

    if word not in stop_words and len(word) > 1:

      result_list.append(word)

  return result_list

# 渲染词云

def render_cloud(word_counts_top100):
    word1 = WordCloud(init_opts=opts.InitOpts(width='1350px', height='750px', theme=ThemeType.MACARONS))

    word1.add('词频', data_pair=word_counts_top100,

              word_size_range=[15, 108], textstyle_opts=opts.TextStyleOpts(font_family='cursive'),

              shape=SymbolType.DIAMOND)

    word1.set_global_opts(title_opts=opts.TitleOpts('评论云图'),

                          toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical'),

                          tooltip_opts=opts.TooltipOpts(is_show=True, background_color='red', border_color='yellow'))

    # 渲染在html页面上

    word1.render("评论云图.html")

def render_bar(word_counts_top50):

    x=[i[0] for i in word_counts_top50]
    y = [i[1] for i in word_counts_top50]
    print (x)

    keywords_count_bar = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("",y)
    # .add_yaxis(“”， list(keywords_count_dict.values())) 可以形成两个柱状图在一个坐标系中
    .reversal_axis()  # 反转坐标轴
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))  # 柱状图坐标上数字显示，不写默认为right
        .set_global_opts(
        title_opts=opts.TitleOpts(title="title"),  # 标题
        yaxis_opts=opts.AxisOpts(name="数量"),  # y轴
        xaxis_opts=opts.AxisOpts(name="关键词"),  # x轴
        datazoom_opts=opts.DataZoomOpts(type_="slider",orient='vertical')
    )
    )
    keywords_count_bar.render('title-word-count-bar.html')


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

def deal_chi(data):
    # 文本预处理 去除一些无用的字符  只提取出中文出来

    new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)

    new_data = " ".join(new_data)

    # jieba分词将整句切成分词

    seg_list_exact = jieba.cut(new_data, cut_all=True)

    # 去掉无用词汇

    final_list = deal_txt(seg_list_exact)
    return final_list
#词性判断
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

if __name__ == '__main__':
    #下载所需资源
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

    print ("\033[1;34m中英文词云生成\n")
    print("Chinese and English wordcloud generator\n")
    print("王珊 南京大学 Nanjing University, Nanjing 210023, P.R.China\n")
    print("https://shannju.github.io/ \n")

    print("请选择词云语言 （ Please select the language for wordcloud）:\n")
    lan = input("中文词云按0、英文按1 （ Press 0 to generate Chinese wordcloud, 1 for english）\n")

    print("请输入文件夹路径（相对绝对都可）（ Please enter the folder path）")
    filename = input("注意：请使用utf-8编码txt （Note：Please use utf-8 to encode txt） \n")
    # 读取文件
    with open(filename, encoding='utf-8') as f:
        data = f.read()
    cutwords=[]

    if(lan=='1'):
        data = data.lower()
        cutwords =deal_eng(data)
    elif(lan=='0'):
        cutwords = deal_chi(data)


    # 筛选后统计
    word_counts = collections.Counter(cutwords)

    # 获取前100最高频的词

    word_counts_top100 = word_counts.most_common(100)

    # 可以打印出来看看统计的词频

    print(word_counts_top100)

    # 渲染词云
    print("词云已经生成（Word cloud has been generated）")
    render_cloud(word_counts_top100)

    print("柱状图已经生成（Bar has been generated）")
    render_bar(word_counts_top100[1:])
