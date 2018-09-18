# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import Request

from chainxy.items import ChainItem

from lxml import etree

from lxml import html


class spotalpha(scrapy.Spider):

	name = 'spotalpha'

	domain = 'https://spotalpha.com/in'

	history = []


	def __init__(self):

		script_dir = os.path.dirname(__file__)

		file_path = script_dir + '/list.txt'

		with open(file_path) as data_file:    

			self.key_list = data_file.readlines()

	
	def start_requests(self):

		url  = 'https://spotalpha.com/v1/'

		headers = {

			"accept": "application/json, text/plain, */*",

			"accept-encoding": "gzip, deflate, br",

			"content-type": "application/json",

			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
		}
		
		data = { 

			"email" : "interactiveapp7@gmail.com",

			"password" : "12345678"
		}

		yield scrapy.Request(url=url, headers=headers, body=json.dumps(data), callback=self.parse, method="POST") 


	def parse(self, response):

		for key in self.key_list:

			link = self.domain + '/' + key.strip()

			yield scrapy.Request(link, callback=self.parse_detail)


	def parse_detail(self, response):

		item = ChainItem()

		try:

			item['name'] = ''.join(response.xpath('//div[contains(@class, "head_symbol")]//text()').extract()).strip()

			if item['name'] not in self.history:

				item['price'] = ''.join(response.xpath('//span[@class="head_price"]//text()').extract()).strip()

				item['state'] = ''.join(response.xpath('//span[contains(@class, "head_trend trSell")]//text()').extract()).strip()

				self.history.append(item['name'])

				yield item

		except Exception as e:

			print e

			pass


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


