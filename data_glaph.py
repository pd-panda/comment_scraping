# -*- coding: utf-8 -*-
"""data_glaph.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TBzglP70ydbpRW4ocgcyjFy6WyAcMKMX
"""

# -*- coding: utf-8 -*-
"""data_glaph
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1JmnJ4h2wpPxI28fXUHfkWyFU7eqYwSSM
"""

import matplotlib.pyplot as plt#
import japanize_matplotlib
import matplotlib#
from matplotlib import style#
import pandas as pd#
#import datetime#
import os
import shutil
import squarify#
import seaborn as sns#
import codecs
import numpy as np
# coding:utf-8
import csv
from bs4 import BeautifulSoup#
from collections import Counter, defaultdict
sns.set(font="IPAexGothic") #日本語フォント設定
from pyknp import Juman#
#京都大学大学院情報学研究科知能情報学専攻黒橋・褚・村脇研究室 (http://nlp.ist.i.kyoto-u.ac.jp/)
import warnings
warnings.filterwarnings('ignore')
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from urllib.parse import urlparse
sourcedir = "./Source"

class DataGraph:
#-----------csvファイルをデータフレームに変換--------------
    def csv_df(self, fname):
        df = pd.read_csv(os.path.join(sourcedir, fname))
        df = df.dropna(how='all').dropna(how='all', axis=1)
        return df
#-----------------------------------------------------------treemap---------------------------------------------------------
#------------------treemap出力用------------------------　
    #引数:データフレームとタイトル
    def print_treemap(self, df, title, fig, ax) :
        #ソート
        df = self.rank_sort(df,False)
        #最大文字数検索
        max_num = self.max_word_num(df) 

        sns.set()
        matplotlib.rcParams['figure.figsize'] = (16.0, 9.0)
        # ggplot style使用
        style.use('ggplot')
        sns.set(font="IPAexGothic") #日本語フォント設定

        #fig, ax = plt.subplots()
        # Colormap
        cmap = matplotlib.cm.Blues

        # Min and Max Values
        #割合作成後dfに追加
        df = self.add_percent(df)
        mini = min(df["Population"])
        maxi = max(df["Population"])   

        # colors setting
        norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
        colors = [cmap(norm(value)) for value in df["Population"]]

        # Plotting
        #squarify.plot(sizes=df["Population"], label=df['word'], alpha=0.8, color=colors, text_kwargs={'fontsize':int(100/max_num),'color':'black'})
        squarify.plot(sizes=df["Population"], label=df['word'], alpha=0.8, color=colors)
        # 軸削除
        plt.axis('off')
        # y軸逆に
        plt.gca().invert_yaxis()
        # タイトル、位置設定
        plt.title(title, fontsize=32,fontweight="bold")
        ttl = ax.title
        ttl.set_position([.5, 1.05])
        # 背景色
        fig.set_facecolor('#ffffff')

#-------------------割合作成後dfに追加----------------------
    def add_percent(self, df) :
        s = df['point'].sum()
        df["Population"] = 0.0

        for i in range(len(df['point'])) :
            a = df['point'][i] /float(s) * 100.0
            df["Population"][i] = a

        return df
#--------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------構文解析&データ作成---------------------------------------------------------

