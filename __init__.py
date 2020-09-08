#-*- coding: utf-8 -*-
import os

try:
  import kivy
except ImportError:
  print("Trying to Install required module: kivy")
  os.system('conda install -c conda-forge kivy')

try:
  import numpy
except ImportError:
  print("Trying to Install required module: numpy")
  os.system('conda install -c anaconda numpy')

try:
  import matplotlib
except ImportError:
  print("Trying to Install required module: matplotlib")
  os.system('conda install -c conda-forge kivy-garden')
  os.system('conda install matplotlib==2.2.2')
  os.system('garden install matplotlib')

try:
  import pandas
except ImportError:
  print("Trying to Install required module: pandas")
  os.system('conda install -c anaconda pandas')

try:
  import bs4
except ImportError:
  print("Trying to Install required module: bs4")
  os.system('conda install -c conda-forge bs4')

try:
  import selenium
except ImportError:
  print("Trying to Install required module: selenium")
  os.system('conda install -c conda-forge selenium')
  
#ここから，内部処理用
 
try:
  import datetime
except ImportError:
  print("Trying to Install required module: datetime")
  os.system('conda install -c trentonoliphant datetime')
 
try:
  import seaborn as sns
except ImportError:
  print("Trying to Install required module: seaborn")
  os.system('conda install -c conda-forge seaborn')

try:
  from collections import Counter, defaultdict
except ImportError:
  print("Trying to Install required module: Counter, defaultdict")
  os.system('conda install -c auto counter')
  
try:
  import squarify
except ImportError:
  print("Trying to Install required module: squarify")
  os.system('conda install -c conda-forge squarify')

try:
  from pyknp import Juman
except ImportError:
  print("Trying to Install required module: Juman")
  os.system('conda install -c temporary-recipes pyknp')

try:
  import japanize_matplotlib
except ImportError:
  print("Trying to Install required module: japanize_matplotlib")
  os.system('pip install japanize-matplotlib')

from Source.showwidget import TestApp


if __name__ == '__main__':
    shw = TestApp()
    print("ss")
    shw.run()
