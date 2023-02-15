import configparser


class ConfigParser():
    def __init__(self, ini_path) -> None:
        self.ini_path = ini_path

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.ini_path, encoding='GB18030')

        parser_list = []
        for sections in config.sections():
            for items in config.items(sections):
                parser_list.append(items)
        return parser_list

    def get_all_parser(self):
        parser_list = self.read_config()

        parser_dict = {}
        for key, values in parser_list:
            parser_dict[key] = values
        return parser_dict


if __name__ == "__main__":
    ini_path = r'D:\Github\MyScript\baidu翻译api\config\config.ini'
    parserconfig = ConfigParser(ini_path)
    print(parserconfig.read_config())
    parser_dict = parserconfig.get_all_parser()
    print(parser_dict)
    print(parser_dict['appid'])
# end main
