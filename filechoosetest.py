import os
import sys
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.treeview import TreeViewLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from pprint import pprint
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
# 日本語フォント設定
resource_add_path('./Source/fonts')
LabelBase.register(DEFAULT_FONT, 'hiragimaruproNW4.ttc')
sm = ScreenManager()
path_inf = 'path_inf.json'
class MsgboxOk(BoxLayout):
    message_text = StringProperty()
    ok_button = ObjectProperty(None)
class MsgboxOkCancel(BoxLayout):
    message_text = StringProperty()
    ok_button = ObjectProperty(None)
    cancel_button = ObjectProperty(None)
class SetSCN(Screen):
    begin_path_dsp = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(SetSCN, self).__init__(**kwargs)
    def setSelect(self):
        content = LoadDialog(load = self.setSelectLoad, cancel = self.setSelectCancel)
        self._popup = Popup( title="読み込み中", content=content, size_hint=(0.9,0.9))
        self._popup.open()
    def setSelectLoad (self, path, filename):
        pprint(path)
        pprint(filename)
        #self.begin_path_dsp.text = filename[0]
        self.begin_path_dsp.text = path
        self._popup.dismiss()
    def setSelectCancel(self):
        self._popup.dismiss()
    def msgTestOk(self):
        pprint ('OKが押されました')
        self.popup.dismiss()
    def msgTestCancel(self):
        pprint ('CANCELが押されました')
        self.popup.dismiss()
    def selfOk(self):
        self.bl = {}
        self.bl['begin_path'] = self.begin_path_dsp.text
        pprint (self.bl)
        try:
            #raise OverflowError('やっちまったな')
            with open(path_inf, 'w') as fd:
                json.dump(self.bl, fd)
        except PermissionError as err:
            self.msg = '保存データを書き込もうとしましたが、書き込み許可がありません。\n'
            self.msg += 'パスは、' + self.bl['begin_path'] + 'です。\n'
            self.msg += '保存先の書き込み許可を確認するか、パスが適当かを確認してください。\n\n'
            self.msg += str(err)
            content = MsgboxOk \
                (ok_button= self.msgTestOk, \
                message_text= self.msg)
            self.popup = Popup(title='書き込み許可エラー', content=content)
            self.popup.open()
        except IOError as err:
            self.msg = '保存データを書き込もうとしましたが、書き込めません。\n'
            self.msg += '書き込み先機器に問題があるようです。\n'
            self.msg += '書き込み先機器の状態を確認してください。\n\n'
            self.msg += str(err)
            content = MsgboxOk \
                (ok_button= self.msgTestOk, \
                message_text= self.msg)
            self.popup = Popup(title='I/Oエラー', content=content)
            self.popup.open()
        except BaseException as err:
            self.msg = '保存データを書き込もうとしましたが、何らかのエラーが起きました。\n\n'
            self.msg += str(err)
            content = MsgboxOk \
                (ok_button= self.msgTestOk, \
                message_text= self.msg)
            self.popup = Popup(title='その他のエラー', content=content)
            self.popup.open()
        finally:
            sm.current = 'all'
    def selfCancel(self):
        sm.current = 'all'
class LoadDialog(FloatLayout):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def is_dir(self, dirname, filename):
        # ディスレクトリならTrueを返す
        return os.path.isdir(os.path.join(dirname, filename))
class AllSCN(Screen):
    tv = ObjectProperty(None)
    file_name = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    def msgOsErrorOk(self):
        print('OKが押されました')
        self.popup.dismiss()
        sys.exit()
    def begin_display(self, dt):
        path = ''
        thisos = os.name
        if thisos == 'posix':
            path = os.environ.get('HOME')
        elif thisos == 'nt':
            path = os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
        else:
            msg = '内部OS判定(os.name)が、"' + thisos + '”でした。\n'
            msg += 'サポートしているOSは、UNIX系統と、Windowsです。\n'
            msg += 'したがってこのOSはサポート外です。すみません。'
            content = MsgboxOk \
                (ok_button= self.msgOsErrorOk, \
                message_text= msg)
            self.popup = Popup(title='OSサポートエラー', content=content)
            self.popup.open()
            return
        self.manager.get_screen('set').begin_path_dsp.text = path
        self.tv.add_node(TreeViewLabel(text ='シンカリオン E1 とき'))
        self.tv.add_node(TreeViewLabel(text ='シンカリオン 0 ひかり'))
        self.tv.add_node(TreeViewLabel(text ='シンカリオン キハ32　鉄道ホビートレイン'))
    def setupButtonClicked(self):
        sm.current = 'set'
    def show_load(self):
        content = LoadDialog(load = self.load, cancel = self.dismiss_popup)
        self._popup = Popup( title="読み込み中", content=content, size_hint=(0.9,0.9))
        self._popup.open()
    def load (self, path, filename):
        pprint(filename)
        #self.file_name.text = filename[0]
        self.file_name.text = path
        #with open (os.path.join(path, filename[0])) as stream:
        #    self.text_input.text = stream.read()
        self.dismiss_popup()
    def dismiss_popup(self):
        self._popup.dismiss()
class FilelistApp(App):
    def build(self):
        allscn = AllSCN()
        setscn = SetSCN()
        Clock.schedule_once(allscn.begin_display, 0)
        sm.add_widget(allscn)
        sm.add_widget(setscn)
        return sm
if __name__ == '__main__':
    FilelistApp().run()