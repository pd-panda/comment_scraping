#-*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

import threading

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


# matplotlib組み込み
import numpy as np
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
import matplotlib.pyplot as pl
import sys, os

import pandas as pd

from Source.commentscraper import Scraper
from Source.class_graph import GraphView

scr = Scraper()
glp = GraphView()

# デフォルトに使用するフォントを変更する
resource_add_path('./Source/fonts')
LabelBase.register(DEFAULT_FONT, 'ヒラギノ丸ゴ ProN W4.ttc') #日本語が使用できるように日本語フォントを指定する

imagedir = "./Source/image/"

class ShowWidget(Widget):
    text = StringProperty()    # プロパティの追加
    source  = StringProperty(imagedir + 'lefton.png')
    color = ListProperty([1,1,1,1])

    def __init__(self, **kwargs):
        super(ShowWidget, self).__init__(**kwargs)
        self.text = 'How are you?'
        print("pressed")
        self.color = [1, 1, 1 , 1]

    def buttonClicked1(self):        # ボタンをクリック時
        self.text = 'I am fine!'
        print("pressed")
        self.color = [1, 0, 1 , 1]
    
    def buttonClicked2(self):        # ボタンをクリック時
        self.text = 'I am soso!'
        print("pressed")
        self.color = [1, 1, 0 , 1]
    
    def buttonClicked3(self):        # ボタンをクリック時
        self.text = 'I am happy!'
        print("pressed")
        self.color = [0, 1, 1 , 1]

    def buttonClickedroom(self):        # ボタンをクリック時
        self.text = 'room名より取得'
        self.source = imagedir + 'lefton.png'
        self.color = [0, 1, 1 , 1]
        print("buttonClickedroom!!!")

    def buttonClickedfile(self):        # ボタンをクリック時
        self.text = 'ファイルから取得'
        self.source = imagedir + 'righton.png'
        self.color = [0, 1, 1 , 1]
        print("buttonClickedfile!!!")

    def buttonClickedroomDone(self):
        print("scraper start!")
        t1 = threading.Thread(target=scr.main, args=["カフカ読書会"])
        t1.start()
        print("scraper end!!!")

    def plottest(self):
        glp.main()

    
"""
class GraphView(BoxLayout):
    def __init__(self, **kwargs):
        super(GraphView, self).__init__(orientation='vertical')
        self.add_widget(self.graph_plot_sample())

    def graph_plot_sample(self):
        self.fig, ax = pl.subplots()
        x = np.linspace(-np.pi, np.pi)
        y = np.sin(x)
        ax.set_xlabel("X label")
        ax.set_ylabel("Y label")
        ax.grid(True)
        ax.plot(x, y)
        return self.fig.canvas
"""
class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = 'コメント見える君'
    
    def build(self):
        return ShowWidget()