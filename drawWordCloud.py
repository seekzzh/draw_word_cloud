# drawWordCloud.py
# -*- coding: utf-8 -*-
#
# 作者：seekzzh
# 创建时间:'2019/5/6'

import docx
import jieba
import codecs
from os import path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import drawBar
import readPDF
import time


# 当前路径
d = path.dirname(__file__)

def readDocx(filePath):
    '''
    获取文档对象，将文档内容按段落读入，并存入doc中
    '''
    file = docx.Document(filePath)
    doc = ""
    for para in file.paragraphs:
        doc = doc + para.text

    return doc

def readTxt(filePath):
    '''
    读取TXT文档中的内容
    :param filepath:
    :return:
    '''
    doc = open(path.join(d, filePath)).read()
    return doc

def segment(doc):
    '''
    用jieba分词对输入文档进行分词，并保存至本地（根据情况可跳过）
    '''
    seg_list = " ".join(jieba.cut(doc, cut_all=False)) #seg_list为str类型
    document_after_segment = open('分词结果.txt', 'w+', encoding='utf-8')
    document_after_segment.write(seg_list)
    document_after_segment.close()

    return seg_list


def wordCount(segment_list):
    '''
        该函数实现词频的统计，并将统计结果存储至本地。
        在制作词云的过程中用不到，主要是在画词频统计图时用到。
    '''
    word_lst = []
    word_dict = {}
    with open('词频统计(去停用词).txt','w', encoding='utf-8') as wf2:
        word_lst.append(segment_list.split(' '))
        for item in word_lst:
            for item2 in item:
                if item2 not in word_dict:
                    word_dict[item2] = 1
                else:
                    word_dict[item2] += 1

        word_dict_sorted = dict(sorted(word_dict.items(), key = lambda item:item[1], reverse=True))#按照词频从大到小排序
        for key in word_dict_sorted:
            wf2.write(key+' '+str(word_dict_sorted[key])+'\n')
    wf2.close()

def drawWordCloud(seg_list):
    '''
        制作词云
        设置词云参数
    '''
    color_mask = np.array(Image.open(path.join(d, "./imageMask/heart.png")))
    wc = WordCloud(
        #设置字体，不指定就会出现乱码，注意字体路径
        ## 系统字体可以直接写名称
        # font_path="simhei.ttf", # simhei 黑体 | simkai 楷体 | simfang 仿宋 |
        ## 非系统字体需要下载字体文件
        font_path=path.join(d,'./fonts/hwxh.ttf'),
        # | arialuni Arial Unicode MS | msyh 微软雅黑 | msjh 微软正黑 | hwxk 华文行楷 | hwxh 华文细黑
        #设置背景色
        background_color='white',
        #词云形状
        mask=color_mask,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=60,
        # 画布缩放比例，默认是mask的尺寸
        scale=4,
        # mode='RGBA',
    )
    wc.generate(seg_list) # 产生词云
    image_colors = ImageColorGenerator(color_mask)
    wc.to_file("./outputImages/wordCloud.png") #保存图片
    #  显示词云图片
    plt.imshow(wc, interpolation="bilinear")
    plt.axis('off')

    #这里主要为了实现词云图片按照图片颜色取色
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")

    plt.show()

def removeStopWords(seg_list):
    '''
    读取停用词表，该函数实现去停用词
    '''
    wordlist_stopwords_removed = []

    stop_words = open('./stopwords/CNENstopwords.txt', encoding='utf-8')
    stop_words_text = stop_words.read()

    stop_words.close()

    stop_words_text_list = stop_words_text.split('\n')
    after_seg_text_list = seg_list.split(' ')

    for word in after_seg_text_list:
        if word not in stop_words_text_list:
            wordlist_stopwords_removed.append(word)

    without_stopwords = open('分词结果(去停用词).txt', 'w', encoding='utf-8')
    without_stopwords.write(' '.join(wordlist_stopwords_removed))
    return ' '.join(wordlist_stopwords_removed)


if __name__ == "__main__":
    time1 = time.time()
    '''读取txt文档'''
    # doc = readTxt("./content/DRLIR.txt")
    '''读取docx文档'''
    doc = readDocx("./content/DRLIR.docx")
    '''读取PDF文档'''
    # doc = readPDF.parse('./content/DRLIR.pdf')
    segment_list = segment(doc)
    segment_list_remove_stopwords = removeStopWords(segment_list)
    drawWordCloud(segment_list_remove_stopwords)
    wordCount(segment_list_remove_stopwords)
    time2 = time.time()
    print('总共耗时：', time2 - time1)
    '''绘制词频直方图'''
    drawBar.drawStatBarh()


'''WordCloud参数设置'''
# font_path : string //字体路径，需要展现什么字体就把该字体路径+后缀名写上，如：font_path = '黑体.ttf'
# scale : float (default=1) //按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍。
# stopwords : set of strings or None //设置需要屏蔽的词，如果为空，则使用内置的STOPWORDS

# font_path : string //字体路径，需要展现什么字体就把该字体路径+后缀名写上，如：font_path = '黑体.ttf'
# width : int (default=400) //输出的画布宽度，默认为400像素
# height : int (default=200) //输出的画布高度，默认为200像素
# prefer_horizontal : float (default=0.90) //词语水平方向排版出现的频率，默认 0.9 （所以词语垂直方向排版出现频率为 0.1 ）
# mask : nd-array or None (default=None) //如果参数为空，则使用二维遮罩绘制词云。如果 mask 非空，设置的宽高值将被忽略，遮罩形状被 mask 取代。
# 除全白（#FFFFFF）的部分将不会绘制，其余部分会用于绘制词云。如：bg_pic = imread('读取一张图片.png')，
# 背景图片的画布一定要设置为白色（#FFFFFF），然后显示的形状为不是白色的其他颜色。可以用ps工具将自己要显示的形状复制到一个纯白色的画布上再保存，就ok了。
# scale : float (default=1) //按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍。
# min_font_size : int (default=4) //显示的最小的字体大小
# font_step : int (default=1) //字体步长，如果步长大于1，会加快运算但是可能导致结果出现较大的误差。
# max_words : number (default=200) //要显示的词的最大个数
# stopwords : set of strings or None //设置需要屏蔽的词，如果为空，则使用内置的STOPWORDS
# background_color : color value (default=”black”) //背景颜色，如background_color='white',背景颜色为白色。
# max_font_size : int or None (default=None) //显示的最大的字体大小
# mode : string (default=”RGB”) //当参数为“RGBA”并且background_color不为空时，背景为透明。
# relative_scaling : float (default=.5) //词频和字体大小的关联性
# color_func : callable, default=None //生成新颜色的函数，如果为空，则使用 self.color_func
# regexp : string or None (optional) //使用正则表达式分隔输入的文本
# collocations : bool, default=True //是否包括两个词的搭配
# colormap : string or matplotlib colormap, default=”viridis” //给每个单词随机分配颜色，若指定color_func，则忽略该方法。
# fit_words(frequencies) //根据词频生成词云【frequencies，为字典类型】
# generate(text) //根据文本生成词云
# generate_from_frequencies(frequencies[, ...]) //根据词频生成词云
# generate_from_text(text) //根据文本生成词云
# process_text(text) //将长文本分词并去除屏蔽词（此处指英语，中文分词还是需要自己用别的库先行实现，使用上面的 fit_words(frequencies) ）
# recolor([random_state, color_func, colormap]) //对现有输出重新着色。重新上色会比重新生成整个词云快很多。
# to_array() //转化为 numpy array
# to_file(filename) //输出到文件

