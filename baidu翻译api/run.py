# import sys
# import os
# parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, parentdir)
from mods.Baidu_Text_transAPI import DoTranslate


from_lang = 'en'
to_lang = 'zh'
query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'
trans_A = DoTranslate(from_lang, to_lang, query)
trans_A.post()