#------------コメントデータからデータ抽出＆データフレーム作成--------------
    def string_word_point(self, df):
        jumanpp = Juman(jumanpp=False)
        tmp_word =[]
        df_time_word = pd.DataFrame(index=[], columns=['time','word']) #単語と時間のｄｆ
        df_word_point = pd.DataFrame(index=[], columns=['word','point'])#単語とその出現数のｄｆ
        df_time_point = pd.DataFrame(index=[], columns=['time','point'])#時間とその時のコメント数のｄｆ
        df_time_www_point = pd.DataFrame(index=[], columns=['time','point'])#時間とその時のwww数のｄｆ
        df_time_hakusyu_point = pd.DataFrame(index=[], columns=['time','point'])#時間とその時の拍手数のｄｆ
        df_URL_point = pd.DataFrame(index=[], columns=['URL','point'])#URLまとめdf
        
        #print(df_word_point)
        for i in range(len(df)):
             #URLだったら追加
            url=URL_hanbetu(df['comment'][i])
            if url != False:
                tmp = self.my_index(df_URL_point['URL'],url)
                df_URL_point = self.make_df_append(df_URL_point,tmp,url)

            #print("記号削除前")
            #print(df_word_point)
            #記号削除中
            print(df['comment'][i])
            df['comment'][i] = self.my_delete(df['comment'][i])
            # h:m:s -> hms　に変更
            tmp_time = self.strtime_to_inttime(df['time'][i])
                    
            #時間ごとのコメント数計算
            tmp = self.my_index(df_time_point['time'],tmp_time)
            df_time_point = self.make_df_append(df_time_point,tmp,tmp_time)
            #wwwがあったら1追加なかったら0追加
            print(url)
            if False != self.www_hanbetu(df['comment'][i]) and url == False:
                df_time_www_point = self.make_df_append(df_time_www_point,tmp,tmp_time)
            else:
                if False == tmp :
                    df_time_www_point = df_time_www_point.append({'time': tmp_time, 'point': 0}, ignore_index=True)
            #拍手があったら1追加なかったら0追加
            if False != self.hakusyu_hanbetu(df['comment'][i]):
                df_time_hakusyu_point = self.make_df_append(df_time_hakusyu_point,tmp,tmp_time)
            else:
                if False == tmp :
                    df_time_hakusyu_point = df_time_hakusyu_point.append({'time': tmp_time, 'point': 0}, ignore_index=True)

                #構文解析
                result = jumanpp.analysis(df['comment'][i])
                #print(result)
                #分析結果からdf作成
                for token in result.mrph_list():
                    tmp_word = token.midasi   
                #名詞の出現数計算
                    if 0 != self.word_Classification(token.hinsi):
                    #名詞なら
                        if self.word_Classification(token.hinsi) == '名詞':    
                            tmp = self.my_index(df_word_point['word'],tmp_word)
                            df_word_point = self.make_df_append(df_word_point,tmp,tmp_word)
                        #名詞とその時の時間
                            df_time_word = df_time_word.append({'time':tmp_time,'word': tmp_word}, ignore_index=True)

        return df_time_word,df_word_point,df_time_point,df_time_www_point, df_time_hakusyu_point,df_URL_point


#---------------dfデータ追加プログラム-------------------
def make_df_append(self,df,index,data):
    if False !=index :
        df[df.columns[1]][index]+=1
        return df
    else :
        return df.append({df.columns[0]: data, df.columns[1]: 1}, ignore_index=True)

#---------------記号削除用プログラム-------------------
    def my_delete(self, string) :
        if '\n' in string:
            string = string.replace('\n', ' ')
        if '@' in string:
            string = string.replace('@', ' ')
        
        return string

#----------------- h:m:s -> hms　に変更----------------
    def strtime_to_inttime(self, time):
        string = time.replace(':', '')
        return int(string)

#----------------品詞検索用---------------------------
    def word_Classification(self, tmp):
        if tmp == '名詞':
            return'名詞'
        else :return 0

#----------------笑い判別用プログラム---------------------------
    def www_hanbetu(self, word):
        if 'ww' in word:
            tmp=word.index('w')
            if tmp == len(word)-1:
                return True
            if word[tmp + 1] == 'w':
                return True
            else :return False
        elif '笑' == word:
            return True
        elif '草' == word:
            return True
        else:return False 
#----------------拍手判別用プログラム--------------------------
    def hakusyu_hanbetu(self,string):
        if '8' in string:
            for char in string:
                if char != '8':
                    return False
            return True
        if '８' in string:
            for char in string:
                if char != '８':
                    return False
            return True
        else:return False 
