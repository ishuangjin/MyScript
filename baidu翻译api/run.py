# import sys
# import os
# parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, parentdir)
from config import env_init
from mods.Baidu_Text_transAPI import DoTranslate


# 要翻译的语言和内容
parser_dict = env_init.parser_dict
from_lang = parser_dict['from_lang']
to_lang = parser_dict['to_lang']
query = parser_dict['query']


# 2. 把翻译得出的结果，自动再次翻译为中文并输出
def trans_main():
    trans_fir = DoTranslate(from_lang, to_lang, query)
    first_result = trans_fir.post()
    trans_sec = DoTranslate(to_lang, from_lang, first_result)
    second_restult = trans_sec.post()


# 3. 读取剪切板内容进行翻译，翻译结果可点击按钮存入剪切板
def get_

def run():
    trans_main()


run()
