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
#-----------------------------------------------------------構文解析&データ作成---------------------------------------------------------

#------------コメントデータからデータ抽出＆データフレーム作成--------------
    def string_word_point(self, df,df_kanzyou):
        jumanpp = Juman(jumanpp=False)
        tmp_word =[]
        df_time_word = pd.DataFrame(index=[], columns=['time','word']) #単語と時間のｄｆ
        df_word_point = pd.DataFrame(index=[], columns=['word','point'])#単語とその出現数のｄｆ
        df_time_point = pd.DataFrame(index=[], columns=['time','point'])#時間とその時のコメント数のｄｆ
        df_time_www_point = pd.DataFrame(index=[], columns=['time','point'])#時間とその時のwww数のｄｆ
        df_time_hakusyu_point = pd.DataFrame(index=[], columns=['time','point'])#時間とその時の拍手数のｄｆ
        df_URL_point = pd.DataFrame(index=[], columns=['URL','point'])#URLまとめdf
        df_time_positive_negative = pd.DataFrame(index=[], columns=['time','positive','negative','neutral','null'])#ネガポジdf

        
        for i in range(len(df)):
            p=0
            n=0
            nil =0
            
            #URLだったら追加
            url=self.URL_hanbetu(df['comment'][i])
            if url != False:
                tmp = self.my_index(df_URL_point['URL'],url)
                df_URL_point = self.make_df_append(df_URL_point,tmp,url)
            
            #記号削除中
            print(df['comment'][i])
            df['comment'][i] = self.my_delete(df['comment'][i])
            #df['contributor'][i] = self.my_delete(df['contributor'][i])
            
            # h:m:s -> hms　に変更
            tmp_time = self.strtime_to_inttime(df['time'][i])
            
            
            #時間ごとのコメント数計算
            tmp = self.my_index(df_time_point['time'],tmp_time)
            df_time_point = self.make_df_append(df_time_point,tmp,tmp_time)

            
            #wwwがあったら1追加なかったら0追加
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
                            
                #ネガポジ判断
                            tmp = self.negapozi_hanbetu(tmp_word,df_kanzyou)
                            if tmp == 'p':
                                p +=1
                            elif tmp == 'n':
                                n +=1
                            elif tmp == 'null':
                                null +=1
                            elif tmp == 'e':
                                e +=1
                index = self.my_index(df_time_positive_negative['time'],tmp_time)
                if False !=index :
                    df_time_positive_negative['positive'][index]+= p
                    df_time_positive_negative['negative'][index]+= n
                    df_time_positive_negative['null'][index]+= null
                    df_time_positive_negative['neutral'][index]+= e
                else :
                    df_time_positive_negative = df_time_positive_negative.append({'time': tmp_time, 'positive': p,'negative': n,'neutral':e,'null':null}, ignore_index=True)

        return df_time_word,df_word_point,df_time_point,df_time_www_point, df_time_hakusyu_point,df_URL_point,df_time_positive_negative
#---------------dfデータ追加プログラム-------------------
    def make_df_append(self,df,index,data):
        if False !=index :
            df[df.columns[1]][index]+=1
            return df
        else :
            return df.append({df.columns[0]: data, df.columns[1]: 1}, ignore_index=True)
#---------------記号削除用プログラム-------------------
    def my_delete(self, string) :
        print(string)
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
#----------------URL判別用プログラム----------------
    def URL_hanbetu(self,string):
        if 'htt' in string:
            tmp = string.index('htt')
            string = string[tmp:]
            if '\n' in string:
                tmp = string.index('\n')
                string = string[:tmp]
            if ' ' in string:
                tmp = string.index(' ')
                string = string[:tmp]   
            parsed_url = urlparse(string)
            url = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(string))
        else : url = False
        return url 