#----------------URL判別用プログラム--------------------------
    def URL_hanbetu(self,string):
        parsed_url = urlparse(string)
        if 'h' in parsed_url.scheme:
            url = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(string))
        else : url = False
    
        return url 

#--------------------------------------------------------------------------------------------------------------------------------------
#------------------------いろんなdf作成------------------------------------------------------

#-----------------人とその人のコメント数のdf作成---------------
    def make_df_contributor_point(self, df):
        df_contributor_point = pd.DataFrame(index=[], columns=['contributor','point'])#時間とその時のコメント数のｄｆ
        valu = df['contributor'].value_counts()
        name =  df['contributor'].unique()
        for i in range(len(name)) :
            if 'プライベート' in name[i]:
                tmp = name[i]
            else :
                df_contributor_point = df_contributor_point.append({'contributor':name[i],'point': valu[i]}, ignore_index=True)
        return df_contributor_point

#========================データ作成(折れ線グラフ)=================================
#------------------各時間の単語ごとの出現数のdf作成---------------------------
    def time_word_point(self, df_time_word,df_word_point,df_time_point) :
        df_time_word_point_stack = pd.DataFrame(index=[])
        df_time_word_point_line = pd.DataFrame(index=[])
        df_time_word_point_stack['time'] = df_time_point['time']
        df_time_word_point_line['time'] = df_time_point['time']

        word = df_word_point['word']

        for row in word:
            df_time_word_point_stack[row] = 0
            df_time_word_point_line[row] = 0
            #特定の単語の配列番号取得
            tmp_list = [i for i, x in enumerate(df_time_word['word'] == row) if x == True]
        
            for i in tmp_list:
                tmp = df_time_word_point_stack['time'].values.tolist().index(df_time_word['time'][i])
                df_time_word_point_stack[row][tmp:] +=1
                df_time_word_point_line[row][tmp] +=1

        return df_time_word_point_stack,df_time_word_point_line

#---------------各時間の人ごとの出現数のdf作成-----------------------------------
    def time_contributor_point(self, df,df_time_point,df_contributor_point) :
        df_time_contributor_point_stack = pd.DataFrame(index=[])
        df_time_contributor_point_line = pd.DataFrame(index=[])
        df_time_contributor_point_stack['time'] = df_time_point['time']
        df_time_contributor_point_line['time'] = df_time_point['time']

        contributor = df_contributor_point['contributor']

        #print(df_time_contributor_point_stack['time'])

        for row in contributor:
            df_time_contributor_point_stack[row] = 0
            df_time_contributor_point_line[row] = 0
            #特定の単語の配列番号取得
            tmp_list = [i for i, x in enumerate(df['contributor'] == row) if x == True]
        
            for i in tmp_list:
                tmp = df_time_contributor_point_stack['time'].values.tolist().index(self.strtime_to_inttime(df['time'][i]))
                df_time_contributor_point_stack[row][tmp:] +=1
                df_time_contributor_point_line[row][tmp] +=1

        return df_time_contributor_point_stack,df_time_contributor_point_line
#====================================================================================================
#--------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------自作関数(便利用)-------------------------------------------------

#-----------------配列の中に一個でもtureがあればその番号を返す---------------------------
    def my_Ture(self, row):
        for i in range(len(row)) :
            if row[i] :
                return i
        return False

#----------------dfの中にxがあればその配列番号をなければFalseを返す-------------------
    def my_index(self, l, x, default=False):
        l = l.values.tolist()
        if x in l:
            return l.index(x)
        else:
            return default

#--------------------pointでソート--------------------------------------------------
    def rank_sort(self, df,flag):
        return df.sort_values('point',ascending=flag)

#-----------------上位いくつかの単語だけ抽出--------------------------------------
    def make_rank_word (self, ranknum,df__point,word):
        if ranknum > len(df__point):
            ranknum = len(df__point)
        elif ranknum < 0:
            ranknum = 0
    
        df__point = self.rank_sort(df__point,False)
        return df__point[word][0:ranknum]
    
