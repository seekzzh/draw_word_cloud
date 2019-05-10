# drawBar.py
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.font_manager import *
import numpy as np

def drawStatBarh():
    '''
    画出词频统计条形图，用渐变颜色显示，选取前N个词频
    '''
    fig, ax = plt.subplots()
    myfont = FontProperties(fname='./fonts/simkai.ttf')
    N = 30
    words = []
    counts = []
    for line in open('词频统计(去停用词).txt', encoding='utf-8'):
        line.strip('\n')
        words.append(line.split(' ')[0])
        counts.append(int(line.split(' ')[1].strip('\n')))

    y_pos = np.arange(N)

    colors = ['#FA8072'] #这里是为了实现条状的渐变效果，以该色号为基本色实现渐变效果
    for i in range(len(words[:N]) - 1):
        colors.append('#FA' + str(int(colors[-1][3:]) - 1))

    rects = ax.barh(y_pos, counts[:N], align='center', color=colors)

    ax.set_yticks(np.arange(N))
    ax.set_yticklabels(words[:N],fontproperties=myfont)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_title('文本中的高频词汇',fontproperties=myfont, fontsize=17)
    ax.set_xlabel(u"出现次数",fontproperties=myfont)

    autolabel(rects, ax)
    plt.show()


def autolabel(rects, ax):
    """
    给条形图加上文字标签
    """
    #fig, ax = plt.subplots()
    for rect in rects:
        width = rect.get_width()
        ax.text(1.03 * width, rect.get_y() + rect.get_height()/2.,
            '%d' % int(width),ha='center', va='center')
