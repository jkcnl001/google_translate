
# coding=utf-8
import random
import requests
import re
import time
import languages
import json
import jsCompile
import config
import io
import sys
import os
import platform


class GoogleTranslator():
    # proxies = {
    #     "http": "http://127.0.0.1:7890",
    #     "https": "http://127.0.0.1:7890",
    # }
    host = 'translate.google.cn'
    url = "https://" + host + "/translate_a/single"

    headers = {
        "Host": host,
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Referrer": "https://" + host,
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0"
    }

    def translate(self, text, to="en", src="auto"):
        _to = languages.getCode(to)
        if(not _to):
            print "language " + to + " is not supported"
            return
        to = _to
        src = languages.getCode(src)
        # 更新 agent
        self.headers["User-Agent"] = self.__getUserAgent()
        params = {
            "client": "webapp",  # "t" "webapp"
            "sl": src,
            "tl": to,
            "hl": "en",
            "dt": ["t"],
            "ie": "UTF-8",
            "oe": "UTF-8",
            "otf": 1,
            "ssel": 0,
            "tsel": 0,
            "kc": 1,
            "q": text,
            "tk": jsCompile.TL(text)
        }
        response = requests.post(
            self.url, params=params, headers=self.headers)
        response.raise_for_status()
        result = ""
        jsonText = response.text
        if len(jsonText) > 0:
            jsonResult = json.loads(jsonText)
            if len(jsonResult[0]) > 0:
                for item in jsonResult[0]:
                    result += item[0]
        return result

    def __getUserAgent(self):
        browsers = [
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
                "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
                "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
                "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"
            ],
            [
                "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
                "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6"
            ],
            [
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
                "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  rv:11.0) like Gecko",
                "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
                "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)"
            ],
            [
                "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
                "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
                "Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51",
                "Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50",
                "Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50",
                "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11",
                "Opera/9.80 (X11; Linux x86_64; U; bg) Presto/2.8.131 Version/11.10",
                "Opera/9.80 (X11; Linux i686; U; ja) Presto/2.7.62 Version/11.01",
                "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; de) Opera 11.01",
                "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.6.37 Version/11.00"
            ],
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
                "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
                "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
            ]
        ]
        agents = browsers[random.randint(0, len(browsers)-1)]
        return agents[random.randint(0, len(agents)-1)]


def main():
    if platform.system() == 'Windows':
        os.system("chcp 65001")
    translator = GoogleTranslator()
    project_dir = os.path.dirname(sys.argv[0])

    src = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(
        project_dir, "src.txt")

    dest = sys.argv[2] if len(
        sys.argv) >= 3 else os.path.join(project_dir, "dest.txt")

    wait_time_min = sys.argv[3] if len(
        sys.argv) >= 4 else 5

    wait_time_max = sys.argv[3] if len(
        sys.argv) >= 4 else wait_time_min * 2

    if(not os.path.exists(src) or not os.path.isfile(src)):
        print "文件路径错误"
        exit(0)
    with io.open(dest, 'w', encoding='utf-8') as wf:
        for languages in config.to_translate_languages:
            wf.write(u'\n\n\n{}:\n\n'.format(languages))
            print ("翻译："+languages)
            for line in io.open(src, 'r', encoding='utf-8'):
                result = translator.translate(line, to=languages)
                wf.write(result.strip()+"\n")
                wf.flush()
                wait = wait_time_min + random.random() * (wait_time_max - wait_time_min)
                print("等待: " + str(wait))
                time.sleep(wait)


if __name__ == "__main__":
    startTime = time.time()
    main()
    print('%.2f seconds' % (time.time() - startTime))
