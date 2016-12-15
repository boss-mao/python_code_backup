#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
import time
import uuid
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver


#添加item到数据库
def add_item(item):
    mongo_db = MongoClient('mongodb://192.168.1.6:27017/').spider
    mongo_db.credit_item.insert_one(item)

#解析每个item
def parse_item(driver):
    order_list_element = driver.find_elements_by_xpath('//div[@class="op_trust_mainBox"]/ul[@class="op_trust_main"]/li')
    for order_list_node in order_list_element:
        # 解析姓名和身份证号
        name = order_list_node.find_element_by_xpath('div[@class="c-clearfix op_trust_btn_list"]/span[@class="op_trust_name"]').get_attribute('innerText')
        identity_card = order_list_node.find_element_by_xpath('div[@class="c-clearfix op_trust_btn_list"]/span[@class="op_trust_fl op_trust_papers"]').get_attribute('innerText')
        item = {'uuid': str(uuid.uuid1()), "createtime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"name":name,"identity_card":identity_card}
        #解析详情
        trs = order_list_node.find_elements_by_tag_name("tr")
        for tr in trs:
            key_element = tr.find_element_by_xpath('td[@class="op_trust_tdLeft"]')
            key = key_element.get_attribute('innerText').replace(u"：","")
            value_element = tr.find_element_by_xpath('td[@class="op_trust_tdRight"]')
            value = value_element.get_attribute('innerText').replace(u"：","")
            item[key] = value
        yield item
    pass

#解析当前页
def parse_list(driver):
    try:
         items = parse_item(driver)
         for item in items:
             add_item(item)
    except Exception as ex:
         logging.exception(ex)

    # 点击进入下一页
    next_page_element = driver.find_element_by_class_name("op_trust_page_next")
    next_page_element.click();
    time.sleep(1)
    return parse_list(driver)

#通过百度抓取失信人员名单
def main():
   try:
       driver = webdriver.Chrome()
       driver.get(
           'https://www.baidu.com/s?wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA%E5%91%98%E5%90%8D%E5%8D%95%E6%9F%A5%E8%AF%A2&rsv_idx=2&tn=baiduhome_pg&usm=1&ie=utf-8&rsv_crq=7&bs=%E4%B8%AD%E5%9B%BD%E6%B3%95%E9%99%A2%E7%BD%91+%E5%A4%B1%E4%BF%A1&qq-pf-to=pcqq.temporaryc2c')
       # 等待网页加载完成
       time.sleep(3)
       parse_list(driver)
   finally:
       driver.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='log.txt',
                        filemode='w')
    try:
         main()
    except Exception as ex:
         logging.exception(ex)

    print "抓取完成"

