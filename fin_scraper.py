import sqlite3
import logging
import time
import smtplib
import requests
import requests_cache

from selenium import webdriver


path = "/home/bart/PythonProjects/flight/chrome/chromedriver"
browser = webdriver.Chrome(path)
browser.get('https://www.gov.pl/web/finanse/ostrzezenia-i-wyjasnienia-podatkowe?page=2')

def getArchiveArticles():
    articles_list = []
    url = 'https://mf-arch2.mf.gov.pl/ministerstwo-finansow/wiadomosci/ostrzezenia-i-wyjasnienia-podatkowe'
    browser.get(url)
    articles = browser.find_elements_by_class_name('article-source-title')
    for element in articles:
        article = {}
        article['title'] = element.text
        article['url'] = element.get_attribute('href')
        articles_list.append(article)

    browser.get('https://mf-arch2.mf.gov.pl/web/bip/ministerstwo-finansow/wiadomosci/ostrzezenia-i-wyjasnienia-podatkowe?p_p_id=101_INSTANCE_M1vU&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_101_INSTANCE_M1vU_delta=20&_101_INSTANCE_M1vU_keywords=&_101_INSTANCE_M1vU_advancedSearch=false&_101_INSTANCE_M1vU_andOperator=true&cur=2')
    articles = browser.find_elements_by_class_name('article-source-title')
    logging.info(len(articles))
    for element in articles:
        article = {}
        article['title'] = element.text
        article['url'] = element.get_attribute('href')
        articles_list.append(article)
    return articles_list


def make_database():
    database_connection = sqlite3.connect('articles.db')
    database_connection.execute("DROP TABLE IF EXISTS Articles")
    database_connection.commit()

    try:
        with database_connection:
            database_connection.execute("""CREATE TABLE Articles(
                Title TEXT,
                Link TEXT
            )""")
    except sqlite3.OperationalError as error:
        logging.warning(error)

def insert_articles_to_database(articles_list):
    database_connection = sqlite3.connect('articles.db')
    cursor = database_connection.cursor()
    for article in articles_list:
        cursor.execute("SELECT Title from Articles WHERE Title=?",(article['title'],))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO Articles VALUES (?,?)",(article['title'],article['url']))
            database_connection.commit()
                
#getCurrentArticles()
#updateArticles()
#scheduleJob()

a = getArchiveArticles()
make_database()
insert_articles_to_database(a)
#print(a)