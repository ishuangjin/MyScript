import configparser

# -实例化configParser对象
config = configparser.ConfigParser()
# -read读取ini文件
config.read(r'D:\Github\MyScript\baidu翻译api\config\config1.ini', encoding='GB18030')
# -sections得到所有的section，并以列表的形式返回
print('sections:' , ' ' , config.sections())

# -options(section)得到该section的所有option
print('options:' ,' ' , config.options('config'))

# -items（section）得到该section的所有键值对
print('items:' ,' ' ,config.items('session1'))

# -get(section,option)得到section中option的值，返回为string类型
print('get:' ,' ' , config.get('session2', 'option4'))

# -getint(section,option)得到section中的option的值，返回为int类型
print('getint:' ,' ' ,config.getint('session1', 'option2'))
print('getfloat:' ,' ' , config.getfloat('session1', 'option3'))
print('getboolean:' ,'  ', config.getboolean('session1', 'option1'))
"""
首先得到配置文件的所有分组，然后根据分组逐一展示所有
"""
for sections in config.sections():
    for items in config.items(sections):
        print(items)

