"""文件夹图标批量修改"""
import os
import stat


class ModifyFolderICON():
    def __init__(self, icon_path, **kwargs):
        assert os.path.exists(icon_path)
        self.icon_path = icon_path
        self.cur_dir = os.getcwd()

    def create_folder(self):
        for i in range(24):
            path_jin = os.path.join(self.cur_dir, 'jin{}'.format(i+1))
            if not os.path.exists(path_jin):
                os.makedirs(path_jin)

    '''run'''

    def run(self):
        cur_dir = self.cur_dir
        for root, dirs, files in os.walk(cur_dir, topdown=False):
            os.chmod(root, stat.S_IREAD)
            for d in dirs:
                os.chdir(f'{os.path.join(root, d)}')
                if os.path.exists('desktop.ini'):
                    os.system('attrib -h -s desktop.ini')
                with open('desktop.ini', 'w') as fp:
                    fp.write('[.ShellClassInfo]' + '\n' + f'IconResource={self.icon_path},0')
                os.system('attrib +h desktop.ini')
                os.chdir(f'{cur_dir}')


if __name__ == '__main__':
    start_run = input("start run?---y/n")
    if start_run == 'y':
        print("-----start------")
        print("-----running-----")
        run_client = ModifyFolderICON(icon_path=r'D:\pythonProject\修改文件夹图标\code\jin.ico')
        run_client.create_folder()
        run_client.run()
        print("-----done-----")
        input('enter to exit')
