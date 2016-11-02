import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
import pandas as pd
import MySQLdb

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

for npage in range(1, 9999):
    url = "https://www.seek.co.nz/jobs/in-new-zealand/#dateRange=999&workType=0&industry=&occupation=&graduateSearch=false&salaryFrom=0&salaryTo=999999&salaryType=annual&companyID=&advertiserID=&advertiserGroup=&keywords=&page=" + str(npage) + "&displaySuburb=&seoSuburb=&where=All+New+Zealand&whereId=3001&whereIsDirty=false&isAreaUnspecified=false&location=3001&area=&nation=3001&sortMode=ListedDate&searchFrom=quick&searchType="
    browser = webdriver.Chrome('C:\Python27\chromedriver-Windows')
    browser.get(url)

    jobs = []
    jobscards = browser.find_elements_by_class_name('job-title')
    for job in jobscards:
        jobs.append(job.text)
    if len(jobs) == 0:
        browser.quit()
        exit()  # stop if reaching the final page

    advertisers = []
    advertiserscards = browser.find_elements_by_class_name('advertiser-name')
    for advertiser in advertiserscards:
        advertisers.append(advertiser.text)

    # points = []
    # pointscards = browser.find_elements_by_class_name('bullet-points')
    # for point in pointscards:
    # points.append(point.text)

    descriptions = []
    descriptionscards = browser.find_elements_by_class_name('job-description')
    for description in descriptionscards:
        descriptions.append(description.text)

    classifications = []
    classificationscards = browser.find_elements_by_class_name('classification')
    for classification in classificationscards:
        classifications.append(classification.text)

    # dates = []
    # datescards = browser.find_elements_by_class_name('listing-date')
    # for date in datescards:
    #     dates.append(date.text)

    salarys = []
    salaryscards = browser.find_elements_by_class_name('salary-range')
    for salary in salaryscards:
        salarys.append(salary.text)

    locations = []
    locationscards = browser.find_elements_by_class_name('location')
    for location in locationscards:
        locations.append(location.text)

    links = []
    linkscards = browser.find_elements_by_class_name('job-title')
    for link in linkscards:
        links.append(link.get_attribute('href'))

    seeks = []
    for seek in range(len(jobs)):
        seeks.append("SEEK")

    data = {"job": jobs, "advertiser": advertisers, "description": descriptions, "classification": classifications,
            "salary": salarys, "location": locations, "link": links, "source": seeks}

    browser.quit()

    db = MySQLdb.connect("localhost", "root", "Tianfeng1", "jobs")
    cursor = db.cursor()
    table = 'details'
    columns_string = '(job, advertiser, description, classification, salary, location, link, source)'
    for x in range(len(jobs)):
        values_string = '(' + "'" + str(data['job'][x]).replace("'", "''") + "'" + ', ' + "'" + str(
            data['advertiser'][x]).replace("'", "''") + "'" + ', ' + "'" + str(data['description'][x]).replace("'",
                                                                                                               "''") + "'" + ', ' + "'" + str(
            data['classification'][x]).replace("'", "''") + "'" + ', ' + "'" + str(data['salary'][x]).replace("'",
                                                                                                              "''") + "'" + ', ' + "'" + str(
            data['location'][x]).replace("'", "''") + "'" + ', ' + "'" + str(data['link'][x]) + "'" + ', ' + "'" + str(
            data['source'][x]) + "'" + ')'
        sql = 'INSERT INTO ' + table + ' ' + columns_string + ' VALUES ' + values_string + ';'

        try:
            cursor.execute(sql)
            db.commit()
        except:
            print "something wrong"
            db.rollback()
    db.close()
    print "Page " + str(npage) + " loading finished!"+" page " + str(npage + 1) + " start..."








