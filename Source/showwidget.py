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

# Clockで描画を更新
from kivy.clock import Clock

import pandas as pd

#from Source.commentscraper import Scraper
from Source.data_glaph import DataGraph
from Source.getcomment import GetComment
from Source.commentscraper import Scraper

# Kivy言語のBuilder
from kivy.lang import Builder

Builder.load_file("./Source/test.kv")

#scr = Scraper()
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
#check = BooleanProperty(True)
class GraphView(BoxLayout):
    """Matplotlib のグラフを表示するためのウィジェット"""
    check = BooleanProperty(True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.state = True
        # 描画領域を用意する
        self.fig, self.ax = plt.subplots()
        # 描画を初期化する
        self.init_view()

        # グラフをウィジェットとして追加する
        widget = FigureCanvasKivyAgg(self.fig)
        self.add_widget(widget)

    def init_view(self):
        # 以前の内容を消去する
        self.ax.clear()
        #self.state = True
        #画像の読み込み
        #im = Image.open(os.path.join(imagedir, "QRcode.png"))

        #画像をarrayに変換
        #im_list = np.array(im)
        #self.ax.plot(x, y, label="test")
        #self.ax.set_title("test", color='red')
        # データを描画する
        #self.ax.imshow(im_list, im_list.shape[0], im_list.shape[1], im_list.shape[2])
        #img = plt.imread(os.path.join(imagedir, "QRcode.png"))
        #self.plt.imshow(img) # 画像の描画
        #self.get_center_yplt.show() # 描画結果の表示

        self.ax.axis('off')

        # 再描画する
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


        # 再描画する
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def load_data(self):
        # テキストファイル読み込み
        global loadfilepath
        global df
        # テキストファイルからdfの生成
        df = getcomment.main(loadfilepath, savefilepath)
        print(df)
        self.update_view(df, "func1")
    
    def load_scrapingdata(self):
        print("scraper start!")
        global df
        df = scr.main("カフカ読書会", True)
        # スレッド処理で返り値を受け取るようにしたい・・・
        #t1 = threading.Thread(target=scr.main, args=["カフカ読書会"])
        #t1.start()
        print("scraper end!!!")
        print(df)
        self.update_view(df, "func1")

    def update_view(self, df, funcname):
        # 以前の内容を消去する
        self.ax.clear()

        dataglp.init_graph(df)
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
        print(funcname)
        if funcname == "func1":
            print("func1 play")
            dataglp.switch_graph(self.fig, self.ax, "df_time_word_point_line_100")
        elif funcname == "func2":
            print("func2 play")
            dataglp.switch_graph(self.fig, self.ax, "treemap")
        elif funcname == "func3":
            print("func3 play")
            dataglp.switch_graph(self.fig, self.ax, "bargraph_contributor")


#glp = GraphView()

class ShowWidget(Widget):
    
    text = StringProperty()    # プロパティの追加
    source  = StringProperty(imagedir + 'lefton.png')
    color = ListProperty([1,1,1,1])
    fileinputimage = StringProperty(imagedir + 'nomalimage.png')
    filepath = StringProperty()
    check1 = BooleanProperty(False)
    check2 = BooleanProperty(False)
    check3 = BooleanProperty(False)
    #df = pd.DataFrame()
    def __init__(self, **kwargs):
        super(ShowWidget, self).__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)
        self.text = 'How are you?'
        print("pressed")
        self.color = [1, 1, 1 , 1]

    def buttonClicked1(self):        # ボタンをクリック時
        self.text = 'I am fine!'
        print("pressed")
        #df = getcomment.main(self.filepath, savefilepath)
        print("buttonclickedfunc")
        print(df)
        #glp.update_view(df)
        self.color = [1, 0, 1 , 1]
    
    def buttonClicked2(self):        # ボタンをクリック時
        self.text = 'I am soso!'
        print("pressed")
        self.color = [1, 1, 0 , 1]
        #glp.test_sin_show()
    
    def buttonClicked3(self):        # ボタンをクリック時
        self.text = 'I am happy!'
        print("pressed")
        self.color = [0, 1, 1 , 1]

    def buttonClickedroom(self):        # ボタンをクリック時
        #self.text = 'room名より取得'
        self.source = imagedir + 'lefton.png'
        self.color = [0, 1, 1 , 1]
        print("buttonClickedroom!!!")

    def buttonClickedfile(self):        # ボタンをクリック時
        #self.text = 'ファイルから取得'
        self.source = imagedir + 'righton.png'
        self.color = [0, 1, 1 , 1]
        print("buttonClickedfile!!!")

    def checkbox_check1(self, checkbox):
        self.check1 = checkbox.active
        return
    
    def checkbox_check2(self, checkbox):
        self.check2 = checkbox.active
        return
    
    def checkbox_check3(self, checkbox):
        self.check3 = checkbox.active
        return

    def plottest(self):
        glp.main()

    # Windowにドロップされた際発生するイベント
    # ファイル名を取得する
    def _on_file_drop(self, window, file_path):
        global loadfilepath
        loadfilepath = file_path.decode()
        self.filepath = os.path.basename(file_path.decode())
        self.fileinputimage = imagedir + 'inputimage.png'

class CommentShowApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'コメント見える君'
    
    def build(self):
        return ShowWidget()