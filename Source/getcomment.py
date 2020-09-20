# -*- coding: utf-8 -*-

import os
import pandas as pd


class GetComment:
    """
    コメントを取得する
    """
    def get_textdata_from_path(self, path):
        """
        filepathからテキストデータを抽出する

        Parameters
        ----------
        path : str
            読み込みたいテキストファイルのパス

        Returns
        -------
        readtxt : str
            抽出したテキストデータ
        """
        with open(path) as f:
            readtxt = f.read()
        return readtxt
    
    def get_datalist_from_textdata(self, textdata):
        """
        textdataからdatalist(timelist,textlist,namelist)を抽出する

        Parameters
        ----------
        textdata : str
            datalistに変換したいテキストデータ

        Returns
        -------
        datalist : list of str
            抽出したデータリスト。[[time],[text],[name]]
        """
        readtxtlist = textdata.split('\n')
        timelist = []
        namelist = []
        textlist = []

        if '開始 ' in readtxtlist[0]:
            count = 0
            for a in readtxtlist[:len(readtxtlist)-1:]:
                if len(a.split('\t')) == 1:
                    textlist[-1]+=a.split('\t')[0]
                else:
                    timelist.append(a.split('\t')[0])
                    namelist.append(a.split('\t')[1].split(' : ')[0].lstrip('開始 '))
                    textlist.append(a.split('\t')[1].split(' : ')[1])

        else:
            for a in readtxtlist:
                if len(a.split('\t')) == 1:
                    textlist[-1]+=a.split('\t')[0]
                else:
                    timelist.append(a.split('\t')[0])
                    namelist.append(a.split('\t')[1])
                    textlist.append(a.split('\t')[2])
        datalist = []
        datalist.append(timelist)
        datalist.append(textlist)
        datalist.append(namelist)
        #print(datalist)
        return datalist
    
    def get_df_from_datalist(self, datalist, columns=['time', 'comment', 'contributor']):
        """
        datalistからdetaframeを生成する

        Parameters
        ----------
        datalist : str
            読み込みたいテキストファイルのパス
        
        indexs : list of str, default ['time', 'comment', 'contributor']
            dataframeにつけるindex

        Returns
        -------
            カラム付きのdataframe
        """
        return pd.DataFrame(datalist, index=columns).T
    
    def save_csv_from_df(self, df, path):
        """
        dataframeをcsvとして保存する

        Parameters
        ----------
        df : dataframe
            保存するdetaframe
        
        path : str
            csvファイルを保存する場所
        """
        df.to_csv(path)
    
    def main(self, filepath, savefilepath, columns=['time', 'comment', 'contributor']):
        """
        Parameters
        ----------
        filepath : str
            読み込むテキストファイルのパス名
        
        savefilepath : str
            csvファイルを保存する場所

        indexs : list of str
            dataframeにつけるindexのリスト
        """
        textlist = self.get_textdata_from_path(filepath)
        datalist = self.get_datalist_from_textdata(textlist)
        df = self.get_df_from_datalist(datalist, columns)
        self.save_csv_from_df(df, savefilepath)
        return df


if __name__ == "__main__":
    filedir = "txt"
    filename = "meeting_saved_chat.txt"
    filepath = os.path.join(os.getcwd(), filedir, filename)
    
    savefiledir = "csv"
    savefilename = "savecsvfile.csv"
    savefilepath = os.path.join(os.getcwd(), savefiledir, savefilename)
    
    indexs = ['time', 'comment', 'contributor']

    comment = GetComment()
    comment.main(filepath, savefilepath, indexs)