# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import sys
import pandas as pd
import numpy as np

class Scraper:
    # 取得したいテキストのclassタグ
    textclass = ".Bubble__CommentText-v4d1le-2.kUKzWP"
    # 取得したい時間のclassタグ
    timeclass = ".Bubble__InformationText-v4d1le-6.Bubble__Time-v4d1le-7.bsRdRB"

    # データフレームのカラム名
    colname1 = "time"
    colname2 = "comment"
    colname3 = "contributor"

    # スクレイピングするルーム名
    room_name = "カフカ読書会"
    # 出力するcsvファイル名
    exportcsvfile = "data1.csv"

    # urlからhtmlを取得
    def get_html_from_url(self, url): 
        # ブラウザのオプションを格納する変数を取得
        options = Options()
        # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がる）
        options.set_headless(True)

        # ブラウザを起動する
        driver = webdriver.Chrome(chrome_options=options)
        # ブラウザでアクセスする
        driver.get(url)

        # jsが全てのチャットテキストを表示するまで待つ
        # 15秒でタイムアウト
        try:
            search_results = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".Bubble__CommentText-v4d1le-2.kUKzWP")
                    )
                )
            print('do something')
        except TimeoutException:
            print("timeout!!!!")
            sys.exit(1)

        # HTMLを文字コードをUTF-8に変換したものを返す
        return driver.page_source.encode('utf-8')



    # htmlからデータフレームを取得
    # time, comment, contributor
    def get_df_from_html(self, html):
        # BeautifulSoupで扱えるようにパースする
        soup = BeautifulSoup(html, "html.parser")
        # 時間のリスト生成
        times = self.elemlist_to_datalist(soup.select(self.timeclass))
        # テキストのリスト生成
        comments = self.elemlist_to_datalist(soup.select(self.textclass))

        create_df = self.create_df_from_datalists(times, comments)
        create_df[self.colname3] = np.nan
        # 作成したデータフレームを返す
        return create_df



    # 要素のリストからデータのリストに変換
    def elemlist_to_datalist(self, elemlist):
        return [x.text for x in elemlist]



    # 2つのデータリストからデータフレームを作成
    def create_df_from_datalists(self, datalist1, datalist2):
        return pd.DataFrame({ self.colname1: datalist1, self.colname2: datalist2})


    # データフレームを指定ファイル名のcsvファイルに出力
    def export_df_to_CSV(self, df, filename):
        df.to_csv(filename, encoding="utf_8_sig")

    def main(self, room_name= "カフカ読書会"):
        # スクレイピングするurl
        url = "https://commentscreen.com/comments?room=" + room_name

        # urlからhtmlを取得
        html = self.get_html_from_url(url)
        # htmlからデータフレームを取得
        dataframe = self.get_df_from_html(html)
        print("関数内DF表示")
        print(dataframe)

        # データフレームをcsvファイルに出力
        self.export_df_to_CSV(dataframe, self.exportcsvfile)

        return dataframe
        

'''
if __name__ == '__main__':
    # スクレイピングするurl
    url = "https://commentscreen.com/comments?room=" + room_name
    
    # urlからhtmlを取得
    html = get_html_from_url(url)
    # htmlからデータフレームを取得
    df = get_df_from_html(html)

    # データフレームをcsvファイルに出力
    export_df_to_CSV(df, exportcsvfile)
    print(df)
'''