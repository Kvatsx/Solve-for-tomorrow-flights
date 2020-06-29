from selenium import webdriver
import pandas as pd
driver = webdriver.Chrome('D:\MMT\chromedriver\chromedriver.exe')

driver.get('https://flight.easemytrip.com/FlightList/Index?srch=DEL-Delhi-India|BOM-Mumbai-India|07/07/2020&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lng=&')

# data = driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]')
# for d in data:
#     print(d.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/div/div[2]/span[1]/text()'))

flightList = driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]')
# flightList = driver.find_elements_by_id('ResultDiv')
print(flightList[0])


d = driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]/div[1]/div[1]/div[1]/div[2]/span[1]')[0]
print("Data", d.text)

driver.quit()