#-----------------最大文字数--------------------------------------
    def max_word_num(self,df):
        max = 0
        for word in df['word']:
            if max < len(word) :
                max = len(word)

        return max
#--------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------棒グラフ---------------------------------------------------------

#---------------------棒グラフ出力用--------------------------
    def print_bar_graph_df(self, df, calamu, fig, ax):
        df = self.rank_sort(df,True)
        plt.tight_layout()
        plt.rcParams["font.size"] = 25
        #plt.figure(figsize=(10,20 ), dpi=50,facecolor='#FFFFFF')
        plt.barh(df[calamu], df['point'])
        plt.grid(which='major',color='black',linestyle='-',axis = "x")
        #plt.show()

#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------感情推定----------------------------------------

#----------各時間でのネガティブかポジティブかをdfに-------------------------
    def make_df_time_negapozi(self, df_time_word,df_time_point,df_kanzyou):
        df_time_negapozi = pd.DataFrame(index=[])
        df_time_negapozi['time'] = df_time_point['time']
        df_time_negapozi['negapozi'] = 0
        c=0
        for i in range(len(df_time_negapozi)):
        
            while df_time_negapozi['time'][i] == df_time_word['time'][c]:
                tmp = self.my_index(df_kanzyou['word'],df_time_word['word'][c])
                if tmp == False:
                    df_time_negapozi['negapozi'][i:] += 0
                else:
                    if  'p' in df_kanzyou['negapozi'][tmp]:
                        df_time_negapozi['negapozi'][i:] += 1
                    if  'n' in df_kanzyou['negapozi'][tmp]:
                        df_time_negapozi['negapozi'][i:] -= 1   
                c+=1
                if c >= len(df_time_word) :
                     return df_time_negapozi
    
        return df_time_negapozi
#--------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------get関数-------------------------------------------------

    # 単語（名詞）の数を取得
    def get_word_num(self):
        return len(self.df_word_point['word'])

    # 単語（名詞）を全て取得
    def get_all_word(self):
        return self.df_word_point['word']

    # 投稿者数の取得
    def get_contributor_num(self):
        return len(self.df_contributor_point['contributor'])

    # 投稿者名を全て取得
    def get_all_contributor(self):
        return self.df_contributor_point['contributor']
    
    # 最初・最後のコメント投稿時間の取得
    def get_start_end_time(self):
        return self.df_time_point[0],self.df_time_point[-1]
    
    # コメント投稿時間を全て取得
    def get_all_time(self):
        return self.df_time_point['time']
    
    # 投稿されたURLを全て取得
    def get_all_URL(self):
        return self.df_URL_point['URL']
