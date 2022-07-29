import requests
import os


class Code:
    def __init__(self):
        self.url = [
            "https://api.uiverse.io/buttons?type=button&orderBy=popular",
            "https://api.uiverse.io/buttons?type=button-of-the-day&orderBy=popular",
            "https://api.uiverse.io/buttons?type=card&orderBy=popular",
            "https://api.uiverse.io/buttons?type=checkbox&orderBy=popular",
            "https://api.uiverse.io/buttons?type=input&orderBy=popular",
            "https://api.uiverse.io/buttons?type=spinner&orderBy=popular",
            "https://api.uiverse.io/buttons?type=switch&orderBy=popular",
        ]
        self.headers = {
            "user-agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 86.0.4240.198Safari / 537.36"
        }

    def send_request(self, url):
        return requests.get(url, headers=self.headers, timeout=3).json()

    def run(self):
        for url in self.url:
            html_str = self.send_request(url)
            for val in html_str['buttons']:
                css = val['scopedCss']
                html = val['html']
                first = css.index('.')
                last = css.find(' ', first)
                print(first)
                print(css[first + 1:last])

                content = (
                        '<html lang="en">'
                        '<head>'
                        '<meta charset="UTF-8">'
                        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
                        '<title > Document </title>'
                        '<style >' + css + '</style>'
                                           '</head>'
                                           '<body><div class="' + css[first + 1:last] + '">' + html + '</div></body>'
                                                                                                      '</html>'
                )
                # break
                path = "D:\\pythonProject\\爬虫\\爬取Button\\" + url[36:-16]
                if not os.path.exists(path=path):
                    os.makedirs(path)
                with open(path + '/' + val['id'] + '.html', 'w',
                          encoding='utf-8') as ht:
                    ht.write(content)


def main():
    code = Code()
    code.run()


if __name__ == '__main__':
    main()
