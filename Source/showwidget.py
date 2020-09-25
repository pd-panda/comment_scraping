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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label 
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image as ImageKivy
from kivy.uix.button import Button

from kivy.graphics import Color, Rectangle

# kivy.unix.popupクラスを使ってPopUpを生成する
from kivy.uix.popup import Popup

from functools import partial

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
imgdir = "./Source/image"
savefiledir = "./Source/csv"
savefilename = "savecsvfile.csv"
savefilepath = os.path.join(savefiledir, savefilename)
loadfilepath = ""

df = pd.DataFrame()

lists_id = []

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
            self.add_widget(Label(text=word, color=[0.23,0.23,0.23,1]))
            for _, str_word in (dataglp.get_all_word()).iteritems():
                print(str_word)
                self.add_widget(SubGrids(word=str_word))
        pass



class Panels(GridLayout):
    """詳細設定をするためのウィジェット"""
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        lists = ["表示単語"]
    def make_config_panel(self, lists):
        # 呼び出される度にWidgetを初期化する
        self.clear_widgets()
        # リストの数だけパネルのGridLayoutを準備する
        GridLayout.__init__(self, cols=1, rows=len(lists))
        # リストの数だけConfigPanelをWidgetに追加
        for text in lists:
            print(text)
            self.add_widget(Label(text=text))
            #self.add_widget(ConfigPanel(text))
    def make_pozinega_config_panel(self, lists):
        global lists_id
        lists_id = {}
        # 呼び出される度にWidgetを初期化する
        self.clear_widgets()
        self.padding= [10, 50]
        gridpanel = GridLayout(cols=1, rows=6, size_hint_y=None, height= self.minimum_height)
        label = Label(text="表示グラフ", font_size= 34, color=[0.23,0.23,0.23,1])
        label.size = label.texture_size
        gridpanel.add_widget(label)
        lineimage = ImageKivy(source= os.path.join(imgdir,'line.png'), keep_ratio= True, size_hint_y=None, height= 45)
        # タイトル下の棒を描く
        gridpanel.add_widget(lineimage)
        for index, text in enumerate(lists):
            checkpanel = BoxLayout(orientation='horizontal', size_hint_y=None, height= 45)
            checkbox = CheckBox(size_hint_x=None,size_hint_y=None, width=75, height=35, active= True)
            lists_id["configpanel" + str(index)] = checkbox
            checkpanel.add_widget(checkbox)
            label = Label(text=text, font_size= 26, color=[0.23,0.23,0.23,1], size_hint_y=None, height=35)
            checkpanel.add_widget(label)
            gridpanel.add_widget(checkpanel)
        with self.canvas.before:
            self.rect = Rectangle(source=os.path.join(imgdir,'commentpanel.png'), size=self.size, pos=self.pos)
        self.add_widget(gridpanel)

    def make_config_panel_list(self, funcname):
        # 生成したいチェックボックスを作る
        if funcname == "func7":
            lists = ["ポジティブ", "ネガティブ", "ニュートラル", "NULL"]
        if funcname == "":
            lists = []
        else:
            lists = []
        self.make_pozinega_config_panel(lists)


