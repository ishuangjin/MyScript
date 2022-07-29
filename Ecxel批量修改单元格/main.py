## 源码

# -*- coding:utf-8 -*-
import wx
import openpyxl as vb
import os
import xlwings as xw


class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,
                          None,
                          title='Ecxel批量修改单元格',
                          size=(580, 350),
                          name='frame',
                          style=541072384)
        icon = wx.Icon(r'./jin.ico')
        self.SetIcon(icon)
        self.qdck = wx.Panel(self)
        self.Centre()
        self.bjk1 = wx.TextCtrl(self.qdck,
                                size=(100, 40),
                                pos=(20, 20),
                                value='单元格，如A2',
                                name='text',
                                style=0)
        self.bjk2 = wx.TextCtrl(self.qdck,
                                size=(100, 40),
                                pos=(140, 20),
                                value='单元格，如A2',
                                name='text',
                                style=0)
        self.bjk3 = wx.TextCtrl(self.qdck,
                                size=(100, 40),
                                pos=(260, 20),
                                value='单元格，如A2',
                                name='text',
                                style=0)
        self.bjk6 = wx.TextCtrl(self.qdck,
                                size=(100, 40),
                                pos=(20, 80),
                                value='替换文本',
                                name='text',
                                style=wx.TE_MULTILINE)
        self.bjk7 = wx.TextCtrl(self.qdck,
                                size=(100, 40),
                                pos=(140, 80),
                                value='替换文本',
                                name='text',
                                style=wx.TE_MULTILINE)
        self.bjk8 = wx.TextCtrl(self.qdck,
                                size=(100, 40),
                                pos=(260, 80),
                                value='替换文本',
                                name='text',
                                style=wx.TE_MULTILINE)
        self.an1 = wx.Button(self.qdck,
                             size=(140, 40),
                             pos=(400, 20),
                             label='运行',
                             name='button')
        self.an1.Bind(wx.EVT_BUTTON, self.an1_anbdj)
        self.sheet = wx.TextCtrl(self.qdck,
                                 size=(140, 40),
                                 pos=(400, 80),
                                 value='Sheet1',
                                 name='text',
                                 style=wx.TE_MULTILINE)
        self.msg = wx.TextCtrl(self.qdck,
                               size=(520, 120),
                               pos=(20, 150),
                               value='请将Sheet1替换为你需要修改的excel文件中的工作表名称',
                               name='text',
                               style=wx.TE_MULTILINE)

    def an1_anbdj(self, event):
        self.msg.Clear()
        cell_list = [self.bjk1, self.bjk2, self.bjk3]
        text_list = [self.bjk6, self.bjk7, self.bjk8]
        self.set01 = zip(cell_list, text_list)
        self.sheet_name = self.sheet.GetValue()
        self.dict01 = {}
        for cell, text in self.set01:
            cell = cell.GetValue()
            text = text.GetValue()
            if '单元格' not in cell:
                self.dict01[cell] = text
        dir = wx.DirSelector('请选择需要处理的文件夹')
        file_list = list(os.scandir(dir))
        self.msg.Clear()
        for file in file_list:
            type = os.path.basename(file).split('.')[-1]
            if type == 'xlsx':
                self.revise(file)
            elif type == 'xls':
                self.revise_xls(file)
            else:
                pass
        print('an1,按钮被单击')

    def revise(self, file):
        try:
            wb = vb.load_workbook(file)
            ws = wb[self.sheet_name]
            for cell, text in self.dict01.items():
                ws[cell].value = text
            wb.save(os.path.abspath(file))
        except (KeyError, IndexError) as e:
            self.msg.AppendText(f'{file}出错：\n{e}')

        except IndexError as e:
            self.msg.AppendText(f'{file}出错：\n{e}')

        except Exception as e:
            self.msg.AppendText(f'{file}出错：\n{e}')

        else:
            self.msg.AppendText(f'{file}处理完成\n')

    def revise_xls(self, file):
        try:
            app = xw.App(visible=False, add_book=False)
            wb = app.books.open(file)
            sht = wb.sheets[self.sheet_name]
            for cell, text in self.dict01.items():
                rng = sht[cell]
                rng.value = text
            wb.save()
            wb.close()
            app.quit()

        except (KeyError, IndexError) as e:
            self.msg.AppendText(f'{file}出错：\n{e}')

        except IndexError as e:
            self.msg.AppendText(f'{file}出错：\n{e}')

        except Exception as e:
            self.msg.AppendText(f'{file}出错：\n{e}')

        else:
            self.msg.AppendText(f'{file}处理完成\n')


class myApp(wx.App):

    def OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True


if __name__ == '__main__':
    app = myApp()
    app.MainLoop()
