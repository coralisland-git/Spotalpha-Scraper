# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals

import MySQLdb


class ChainxyPipeline(object):

    def __init__(self):

        self.db = ''

    @classmethod

    def from_crawler(cls, crawler):

        pipeline = cls()

        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)

        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)

        return pipeline

    def spider_opened(self, spider):

        self.db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="mydb")       

        cur = self.db.cursor()

        self.table_name = 'spotalpha'

        _SQL = """SHOW TABLES"""

        cur.execute(_SQL)

        results = cur.fetchall()

        print('All existing tables: ', results) # Returned as a list of tuples

        results_list = [item[0] for item in results] 

        if table_name in results_list:

            print(table_name, 'was found!')

        else:

            print(table_name, 'was NOT found!')

            _SQL = """CREATE TABLE %s (

                id int auto_increment not null primary key,

                name varchar(50),

                price varchar(20),

                state varchar(20),

                );""" %table_name

            cur.execute(_SQL)


    def spider_closed(self, spider):

        self.db.close()


    def process_item(self, item, spider):

        cur = self.db.cursor()

        check_query = "select * from %s where name='%s'" %(self.table_name, item['name'])

        count = cur.execute(check_query)

        if count == 0:

            sql = "INSERT INTO %s " 

            sql += "(name, price, state) "

            sql += "VALUES ('%s', '%s', '%s'); " %(self.table_name, item['name'], item['price'], item['state'])

        else :

            sql = "UPDATE %s SET name='%s', price='%s', state='%s' " %(self.table_name, item['name'], item['price'], item['state'])

        cur.execute(sql)

        self.db.commit()

        return item