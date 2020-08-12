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

# 取得したいテキストのclassタグ
textclass = ".Bubble__CommentText-v4d1le-2.kUKzWP"
# 取得したい時間のclassタグ
timeclass = ".Bubble__InformationText-v4d1le-6.Bubble__Time-v4d1le-7.bsRdRB"

# データフレームのカラム名
colname1 = "comment"
colname2 = "time"

# スクレイピングするルーム名
room_name = "カフカ読書会"
# 出力するcsvファイル名
exportcsvfile = "data1.csv"

# urlからhtmlを取得
def get_html_from_url(url): 
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
def get_df_from_html(html):
    # BeautifulSoupで扱えるようにパースする
    soup = BeautifulSoup(html, "html.parser")
    # テキストのリスト生成
    words = elemlist_to_datalist(soup.select(textclass))
    # 時間のリスト生成
    times = elemlist_to_datalist(soup.select(timeclass))

    # 作成したデータフレームを返す
    return create_df_from_datalists(words, times)



# 要素のリストからデータのリストに変換
def elemlist_to_datalist(elemlist):
    return [x.text for x in elemlist]



# 2つのデータリストからデータフレームを作成
def create_df_from_datalists(datalist1, datalist2):
    return pd.DataFrame({ colname1: datalist1, colname2: datalist2 })


# データフレームを指定ファイル名のcsvファイルに出力
def export_df_to_CSV(df, filename):
    df.to_csv(filename, encoding="utf_8_sig")

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