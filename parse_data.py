from backend import active_insert
import requests as r
from bs4 import BeautifulSoup as bs
import time
from tqdm import tqdm
from vacancy import Vacancy
import sqlite3
import datetime

def find_city(field, city):
    headers = {"accept": "*/*",
               "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    base_url = "https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&search_period=30&text=%s&page=1" % (
    field)
    session = r.Session()
    request = session.get(base_url, headers=headers)
    soup = bs(request.content, "html.parser")
    cites = soup.find_all("a", attrs={'class': 'clusters-value'})
    for c in cites:
        if c.find("span", attrs={'data-qa': 'serp__cluster-item-title'}).text == city :
            href_c = c['href']
            return href_c
            break


def parse(field, city):
    sal = 0.0
    s = 0.0
    conn = sqlite3.connect("vac.db")  
    cursor = conn.cursor()

    headers = {"accept":"*/*" , "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    base_url = "https://hh.ru/search/vacancy" + find_city(field, city) + "page=1"
    session = r.Session()
    request = session.get(base_url, headers=headers)
    soup = bs(request.content, "html.parser")
    pages = soup.find_all("a", attrs={'data-qa': 'pager-page'})
    if len(pages)>1:
        end = int(pages[-1].text)
    else:
        end = 1 + 1

    for page in range(1, end):
        base_url = "https://hh.ru/search/vacancy" + find_city(field, city) + "&page=%d"%(page)
        session = r.Session()
        request = session.get(base_url, headers=headers)
        soup = bs(request.content, "html.parser")
        if request.status_code == 200:
            divs = soup.find_all("div", attrs={'data-qa': 'vacancy-serp__vacancy'})

            for div in divs:
                try:
                    title = div.find("a", attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                    href = div.find("a", attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                except:
                    title = "-"

                try:
                    company = div.find("a", attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                except:
                    company = "-"

                try:
                    salary = div.find("div", attrs={'class': 'vacancy-serp-item__compensation'}).text
                    vac = Vacancy(salary)
                    salary = vac.get_salary()
                except:
                    salary = "-1"

                try:
                    location = div.find("span", attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
                except:
                    location = "-"

                try:
                    skills = div.find("div", attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                except:
                    skills = "-"
                date = datetime.datetime.today().strftime("%m/%d/%Y")
                active_insert(field, city, date, title, company, salary, skills, location, href)

    cursor.close()
    conn.close()


