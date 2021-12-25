import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import time


def crawl(n, path):
    Q = []
    with open(path) as f:
        Q.append(f.readlines())
    Q = [Q[0][i][:-1] for i in range(len(Q[0]))]
    driver = webdriver.Chrome()
    counter = 0
    papers = dict()
    while counter < n:
        try:
            url = Q.pop(0)
            id = str(re.findall(r"\d+", url)[-1])
            if id in papers:
                continue
            paper = {}
            driver.get(url)
            whole_page = WebDriverWait(driver, 10).until(lambda d: d.find_element_by_css_selector('#mainArea')) 
            paper['id'] = id
            paper['title'] = whole_page.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/h1').text
            paper['abstract'] = whole_page.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/p').text
            paper['date'] = str(whole_page.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/a/span[1]').text)
            temp = list(map(lambda d: d.text, whole_page.find_elements_by_css_selector('.authors .author-item a:nth-of-type(1)')))
            temp2 = []
            for i in temp:
                if i == '':
                    continue
                temp2.append(i)
            paper['authors'] = temp2
            paper['related_topics'] = list(map(lambda d: d.text, whole_page.find_elements_by_css_selector('.tag-cloud .ma-tag .text')))
            citation = whole_page.find_element_by_css_selector('.ma-statistics-item[aria-label="Citations"] .data .count').text
            paper['citation_count'] = citation.replace(',', '')
            ref_count = whole_page.find_element_by_css_selector('.ma-statistics-item[aria-label="References"] .data .count').text
            paper['reference_count'] = ref_count.replace(',', '')
            temp3 = WebDriverWait(driver, 10).until(lambda d: d.find_elements_by_css_selector('.primary_paper a.title'))
            temp4 = []
            for i in temp3:
                temp4.append(i.get_attribute('href'))
            refs = temp4
            temp5 = []
            for i in refs:
                temp5.append(str(re.findall(r"\d+", i)[-1]))
            paper['references'] = temp5
            Q.extend(refs)
            counter += 1
            papers[id] = paper
            time.sleep(4)
        except:
            print("ERROR")
    result = []
    for key in papers:
        result.append(papers[key])
    with open('crawling_test.json', 'w') as json_file:
        json.dump(papers, json_file, indent=4)
    print('Crawling results saved on crawling_test.json file!')
    

crawl(10, 'start.txt')























# driver = webdriver.Chrome()
# url = 'https://academic.microsoft.com/paper/2981549002'
# driver.get(url)
# #ref = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'primary_paper')))
# ref = driver.find_elements_by_class_name('primary_paper')
# for r in ref:
#     atag = r.find_element_by_xpath('//*[@id="mainArea"]/router-view/router-view/ma-edp-serp/div/div[2]/div/compose/div/div[2]/ma-card[1]/div/compose/div/div[1]/a[1]')
#     print(atag.get_attribute('href'))

# # cur_url = driver.current_url

# title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainArea"]/router-view/div/div/div/div/h1'))).text
# print(title)
# ref_count = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainArea"]/router-view/div/div/div/div/div[1]/ma-statistics-item[1]/div[2]/div[2]/div[1]'))).text
# print(ref_count)
# citation = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainArea"]/router-view/div/div/div/div/div[1]/ma-statistics-item[2]/div[2]/div[2]/div[1]'))).text
# print(citation)
# author = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainArea"]/router-view/div/div/div/div/ma-author-string-collection/div/div/div/a[1]'))).text
# print(author)
# abstract = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainArea"]/router-view/div/div/div/div/p'))).text
# print(abstract)
# date = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainArea"]/router-view/div/div/div/div/a/span[1]'))).text
# print(date)







#driver.implicitly_wait(10)


# elems = driver.find_elements_by_xpath("//a[@href]")
# for elem in elems:
#     print(elem.get_attribute("href"))

# driver.get('https://academic.microsoft.com/paper/3105081694')
# driver.implicitly_wait(15)
# text = driver.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/h1').text
# print(text)

# content = driver.find_elements_by_class_name('name-section')
# items = []
# for x in content:
#     title = x.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/h1').text
#     ref_count = x.find_element_by_xpath('//*[@id="mainArea"]/router-view/div/div/div/div/div[1]/ma-statistics-item[1]/div[2]/div[2]/div[1]').text
#     item = {
#         'title': title,
#         'ref_count': ref_count
#     }
#     items.append(item)