class GraphView(BoxLayout):
    """Matplotlib のグラフを表示するためのウィジェット"""
    check = BooleanProperty(True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 描画領域を用意する
        self.fig = plt.figure(figsize=(16, 9))
        self.ax = self.fig.add_subplot(111)
        # 描画を初期化する
        #self.init_view()
        # グラフをウィジェットとして追加する
        #widget = FigureCanvasKivyAgg(self.fig)
        #self.add_widget(widget)
        widget = FigureCanvasKivyAgg(self.fig)
        self.add_widget(widget)

    def init_view(self):
        self.fig = plt.figure(figsize=(16, 9))
        self.ax = self.fig.add_subplot(111)

        # 以前の内容を消去する
        self.ax.clear()
        plt.figure()

        widget = FigureCanvasKivyAgg(self.fig)
        self.add_widget(widget)

        # 再描画する
        #self.fig.canvas.draw()
        #self.fig.canvas.flush_events()

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
        #dataglp.init_graph(df)
        # 最初のグラフを出力
        self.update_view(df, "func1")
    
    def load_scrapingdata(self):
        print("scraper start!")
        global df
        df = scr.main("カフカ読書会", True)
        # スレッド処理で返り値を受け取るようにしたい・・・
        #t1 = threading.Thread(target=scr.main, args=["カフカ読書会"])
        #t1.start()
        #dataglp.init_graph(df)
        print("scraper end!!!")
        print(df)
        self.update_view(df, "func1")

    def update_view(self, df, funcname):

        #self.fig = plt.figure(figsize=(16, 9))
        #self.ax = self.fig.add_subplot(111)

        # 以前の内容を消去する
        self.ax.clear()
        #plt.figure()

        dataglp.init_graph(df)
        self.plot_graph(funcname)

        #widget = FigureCanvasKivyAgg(self.fig)
        #self.add_widget(widget)

        # 以前の内容を消去する
        #self.ax.clear()

        #dataglp.init_graph(df)
        #self.plot_graph(funcname)

        # 再描画する
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def checkbox_check(self, checkbox, funcname):
        global df
        print(funcname)
        self.update_view(df,funcname)
        self.check = checkbox.active
        return
    
    def checkbox_check_test(self, funcname):
        global df
        print(funcname)
        self.update_view(df,funcname)
        return
    
    def save_graph(self, savepath):
        dataglp.save_graph_to_png(savepath,self.fig)
        print("グラフを保存しました!!")
    
    def plot_graph(self, funcname, lists= []):
        """dataglp.switch_graph(fig, ax, グラフタイトル, 呼び出し関数名)"""
        #self.fig.delaxes(self.ax)
        if funcname == "func1":
            # 全コメント数推移
            dataglp.switch_graph(self.fig, "単語出現数の推移", "df_timepoint_line_1000")
            # 単語出現数の推移の表示
            #print("単語出現数の推移 plot")
            #dataglp.switch_graph(self.fig, "単語出現数の推移", "df_time_word_point_line_100")
        elif funcname == "func2":
            # ホットワードの表示
            print("ホットワード plot")
            dataglp.switch_graph(self.fig, "ホットワード", "treemap")
        elif funcname == "func3":
            # コメントの多い投稿者の表示
            print("コメントの多い投稿者 play")
            dataglp.switch_graph(self.fig, "コメントの多い投稿者", "bargraph_contributor")
        elif funcname == "func4":
            # 笑いの推移の表示
            print("笑いの推移 play")
            dataglp.switch_graph(self.fig, "笑いの推移", "df_time_www_point_100")
        elif funcname == "func5":
            # 拍手の推移の表示
            print("拍手の推移 play")
            dataglp.switch_graph(self.fig, "拍手の推移", "df_time_hakusyu_point_100")
        elif funcname == "func6":
            # 参照URLランキングの表示
            print("func6 play")
            dataglp.switch_graph(self.fig, "参照URLランキング", "urltable")
        elif funcname == "func7":
            # ポジネガ単語数推移グラフの表示
            print("func7 play")
            dataglp.switch_graph(self.fig, "ポジネガ単語数推移グラフ", "df_time_negapozi_100", plot_lists=['positive','negative','neutral','null'])
        elif funcname == "func8":
            # ポジネガ単語棒グラフの表示
            print("func8 play")
            dataglp.switch_graph(self.fig, "ポジネガ単語棒グラフ", "piegraph_negapozi")
        elif funcname == "func9":
            # 入退室棒グラフの表示
            print("func9 play")
            dataglp.switch_graph(self.fig, "入退室棒グラフ", "bargraph_nyuutaisitu")
        elif funcname == "func10":
            # 参照URLランキングの表示
            print("func10 play")
            dataglp.switch_graph(self.fig, "入退室棒グラフ2", "bargraph_nyuutaisitu2")
        elif funcname == "func11":
            # 参照URLランキングの表示
            print("func11 play")
            dataglp.switch_graph(self.fig, "ポジティブ・ネガティブな単語の割合", "piegraph_negapozi")

class PopupChooseFile(BoxLayout):
 
    # 現在のカレントディレクトリ。FileChooserIconViewのpathに渡す
    current_dir = os.path.dirname(os.path.abspath(__file__))
 
    # MusicPlayerクラス内で参照するための設定
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadDialog(FloatLayout):
    """ファイルをロードするダイアグラム"""
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    """ファイルをセーブするダイアグラム"""
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


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
    check_radio = BooleanProperty(True)

    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        print(path)
        print(filename)
        savedir = os.path.dirname(path)
        if os.path.splitext(filename)[1] == ".png":
            savepath = os.path.join(savedir, filename)
        else :
            savepath = os.path.join(savedir, filename+".png")
        print(savepath)
        graphpanel = self.ids.graph_view
        graphpanel.save_graph(savepath)

        self.dismiss_popup()

    #def save_graph(self):
    #    """graphの保存"""
    #    #filechooser = Root()
    #    #filechooser.show_save()
    #    content = PopupChooseFile(select=self.select, cancel=self.cancel)
    #    self.popup = Popup(title="Select MP3", content=content)
    #    self.popup.open()

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
    
    def checkbox_check(self, checkbox, funcname):
        global lists_id
        self.check_radio = checkbox.active
        graphpanel = self.ids.graph_view
        graphpanel.checkbox_check_test(funcname)
        configpanel = self.ids.conpanel
        configpanel.make_config_panel_list(funcname)
        # 表示グラフ指定チェックボックスが変化した時
        if len(lists_id) != 0:
            for index, item in lists_id.items():
                print(item.active)


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