#----------------ネガポジ判断----------------
    def negapozi_hanbetu(self,word,df_kanzyou) :
        tmp = self.my_index(df_kanzyou['word'],word)

        if tmp != False:
            if 'p' in df_kanzyou['negapozi'][tmp]:
                return 'p'
            if 'n' in df_kanzyou['negapozi'][tmp]:
                return 'n'
            if  'e' in df_kanzyou['negapozi'][tmp]:
                    return 'e'
            return 'null'   

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
        df_time_word_point = pd.DataFrame(index=[])
        df_time_word_point['time'] = df_time_point['time']

        word = df_word_point['word']

        for row in word:
            df_time_word_point[row] = 0
            
            #特定の単語の配列番号取得
            tmp_list = [i for i, x in enumerate(df_time_word['word'] == row) if x == True]
            for i in tmp_list:
                tmp = df_time_word_point['time'].values.tolist().index(df_time_word['time'][i])
                df_time_word_point[row][tmp] +=1

        return df_time_word_point

#---------------各時間の人ごとの出現数のdf作成-----------------------------------
    def time_contributor_point(self, df,df_time_point,df_contributor_point) :
        df_time_contributor_point = pd.DataFrame(index=[])
        df_time_contributor_point['time'] = df_time_point['time']


        contributor = df_contributor_point['contributor']


        for row in contributor:
            df_time_contributor_point[row] = 0
            #特定の単語の配列番号取得
            tmp_list = [i for i, x in enumerate(df['contributor'] == row) if x == True]
        
            for i in tmp_list:
                tmp = df_time_contributor_point['time'].values.tolist().index(self.strtime_to_inttime(df['time'][i]))
                df_time_contributor_point[row][tmp] +=1

        return df_time_contributor_point
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
#====================================================-出力用====================================================================
#-----------------------------------------------------------treemap---------------------------------------------------------
#------------------treemap出力用------------------------　
    #引数:データフレームとタイトル
    def print_treemap(self, df, fig, ax) :
        #ソート
        df = self.rank_sort(df,False)
        #最大文字数検索
        max_num = self.max_word_num(df) 

        sns.set()
        matplotlib.rcParams['figure.figsize'] = (16.0, 9.0)
        # ggplot style使用
        style.use('ggplot')
        sns.set(font="IPAexGothic") #日本語フォント設定

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

#-------------------割合作成後dfに追加----------------------
    def add_percent(self, df) :
        s = df['point'].sum()
        df["Population"] = 0.0

        for i in range(len(df['point'])) :
            a = df['point'][i] /float(s) * 100.0
            df["Population"][i] = a

        return df
#--------------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------棒グラフ---------------------------------------------------------
#---------------------棒グラフ出力用--------------------------
    def print_bar_graph_df(self, df, calamu, fig, ax):
        #dfソート
        df = self.rank_sort(df,True)

        plt.barh(df[calamu], df['point'])
        plt.grid(which='major',color='black',linestyle='-',axis = "x")
        
#---------------------積立式棒グラフ出力用--------------------------        
    def print_bar_graph_2(self,df,calamu,fig,ax,labelnum = 5):
        #labelnumの数棒グラフが出るようにcuttime作成
        tmp = (df['time'].iloc[-1]-df['time'].iloc[0])/labelnum
        #区切る時間を指定して，グラフ用df作成
        df = self.df_time__(df,int(tmp))
        #出力
        ax.bar(df['time'], df[calamu[0]])
        sum = df[calamu[0]]
        for i in range(len(calamu)-1):
            ax.bar(df['time'], df[calamu[i+1]], bottom=sum)
            sum += df[calamu[i+1]]
#---------------------棒グラフ出力用(in率)--------------------------
    def print_barh_graph_df(self,df,calamu,fig,ax,labelnum = 5):
        colors = ["#ed7d31",'#c0c0c0']
        df = self.df_time__barh(df,500)
        for i in range(len(df['time'])):
            ax.barh(calamu, df[calamu].iloc[i], left=df[calamu].iloc[:i].sum() ,color =colors[i%2] )
        self.make_label(df,labelnum,df[calamu[0]].iloc[:i].sum(),ax)