#--------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------散布図---------------------------------------------------------
#----------------------------------wwwwww描画用-------------------------------------------
#wwwの散布図表示用
    def print_www(self,df,cutnum, fig, ax, flag='line'):
        df = self.df_time__(df,cutnum,flag)
        i = 0
        plt.tick_params(labelbottom=True,
            labelleft=False,
            labelright=False,
            labeltop=False)
        flag = False
        colx = df[df.columns[0]]
        #ax = plt.figure(figsize=(30,10), dpi=50,facecolor='#FFFFFF')     
        for tmp in df['point']:
            x =[]
            y = np.random.rand(tmp)
            for j in range(tmp):
                x = x + [colx[i]]
            color = self.rand_green(np.random.rand(1))
            if tmp > 0:
                flag = True
            i+=1
            plt.scatter(x,y, c=color,s=1800, marker="$w$",alpha=0.5)
        if  flag == True:
            if len(colx) > 5:
            # 時間のラベルを5個に変更
                plt.xticks(colx[0::(-(-len(colx)//5))])        


        #plt.show()
#色決め
    def rand_green(self,rand):
        if rand <= 0.1:
            return '#66FF66'
        elif rand <= 0.2 :
            return '#00FF00'
        elif rand <= 0.3 :
            return '#00CC00'
        elif rand <= 0.4 :
            return '#33CC66'
        elif rand <= 0.5 :
            return '#99CC00'
        elif rand <= 0.6 :
            return '#006633'
        elif rand <= 0.7 :
            return '#003300'
        elif rand <= 0.8 :
            return '#99FF00'
        elif rand <= 0.9 :
            return '#99CC00'
        elif rand <= 1.0 :
            return '#339966'
        else : return '#339966'
#-----------------------------------------------------------拍手表示用---------------------------------------------------------
#拍手散布図表示用
    def print_hakusyu(self,df,cutnum, fig, ax,flag='line'):
        df = self.df_time__(df,cutnum,flag)
        i = 0
        flag = False
        #fig, ax = plt.subplots()     
        image_path ='1922466.png'
        colx = df[df.columns[0]]
        plt.tick_params(labelbottom=True,
                labelleft=False,
                labelright=False,
                labeltop=False)
    
       
        for tmp in df['point']:
            x =[]
            y = np.random.rand(tmp)
            if tmp > 0:
                flag = True
            for j in range(tmp):
                x = x + [colx[i]]
            self.imscatter(x, y, os.path.join(sourcedir, 'image', image_path), ax=ax,  zoom=.025) # path.join()
            ax.plot(x, y, 'ko',alpha=0)
        #plt.savefig('cactus_plot.png',dpi=200, transparent=False) 
        #plt.show()
        if  flag == True:
            if len(colx) > 5:
                # 時間のラベルを5個に変更
                plt.xticks(colx[::(-(-len(colx)//5))])

    def imscatter(self,x, y, image, ax=None, zoom=1): 
        if ax is None: 
            ax = plt.gca() 
        try: 
            image = plt.imread(image) 
        except TypeError: 
        # Likely already an array... 
            pass 
        im = OffsetImage(image, zoom=zoom) 
        x, y = np.atleast_1d(x, y) 
        artists = [] 
        for x0, y0 in zip(x, y): 
            ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False) 
            artists.append(ax.add_artist(ab)) 
        ax.update_datalim(np.column_stack([x, y])) 
        ax.autoscale() 
        return artists 
#-----------------------------------------------------------表の作成---------------------------------------------------------
def print_table (self,df,endnum):
    if len(df) == 0:
        return 0
    df = rank_sort(df,False)
    if endnum > len(df[df.columns[0]]):
        endnum = len(df[df.columns[0]])+1
    #fig, ax = plt.subplots(figsize=(2*len(df.columns),endnum))

    ax.axis('off')
    ax.axis('tight')

    tb = ax.table(cellText=df.values[:endnum],
                  colLabels=df.columns[:endnum],
                  bbox=[0, 0, 1, 1],
                  )

    tb[0, 0].set_facecolor('#363636')
    tb[0, 1].set_facecolor('#363636')
    tb[0, 0].set_text_props(color='w')
    tb[0, 1].set_text_props(color='w')
#--------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------折れ線グラフ---------------------------------------------------------

#----------------------折れ線グラフ描画----------------------------------------------
    def print_line_graph(self, df,word,cutnum, fig, ax, flag = 'line'):
        df = self.df_time__(df,cutnum,flag)

        # ラベルとして表示するtimeを格納
        labels = df[df.columns[0]]
        # plot用データ格納
        data =[]

        plt.legend(loc="upper left", fontsize=18)

        if type(word) == str:
            data = plt.plot(labels,df[word])
        else:
            for i in word :
                data = data + plt.plot(labels, df[i])
        
        if len(labels) > 5:
            # 時間のラベルを5個飛ばしに変更
            plt.xticks(labels[::(-(-len(labels)//5))])
        #plt.xticks(df[df.columns[0]][::5]+[df[df.columns[0]][-1]]) # 要検証
        
        ax.legend(data, word, loc='upper right', borderaxespad=1, fontsize=18)

#----------------区切る時間を指定して，グラフ用df作成---------------------------
#h:m:s
#cuttime = (int) hms
    def df_time__(self, df,cuttime,flag = 'line'):
        start = df['time'][0]
        tmp = []
        for i in range(len(df.columns)-1):
            tmp = tmp + [0]

        df_result = pd.DataFrame(index=[], columns = df.columns) 

        for i in range(len(df)):
            j = 0
            for column in df.columns:
                if  column != 'time':
                    tmp[j] += df[column][i]
                    j += 1

            if df['time'][i] > start:
                i -=1
                time = str(int((start%1000000)/10000)) + ':' +str(int((start%10000)/100))+':'+str(start%100)
                tmp.insert(0, time)
                df_2 = pd.DataFrame([tmp],columns=df_result.columns)
                df_result = pd.concat([df_result, df_2], ignore_index=True)
                tmp = tmp[1:]
                
                if flag == 'line' :
                    tmp = []
                    for i in range(len(df.columns)-1):
                        tmp = tmp + [0]
                        
                start += cuttime
                if start % 100 >= 60:
                    start = start - 60 + 100
                if start % 1000 >= 6000:
                    start = start - 6000 + 10000
                if start >= 240000:
                    start = start - 240000 +1000000
        time = str(int((start%1000000)/10000)) + ':' +str(int((start%10000)/100))+':'+str(start%100)
        tmp.insert(0, time)
        df_2 = pd.DataFrame([tmp],columns=df_result.columns)
        df_result = pd.concat([df_result, df_2])

        return df_result
#--------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------main-------------------------------------------------------------------
    def main_graph_test(self, df, fig, ax) :
    #------------データ作成----------------
        #感情推定用df
        df_kanzyou = self.csv_df('kanzyou.csv')
        #東山昌彦、乾健太郎、松本裕治、述語の選択選好性に着目した名詞評価極性の獲得、言語処理学会第14回年次大会論文集、pp.584-587、2008。/東山雅彦、乾健太郎、松本雄二。動詞と形容詞の選択的選好からの名詞の感情の学習、自然言語処理協会の第14回年次会議の議事録、pp.584-587、2008年。
        
        #csvファイルをデータフレームに変換
        #df = csv_df(data)
        #コメントデータからデータ抽出＆データフレーム作成
        df_time_word,df_word_point,df_time_point,df_time_www_point,df_time_hakusyu_point = self.string_word_point(df)
        #人とその人のコメント数のdf作成
        df_contributor_point = self.make_df_contributor_point(df)

        #各時間でのネガティブかポジティブかをdfに
        df_time_negapozi = self.make_df_time_negapozi(df_time_word,df_time_point,df_kanzyou)
        #各時間の単語ごとの出現数のdf作成
        df_time_word_point_stack,df_time_word_point_line = self.time_word_point(df_time_word,df_word_point,df_time_point)
        #各時間の人ごとの出現数のdf作成
        df_time_contributor_point_stack,df_time_contributor_point_line = self.time_contributor_point(df,df_time_point,df_contributor_point)
    #------------------保存変数-----------------------------------
        rank_contributor = self.make_rank_word(2,df_contributor_point,'contributor')
        rank_word  = self.make_rank_word(5,df_word_point,'word')



    #--------------表示-----------------------
        ##折れ線グラフ描画
        #self.print_line_graph(df_time_word_point_line,rank_word,100)
        #self.print_line_graph( df_time_contributor_point_line,rank_contributor,5)
        #self.print_line_graph( df_time_contributor_point_stack,rank_contributor,5,'stack')
        #self.print_line_graph(df_time_negapozi,'negapozi',5)
        #self.print_www( df_time_www_point,100)
        #self.print_hakusyu(df_time_hakusyu_point,100)
    

        #棒グラフ出力用
        #self.print_bar_graph_df(df_word_point,'word')
        #self.print_bar_graph_df(df_contributor_point,'contributor')
        #treemap出力用　
        #return self.print_treemap(df_word_point,'treemap', fig, ax)
        #self.print_treemap(df_word_point,'treemap', fig, ax)
#--------------------------------------------


    def init_graph(self, df, scr_case = False) :

        """
        入力DataFrameを用いてグラフ描画用dfを初期化する
        Parameters
        ----------
        df : DataFrame
            グラフ描画用dfを初期化するDataFrame
        
        fig, ax : 描画したい描画範囲の指定
        """
        print("関数内DF表示")
        print(df)
        self.scr_case = scr_case
    #------------データ作成----------------
        #感情推定用df
        self.df_kanzyou = self.csv_df('kanzyou.csv')
        #東山昌彦、乾健太郎、松本裕治、述語の選択選好性に着目した名詞評価極性の獲得、言語処理学会第14回年次大会論文集、pp.584-587、2008。/東山雅彦、乾健太郎、松本雄二。動詞と形容詞の選択的選好からの名詞の感情の学習、自然言語処理協会の第14回年次会議の議事録、pp.584-587、2008年。

        #コメントデータからデータ抽出＆データフレーム作成
        self.df_time_word,self.df_word_point,self.df_time_point,self.df_time_www_point,self.df_time_hakusyu_point,self.df_URL_point = self.string_word_point(df)
        #人とその人のコメント数のdf作成
        if (scr_case == False):
            self.df_contributor_point = self.make_df_contributor_point(df)

        #各時間でのネガティブかポジティブかをdfに
        self.df_time_negapozi = self.make_df_time_negapozi(self.df_time_word,self.df_time_point,self.df_kanzyou)
        #各時間の単語ごとの出現数のdf作成
        self.df_time_word_point_stack,self.df_time_word_point_line = self.time_word_point(self.df_time_word,self.df_word_point,self.df_time_point)
        if (scr_case == False):
            #各時間の人ごとの出現数のdf作成
            self.df_time_contributor_point_stack,self.df_time_contributor_point_line = self.time_contributor_point(df,self.df_time_point,self.df_contributor_point)
        #------------------保存変数-----------------------------------
            self.rank_contributor = self.make_rank_word(2,self.df_contributor_point,'contributor')
        
        self.rank_word  = self.make_rank_word(5,self.df_word_point,'word')

    def switch_graph(self, fig, ax, graph_name = "treemap") :
    #--------------表示-----------------------
        if (graph_name == "treemap"):
            self.print_treemap(self.df_word_point,'treemap', fig, ax)

        elif (graph_name == "bargraph_word"):
            self.print_bar_graph_df(self.df_word_point,'word', fig, ax)
        elif (graph_name == "table"):
            self.print_table(self.df_URL_point,5, fig, ax)

        elif (graph_name == "bargraph_contributor" and self.scr_case == False):
            self.print_bar_graph_df(self.df_contributor_point,'contributor', fig, ax)

        elif (graph_name == "df_time_word_point_line_100"):
            self.print_line_graph(self.df_time_word_point_line,self.rank_word,100,fig, ax)

        elif (graph_name == "df_time_word_point_line_5" and self.scr_case == False):
            self.print_line_graph(self.df_time_contributor_point_line,self.rank_contributor,5,fig, ax)

        elif (graph_name == "df_time_word_point_stack_5" and self.scr_case == False):
            self.print_line_graph(self.df_time_contributor_point_stack,self.rank_contributor,5, fig, ax, 'stack')

        elif (graph_name == "df_time_negapozi_5"):
            self.print_line_graph(self.df_time_negapozi,'negapozi',5, fig, ax)

        elif (graph_name == "df_time_www_point_100"):
            self.print_www( self.df_time_www_point,100, fig, ax)

        elif (graph_name == "df_time_hakusyu_point_100"):
            self.print_hakusyu(self.df_time_hakusyu_point, 100, fig, ax)

