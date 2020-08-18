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

from Source.showwidget import TestApp


if __name__ == '__main__':
    shw = TestApp()
    print("ss")
    shw.run()