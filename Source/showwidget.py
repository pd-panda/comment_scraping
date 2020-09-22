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

class SubGrids(BoxLayout):
    """チェックボックスとラベルでできたウィジェットを追加"""
    """init時にラベル名を引数として与える"""
    def __init__(self, word, **kwargs):
        super().__init__(**kwargs)
        #GridLayout.__init__(self, cols=2, raws=1)
        self.add_widget(CheckBox(size_hint_x=None, width=75))
        self.add_widget(Label(text=word, color=[0.23,0.23,0.23,1]))
        

class ConfigPanel(GridLayout):
    def __init__(self, word, **kwargs): 
        super().__init__(**kwargs)
        # test用　データがなくても表示されるよ
        #GridLayout.__init__(self, cols=1, rows=3)
        #self.add_widget(Label(text=word, color=[0.23,0.23,0.23,1]))
        #self.add_widget(Label(text=word, color=[0.23,0.23,0.23,1]))
        #self.add_widget(Label(text=word, color=[0.23,0.23,0.23,1]))
        
    # Widget追加時にword抽出をする
    #def make_words_list(self, word):
        try:
            word_df = dataglp.get_all_word()
        except:
            print("ファイルが読み込まれていません")
        else:
            print("ファイルが読み込まれました")
            #self.add_widget(Label(text=word, color=[0.23,0.23,0.23,1]))
            #self.add_widget(SubGrids(word="aaa"))
            self.clear_widgets()
            GridLayout.__init__(self, cols=1, rows=len(word_df))
            #self.add_widget(Label(text="単語一覧", color=[0.23,0.23,0.23,1]))
            #self.add_widget(Label(text=word, color=[0.23,0.23,0.23,1]))
            #GridLayout.__init__(self, cols=2, rows=-(-len(word_df)//2))
            for _, str_word in (dataglp.get_all_word()).iteritems():
                print(str_word)
                self.add_widget(SubGrids(word=str_word))
            
        pass


class Panels(GridLayout):
    """詳細設定をするためのウィジェット"""
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        lists = ["tagai","hamada"]
        GridLayout.__init__(self, cols=1, rows=3)
        #GridLayout.__init__(self, cols=1, rows=len(lists))
        # 縦に分割してラベルを表示できるようにはなった
        #self.add_widget(Label(text= lists[0]))
        #self.add_widget(Label(text= lists[0]))
        #self.add_widget(Label(text= lists[1]))
        """
        # 縦に（チェックボックス , ラベル）の塊を表示したい
        self.add_widget(ConfigPanel("aaa"))
        self.add_widget(ConfigPanel("bbb"))
        self.add_widget(ConfigPanel("ccc"))
        """
        #self.add_widget(ConfigPanel("ddd"))
        
    def make_config_panel(self, lists):
        #self.clear_widgets()
        print(len(lists))
        #GridLayout.__init__(self, cols=1, rows=len(lists))
        #self.add_widget(ConfigPanel("aaa"))
        #self.add_widget(ConfigPanel("bbb"))
        for text in lists:
            print(text)
            self.add_widget(ConfigPanel(text))

        """
        , 
                            orientation = 'vertical',
                            size_hint_y = None,
                            pos_hint    = {"x":0, "top":1},
                            height      = self.parent.height,
                            size_hint_x = 0.5,
                            padding     = [10, 30],
                            spacing     = [20, 50],
        """
        #with self.canvas:
            #Color(0, 1, 1, 1)
        #    self.rect = Rectangle(source="./Source/image/commentpanel.png", size=self.size, pos=self.pos)
            #self.rect = Rectangle(source="back.jpg", size=root.size, pos=root.pos)
        #self.add_widget()
        """
        canvas.before: 
            Rectangle: 
                pos: self.pos 
                size: self.size 
                source: './Source/image/commentpanel.png'
                Label:
        text: "コメント数"
            color: [0.23,0.23,0.23,1]
            font_size: 32
            halign: 'center'
            valign: 'middle'
            height: 30
            size_hint_y: None
            #size_hint_y: 0.1
        Image:
            #size: self.size
            height: 20
            size_hint_y: None
            #size_hint_y: 0.1
            keep_ratio: True
            source: './Source/image/line.png'
        """
        #confpanel = self.ids.conpanel
        #confpanel = ConfigPanel()
        #self.add_widget(confpanel.make_words_list("aaa"))
        #for text in lists:
        #    print(text)
        #    self.add_widget(confpanel.make_words_list(text))

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
        print(funcname)
        if funcname == "func1":
            print("func1 play")
            dataglp.switch_graph(self.fig, self.ax, "単語出現数の推移", "df_time_word_point_line_100")
            #configpanel = self.ids.conpanel
            #print(configpanel)
            #configpanel = ConfigPanel()
            #configpanel.make_words_list()
            #ConfigPanel.make_words_list()
        elif funcname == "func2":
            print("func2 play")
            dataglp.switch_graph(self.fig, self.ax, "ホットワード", "treemap")
        elif funcname == "func3":
            print("func3 play")
            dataglp.switch_graph(self.fig, self.ax, "コメントの多い投稿者", "bargraph_contributor")
        elif funcname == "func4":
            print("func4 play")
            dataglp.switch_graph(self.fig, self.ax, "笑いの推移", "df_time_www_point_100")
        elif funcname == "func5":
            print("func5 play")
            dataglp.switch_graph(self.fig, self.ax, "拍手の推移", "df_time_hakusyu_point_100")
        elif funcname == "func6":
            print("func5 play")
            print(dataglp.get_all_URL())
        elif funcname == "func7":
            dataglp.switch_graph(self.fig, self.ax, "参照URLランキング", "urltable")



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

    def conpanel(self):
        print("conpanel press")
        graphpanel = self.ids.graph_view
        graphpanel.load_data()

        configpanel = self.ids.conpanel
        configpanel.make_config_panel(["tagai","hamada"])

    # Windowにドロップされた際発生するイベント
    # ファイル名を取得する
    def _on_file_drop(self, window, file_path):
        global loadfilepath
        loadfilepath = file_path.decode()
        self.filepath = os.path.basename(file_path.decode())
        self.fileinputimage = imagedir + 'inputimage.png'

class CommentShowApp(App):

    def __init__(self, **kwargs):
        super(CommentShowApp, self).__init__(**kwargs)
        self.title = 'コメント見える君'
    
    def build(self):
        return ShowWidget()