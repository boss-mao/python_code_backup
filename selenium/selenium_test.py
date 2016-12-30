#!/usr/bin/python
#-*- coding: utf-8 -*-
import time
from selenium import webdriver


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get('http://weixin.sogou.com/')
    queryElement = driver.find_element_by_id("upquery")
    queryElement.send_keys(query)
    time.sleep(1)
    clickElement = driver.find_element_by_class_name("swz")
    clickElement.click();
    resultNode = driver.find_elements_by_tag_name("h4")
    for h4Node in resultNode:
        linkNode = h4Node.find_element_by_tag_name("a")
        print h4Node.text + ":" + linkNode.get_attribute("href")