#---------------------横軸を時間にして出力--------------------------
    def make_label(self,df,labelnum,max,ax):
        colx = df['time']
        if len(colx) > labelnum:
            tmp = labelnum
        else :
            tmp = len(colx)
        label = []
        label_string = []
        for i in range(tmp):
            label += [max / tmp * i]
            label_string += [colx[int(len(colx)/tmp*i)]]
        label += [max]
        label_string +=[colx.iloc[-1]]
        ax.set_xticks(label)
        ax.set_xticklabels(label_string)
#---------------------入退室予想専用df作成--------------------------
    def df_time__barh(self,df,cuttime):
        start = df['time'][0]
        tmp = []
        tmp_index = []
    
        for j in range(len(df.columns)-1):
            tmp = tmp + [0]
            tmp_index = tmp_index + [0]
            
        i=0
        df_result = pd.DataFrame(index=[], columns = df.columns) 
        while True:
            if df['time'][i] < start :
                j = 0
                for column in df.columns[1:]:
                    if df[column][i] > 0:
                        tmp[j] = 1
                    j += 1
                i += 1
                if i > len(df['time'])-1:break

            else:
                time = str(int((start%1000000)/10000)) + ':' +str(int((start%10000)/100))+':'+str(start%100)
                tmp_data = [time]
                for column in df.columns[1:]:
                    tmp_data += [0]
                df_2 = pd.DataFrame([tmp_data],columns=df_result.columns)
                df_result = pd.concat([df_result, df_2], ignore_index=True)

                j = 0
                for column in df.columns[1:]:
                    df_result[column][tmp_index[j]] += 1
                    if tmp[j] == 0 and tmp_index[j]  % 2 == 0 :
                        tmp_index[j] += 1
                    elif tmp[j] == 1 and tmp_index[j] % 2 == 1:
                        tmp_index[j] += 1
                    tmp[j] = 0
                    j+= 1

                start += cuttime
                if start % 100 >= 60:
                    start = start - 60 + 100
                if start % 1000 >= 6000:
                    start = start - 6000 + 10000
                if start >= 240000:
                    start = start - 240000 +1000000 
            if df['time'].iloc[-1] < start: break              

        return df_result
