#-*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

import threading

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label 
from kivy.uix.checkbox import CheckBox

# kivy.unix.popupクラスを使ってPopUpを生成する
from kivy.uix.popup import Popup

# matplotlib組み込み
import numpy as np
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
# Figure#canvas のインスタンスを追加できるように
import matplotlib.pyplot as plt
import sys, os
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from PIL import Image

import pandas as pd

#from Source.commentscraper import Scraper
from Source.data_glaph import DataGraph
from Source.getcomment import GetComment
from Source.commentscraper import Scraper

# Kivy言語のBuilder
from kivy.lang import Builder

Builder.load_file("./Source/test.kv")

dataglp = DataGraph()
getcomment = GetComment()
scr = Scraper()

# デフォルトに使用するフォントを変更する
resource_add_path('./Source/fonts')
LabelBase.register(DEFAULT_FONT, 'ヒラギノ丸ゴ ProN W4.ttc') #日本語が使用できるように日本語フォントを指定する

imagedir = "./Source/image/"
savefiledir = "./Source/csv"
savefilename = "savecsvfile.csv"
savefilepath = os.path.join(savefiledir, savefilename)
loadfilepath = ""

df = pd.DataFrame()

class SubGrids(BoxLayout):
    """チェックボックスとラベルでできたウィジェットを追加"""
    """init時にラベル名を引数として与える"""
    def __init__(self, word, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(CheckBox(size_hint_x=None, width=75))
        self.add_widget(Label(text=word, color=[0.23,0.23,0.23,1]))      


class ConfigPanel(GridLayout):
    def __init__(self, word, **kwargs): 
        super().__init__(**kwargs)
        try:
            word_df = dataglp.get_all_word()
        except:
            print("ファイルが読み込まれていません")
        else:
            print("ファイルが読み込まれました")
            self.clear_widgets()
            GridLayout.__init__(self, cols=1, rows=len(word_df))
            for _, str_word in (dataglp.get_all_word()).iteritems():
                print(str_word)
                self.add_widget(SubGrids(word=str_word))
        pass



class Panels(GridLayout):
    """詳細設定をするためのウィジェット"""
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        lists = ["tagai","hamada"]
    def make_config_panel(self, lists):
        # 呼び出される度にWidgetを初期化する
        self.clear_widgets()
        # リストの数だけパネルのGridLayoutを準備する
        GridLayout.__init__(self, cols=1, rows=len(lists))
        # リストの数だけConfigPanelをWidgetに追加
        for text in lists:
            print(text)
            self.add_widget(ConfigPanel(text))

class GraphView(BoxLayout):
    """Matplotlib のグラフを表示するためのウィジェット"""
    check = BooleanProperty(True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 描画領域を用意する
        self.fig = plt.figure(figsize=(16, 9))
        self.ax = self.fig.add_subplot(111)
        # 描画を初期化する
        self.init_view()
        # グラフをウィジェットとして追加する
        widget = FigureCanvasKivyAgg(self.fig)
        self.add_widget(widget)

    def init_view(self):
        # 以前の内容を消去する
        self.ax.clear()

        # 再描画する
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def load_data(self):
        # テキストファイル読み込み
        global loadfilepath
        global df
        print(os.path.splitext(loadfilepath)[1])
        # テキストファイルからdfの生成
        if (os.path.splitext(loadfilepath)[1] == '.txt'):
            print(".txt 抽出")
            df = getcomment.main(loadfilepath, savefilepath)
        elif (os.path.splitext(loadfilepath)[1] == '.csv'):
            print(".csv 抽出")
            df = dataglp.csv_df(loadfilepath)
        else : # error処理
            print("どちらでもありません")
            return
        print(df)
        dataglp.init_graph(df)
        # 最初のグラフを出力
        self.update_view(df, "func1")
    
    def load_scrapingdata(self):
        print("scraper start!")
        global df
        df = scr.main("カフカ読書会", True)
        # スレッド処理で返り値を受け取るようにしたい・・・
        #t1 = threading.Thread(target=scr.main, args=["カフカ読書会"])
        #t1.start()
        dataglp.init_graph(df)
        print("scraper end!!!")
        print(df)
        self.update_view(df, "func1")

    def update_view(self, df, funcname):
        # 以前の内容を消去する
        self.ax.clear()

        #dataglp.init_graph(df)
        self.plot_graph(funcname)

        # 再描画する
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def checkbox_check(self, checkbox, funcname):
        global df
        print(funcname)
        self.update_view(df,funcname)
        self.check = checkbox.active
        return
    
    def plot_graph(self, funcname):
        """dataglp.switch_graph(fig, ax, グラフタイトル, 呼び出し関数名)"""
        if funcname == "func1":
            # 単語出現数の推移の表示
            print("単語出現数の推移 plot")
            dataglp.switch_graph(self.fig, self.ax, "単語出現数の推移", "df_time_word_point_line_100")
        elif funcname == "func2":
            # ホットワードの表示
            print("ホットワード plot")
            dataglp.switch_graph(self.fig, self.ax, "ホットワード", "treemap")
        elif funcname == "func3":
            # コメントの多い投稿者の表示
            print("コメントの多い投稿者 play")
            dataglp.switch_graph(self.fig, self.ax, "コメントの多い投稿者", "bargraph_contributor")
        elif funcname == "func4":
            # 笑いの推移の表示
            print("笑いの推移 play")
            dataglp.switch_graph(self.fig, self.ax, "笑いの推移", "df_time_www_point_100")
        elif funcname == "func5":
            # 拍手の推移の表示
            print("拍手の推移 play")
            dataglp.switch_graph(self.fig, self.ax, "拍手の推移", "df_time_hakusyu_point_100")
        elif funcname == "func6":
            # 参照URLランキングの表示
            print("func6 play")
            dataglp.switch_graph(self.fig, self.ax, "参照URLランキング", "urltable")
        elif funcname == "func7":
            # 参照URLランキングの表示
            print("func7 play")
            dataglp.switch_graph(self.fig, self.ax, "参照URLランキング", "urltable")



class ShowWidget(Widget):
    """Widget全体を管理するスクリプト"""

    #------ 共通プロパティの宣言 ---------------
    text = StringProperty()
    source  = StringProperty(imagedir + 'lefton.png')
    color = ListProperty([1,1,1,1])
    fileinputimage = StringProperty(imagedir + 'nomalimage.png')
    filepath = StringProperty()
    check1 = BooleanProperty(False)
    check2 = BooleanProperty(False)
    check3 = BooleanProperty(False)

    #------ ShowWidgetの初期化 ---------------
    def __init__(self, **kwargs):
        super(ShowWidget, self).__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)

    #------ ボタンイベント --------------------
    def buttonClickedroom(self):
        # 左のタブがクリックされた時
        # 表示画像の変更
        self.source = imagedir + 'lefton.png'
        print("buttonClickedroom!!!")

    def buttonClickedfile(self):
        # 右のタブがクリックされた時
        # 表示画像の変更
        self.source = imagedir + 'righton.png'
        print("buttonClickedfile!!!")

    def checkbox_check1(self, checkbox):
        # チェックボックス1が押された時
        self.check1 = checkbox.active
        return
    
    def checkbox_check2(self, checkbox):
        # チェックボックス2が押された時
        self.check2 = checkbox.active
        return
    
    def checkbox_check3(self, checkbox):
        # チェックボックス3が押された時
        self.check3 = checkbox.active
        return

    #------ ウィンドウイベント -----------------
    def _on_file_drop(self, window, file_path):
        # ウィンドウにドロップ＆ドラッグされたファイルの名前を取得
        global loadfilepath
        # ファイル名を格納
        loadfilepath = file_path.decode()
        # 表示ファイル名を変更
        self.filepath = os.path.basename(file_path.decode())
    
    #------ 設定パネルの再描画 -----------------
    def conpanel(self):
        # 選択されたグラフの種類で設定パネルの中身を変更する
        graphpanel = self.ids.graph_view
        graphpanel.load_data()

        configpanel = self.ids.conpanel
        configpanel.make_config_panel(["tagai","hamada"])

class CommentShowApp(App):
    """アプリの管理をするスクリプト"""

    def __init__(self, **kwargs):
        super(CommentShowApp, self).__init__(**kwargs)
        self.title = 'コメント見える君'
    
    def build(self):
        return ShowWidget()