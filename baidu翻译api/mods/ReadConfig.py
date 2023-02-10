import configparser


def read_config():
    ini_path = r'D:\Github\MyScript\baidu翻译api\config\config.ini'
    config = configparser.ConfigParser()
    config.read(ini_path, encoding='GB18030')

    parser_list = []
    for sections in config.sections():
        for items in config.items(sections):
            parser_list.append(items)
    return parser_list


def get_all_parser():
    parser_list = read_config()

    parser_dict = {}
    for key, values in parser_list:
        parser_dict[key] = values
    return parser_dict


if __name__ == "__main__":
    print(read_config())
    parser_dict = get_all_parser()
    print(parser_dict)
    print(parser_dict['appid'])
# end main
