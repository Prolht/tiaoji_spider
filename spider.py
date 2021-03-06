# coding = utf-8
import re
from typing import List

import requests
from bs4 import BeautifulSoup

from config import SCHOOLS, RULES
from Slog import logger


def __drink_soup(url, parser = 'html.parser'):
    req = requests.get(url, timeout=100)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup


def __get_news(school) -> list:
    if RULES[school][2] == 'fail':
        return ''
    else:
        logger.info("开始查询{}招生信息".format(school))
        soup = __drink_soup(SCHOOLS[school])
        if RULES[school][2] == 'find':
            li_list = soup.find(RULES[school][0], attrs={'class':RULES[school][1]})
        elif RULES[school][2] == 'findAll':
            li_list = soup.findAll(RULES[school][0], attrs={'class':RULES[school][1]})
        re_pattern = '(?<=>).+?(?=<)'
        res = []
        for li in li_list:
            title = re.findall(re_pattern, str(li.find('a')))
            if title:
                res.append(title[0])
        return res


def get_info_from_schools() -> list:
    school_news = []
    for school, url in SCHOOLS.items():
        school_news.append(school)
        school_news.append(url)
        school_news.append('')
        school_news.append('')
        news = __get_news(school)
        school_news += news
        school_news.append('')
        school_news.append('')
    return school_news

        
if __name__ == '__main__':
    # print(get_info_gkd())
    # for school, url in SCHOOLS.items():
    #     print(RULES[school][1])
    print(get_info_from_schools())