#--------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------散布図---------------------------------------------------------
#----------------------------------wwwwww描画用-------------------------------------------
    def print_www(self,df,cutnum, fig, ax, flag='line',labelnum = 5):
        #区切る時間を指定して，グラフ用df作成
        df = self.df_time__(df,cutnum,flag)
        colors = ["#66FF66",'#00FF00','#00CC00', '#33CC66', '#99CC00','#006633','#003300', '#99FF00','#99CC00','#339966']
        i = 0
        #x軸のみ出力
        plt.tick_params(labelbottom=True,
            labelleft=False,
            labelright=False,
            labeltop=False)
        flag = False
        colx = df[df.columns[0]]
        if df['point'].sum() == 0:
            ax.axis('off')
            image_path ='nodata.png'
            image = plt.imread(os.path.join(sourcedir, "image", image_path)) 
            plt.imshow(image)
            return False 
        
        for tmp in df['point']:
            x =[]
            y = np.random.rand(tmp)
            color_tmp = int(np.random.rand(1)*10)
            for j in range(tmp):
                x = x + [colx[i]]
            #wの色決め
            plt.scatter(x,y, c=colors[color_tmp],s=1800, marker="$w$",alpha=0.8)
            i+=1
                
        if len(colx) > labelnum:
        # 時間のラベルを5個に変更
            plt.xticks(colx[0::(-(-len(colx)//labelnum))])

#----------------------拍手散布図表示用----------------------
    def print_hakusyu(self,df,cutnum, fig, ax,flag='line',labelnum = 5):
        #区切る時間を指定して，グラフ用df作成
        df = self.df_time__(df,cutnum,flag)
        image_path =['redhandclap.png','yellowhandclap.png','bluehandclap.png']
        i = 0
        flag = False    
        colx = df[df.columns[0]]
        #x軸のみ出力
        plt.tick_params(labelbottom=False,
                labelleft=False,
                labelright=False,
                labeltop=False)
        
        if df['point'].sum() == 0:
            ax.axis('off')
            image_path ='nodata.png'
            image = plt.imread(os.path.join(sourcedir, "image", image_path)) 
            plt.imshow(image)
            return False 
   
        for tmp in df['point']:
            x = (np.random.rand(tmp) / len(df[df.columns[0]])) + (1 / len(df[df.columns[0]]) * i )
            y = np.random.rand(tmp)
            index = int(np.random.rand(1) *10) %3
            self.imscatter(x, y, os.path.join(sourcedir, 'image', image_path[index]), ax=ax,  zoom=.025) 
            ax.plot(x, y, 'ko',alpha=0)

#----------------------拍手画像表示----------------------
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

#--------------------------------------------------------------------------------------------------------------------------------------

#----------------------表の作成----------------------
    def print_table (self,df,endnum,columnnames,fig,ax):
        if len(df) == 0:
            ax.axis('off')
            image_path ='nodata.png'
            image = plt.imread(os.path.join(sourcedir, "image", image_path))
            image = np.asarray( image)
            plt.imshow(image)
            return False
        df = self.rank_sort(df,False)
        if endnum > len(df[df.columns[0]]):
            endnum = len(df[df.columns[0]])+1
        #fig, ax = plt.subplots(figsize=(2*len(df.columns),endnum))

        ax.axis('off')
        ax.axis('tight')

        tb = ax.table(cellText=df.values[:endnum],
                    colWidths=[1,0.5],
                    colLabels=columnnames,
                    bbox=[0, 1-1/endnum*endnum, 1, 1/endnum*endnum]
                    )

        tb[0, 0].set_facecolor('#363636')
        tb[0, 1].set_facecolor('#363636')
        tb[0, 0].set_text_props(color='w')
        tb[0, 1].set_text_props(color='w')
        return True
#----------------------円グラフ----------------------
    def print_pie_graph(self,df,word,fig,ax,flag2 = ''):
        label = []
        data =[]
        pie_colors = ["#ed7d31", "#3498db", "g", "m", "y"]
        for i in word :
            if flag2 == 'negapozi':
                data = data + [df[i].sum()]
                label += [i]
            else :
                index = my_index(df[df.columns[0]],i)
                if index != False:
                    data = data + [df['point'][index]]
                    label += [i]
        plt.pie(data, labels=label,autopct="%1.1f%%",counterclock=True,colors=pie_colors,startangle=90)
#----------------------折れ線グラフ描画----------------------------------------------
    def print_line_graph(self, df,word,cutnum, fig, ax, flag = 'line',flag2 = '',label = False,labelnum = 5):
        #区切る時間を指定して，グラフ用df作成
        df = self.df_time__(df,cutnum,flag)
        j=0
        #カラーパレット指定
        if flag2 != 'negapozi':
            current_palette = {'positive':"#ed7d31", 'negative':"#3498db", 'neutral':"#65ab31",'null': "#c0c0c0"}
        else : current_palette = sns.color_palette(n_colors=24)
        
        if label == False:
            label = word
        
        # ラベルとして表示するtimeを格納
        labels = df[df.columns[0]]
        # plot用データ格納
        data =[]

        if type(word) == str:
            if flag2 != True:
                data = plt.plot(labels,df[word],marker="o")
            else :data = plt.plot(left,df[word],marker="o",color=current_palette[j],linewidth = 3.0)
            label = [label]
        else:
            for i in word :
                if flag2 != 'negapozi':
                    data = data + plt.plot(left, df[i],marker="o",color=current_palette[i],linewidth = 3.0)
           
                else :data = data + plt.plot(labels, df[i],marker="o",color=current_palette[j],linewidth = 3.0)
                j+=1
        
        if len(labels) > labelnum:
            # 時間のラベルをlabelnum個飛ばしに変更
            plt.xticks(labels[::(-(-len(labels)//labelnum))])
        
        ax.legend(data, label, loc='upper right', borderaxespad=1, fontsize=18)

#----------------区切る時間を指定して，グラフ用df作成---------------------------
#h:m:s
#cuttime = (int) hms
    def df_time__(self, df,cuttime,flag = 'line'):
        start = df['time'][0]
        tmp = []
        for i in range(len(df.columns)-1):
            tmp = tmp + [0]
        i=0
        df_result = pd.DataFrame(index=[], columns = df.columns) 
        while df['time'].iloc[-1] >= start:
            j = 0
            if df['time'][i] < start :
                for column in df.columns[1:]:
                    tmp[j] += df[column][i]
                    j += 1
                i += 1
                if i > len(df['time'])-1:break

            else:
                time = str(int((start%1000000)/10000)) + ':' +str(int((start%10000)/100))+':'+str(start%100)
                tmp.insert(0, time)
                df_2 = pd.DataFrame([tmp],columns=df_result.columns)
                df_result = pd.concat([df_result, df_2], ignore_index=True)
                tmp = tmp[1:]

                if flag == 'line' :
                    tmp = []
                    for j in range(len(df.columns)-1):
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
        #tmp = pd.Series(tmp, index=df_result.columns)
        df_result = pd.concat([df_result, df_2])

        return df_result
#-----------------グラフ表示-----------------------------------
    def setting_graph(self, fig, ax, title, flag = True):
        """ debug用 """
        if flag == True:
            # タイトルの設定（名前、位置）
            plt.title(title, fontsize=18,fontweight="bold")
            ttl = ax.title
            ttl.set_position([.5, 1.05])
    
#--------------------------------------------------------------
#-----------------グラフ初期化-----------------------------------

    def first_graph(self, fig):
        #fig = plt.figure(figsize=(16, 9))
        #ax.axis('off')
        ax = fig.add_subplot(111)
        ax.axis('on')
        # 背景色
        fig.set_facecolor('#ffffff')
        plt.tick_params(labelbottom=True,
            labelleft=True,
            labelright=False,
            labeltop=False)
        print("初期化したよ")
        return fig,ax
    
#--------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#===========================================================================================================================================
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
 #グラフを画像にして保存
    def save_graph_to_png(self,path,fig):
        fig.savefig(path)

#データがないときに画像を出力
    def print_noddata():
        ax.axis('off')
        image_path ='nodata2.png'
        image = plt.imread(os.path.join(sourcedir, "image", image_path))
        image = np.asarray( image)
        plt.imshow(image)

#-------------------------------------main-------------------------------------------------------------------
    def init_graph(self, df, scr_case = False):

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
        #fig,ax = self.first_graph()
    #------------データ作成----------------
        #感情推定用df
        self.df_kanzyou = self.csv_df('kanzyou.csv')
        #東山昌彦、乾健太郎、松本裕治、述語の選択選好性に着目した名詞評価極性の獲得、言語処理学会第14回年次大会論文集、pp.584-587、2008。/東山雅彦、乾健太郎、松本雄二。動詞と形容詞の選択的選好からの名詞の感情の学習、自然言語処理協会の第14回年次会議の議事録、pp.584-587、2008年。

        #コメントデータからデータ抽出＆データフレーム作成
        self.df_time_word,self.df_word_point,self.df_time_point,self.df_time_www_point,self.df_time_hakusyu_point,self.df_URL_point,self.df_time_positive_negative = self.string_word_point(df,self.df_kanzyou)
        #人とその人のコメント数のdf作成
        if (scr_case == False):
            self.df_contributor_point = self.make_df_contributor_point(df)

        #各時間の単語ごとの出現数のdf作成
        self.df_time_word_point = self.time_word_point(self.df_time_word,self.df_word_point,self.df_time_point)
        if (scr_case == False):
            #各時間の人ごとの出現数のdf作成
            self.df_time_contributor_point= self.time_contributor_point(df,self.df_time_point,self.df_contributor_point)
        #------------------保存変数-----------------------------------
            self.rank_contributor = self.make_rank_word(2,self.df_contributor_point,'contributor')
        
        self.rank_word  = self.make_rank_word(5,self.df_word_point,'word')

    def switch_graph(self, fig, title, graph_name = "treemap") :
        flag = True
    #--------------表示-----------------------
        fig, ax = self.first_graph(fig)

        #labelnum   : x軸に表示するメモリの数-1                                                        default : 5
        #flag       : 'stack','line' 線グラフの時に使い分けてね(print_line_graph)                       default : 'line'
        #flag2      : negapozi判断をするときは'negapozi'をつけてね(print_line_graph,print_pie_graph)    default : ''
        #label      : ラベルを別の名前にしたいときは入力してね(print_line_graph)                         default : False
        
        if (graph_name == "treemap"):
            self.print_treemap(self.df_word_point, fig, ax)
        if(graph_name == "df_timepoint_line_100"):
            self.print_line_graph(self.df_time_point,'point',100,fig,ax,label='コメント数')
        elif (graph_name == "bargraph_word"):
            self.print_bar_graph_df(self.df_word_point,'word', fig, ax)
          
        elif (graph_name == "bargraph_contributor" and self.scr_case == False):
            self.print_bar_graph_df(self.df_contributor_point,'contributor', fig, ax)
            
        elif (graph_name == "bargraph_negapozi" and self.scr_case == False):
            self.print_bar_graph_2(self.df_time_positive_negative,['positive','negative'], fig, ax)
        
        elif (graph_name == "bargraph_nyuutaisitu" and self.scr_case == False):
            #人数を減らしたかったら df_human_point['contributor'] -> self.rank_contributor
            self.print_barh_graph_df(self.df_time_human_point,self.df_human_point['contributor'],fig,ax)
        
        elif (graph_name == "bargraph_nyuutaisitu" and self.scr_case == False):
            self.print_bar_graph_2( self.df_time_positive_negative,['positive','negative'],fig,ax)
            
        elif (graph_name == "urltable"):
            flag = self.print_table(self.df_URL_point,5,['URL','コメント数'], fig, ax)

        elif (graph_name == "wordtable"):
            flag = self.print_table(self.df_word_point,5,['単語','コメント数'], fig, ax)
            
        elif (graph_name == "df_time_word_point_line_100"):
            self.print_line_graph(self.df_time_word_point,self.rank_word,100,fig, ax)

        elif (graph_name == "df_time_word_point_line_5" and self.scr_case == False):
            self.print_line_graph(self.df_time_contributor_point,self.rank_contributor,5,fig, ax)

        elif (graph_name == "df_time_word_point_stack_5" and self.scr_case == False):
            self.print_line_graph(self.df_time_contributor_point,self.rank_contributor,5, fig, ax, 'stack')

        elif (graph_name == "df_time_negapozi_100"):
            self.print_line_graph(self.df_time_negapozi,['neutral','negative','positive'],100, fig, ax)

        elif (graph_name == "df_time_www_point_100"):
            flag = self.print_www( self.df_time_www_point,100, fig, ax)

        elif (graph_name == "df_time_hakusyu_point_100"):
            flag = self.print_hakusyu(self.df_time_hakusyu_point, 100, fig, ax)
        
        elif (graph_name == "piegraph_negapozi"):
            flag = self.print_pie_graph(self.df_time_positive_negative, ['positive','negative','neutral','null'], fig, ax)
        
        self.setting_graph(fig, ax, title, flag)
        print(fig)
        print(ax)
