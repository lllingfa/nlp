# -*- coding:utf-8 -*-
# !/usr/bin/python

'''''
功能：抽取指定url的页面内容中的title
'''
import json
import re
import chardet
import urllib
from lxml import etree
import xml.sax
from xml.dom.minidom import parse
import xml.etree.cElementTree as ET
# 导 minidom 的包
import xml.dom.minidom
#import lxml
from bs4 import BeautifulSoup
file_syn=open("syn_table_wiki2",'a')
file_log=open("syn_log_wiki1",'a')

def utf8_transfer(strs):
    '''''
    utf8编码转换
    '''
    try:
        if isinstance(strs, unicode):
            strs = strs.encode('utf-8')
        elif chardet.detect(strs)['encoding'] == 'GB2312':
            strs = strs.decode("gb2312", 'ignore').encode('utf-8')
        elif chardet.detect(strs)['encoding'] == 'utf-8':
            strs = strs.decode('utf-8', 'ignore').encode('utf-8')
    except Exception, e:
        print 'utf8_transfer error', strs, e
    return strs


def get_title_xpath(Html):
    '''''
    用xpath抽取网页Title,去掉百度百科
    '''
    Html = utf8_transfer(Html)
    Html_encoding = chardet.detect(Html)['encoding']
    page = etree.HTML(Html, parser=etree.HTMLParser(encoding=Html_encoding))
    title = page.xpath('/html/head/title/text()')
    try:
        #分割中文字符百度
        #title = title[0].strip(ur'_\u767e\u5ea6\u767e\u79d1')
        #分割中文字符wiki
        print title
        title = title[0].strip().split('_')[0]
        print title
    except IndexError:
        print 'Nothing'
    return title


def get_title(Html):
    '''''
    用re抽取网页Title
    '''
    Html = utf8_transfer(Html)
    compile_rule = ur'<title>.*</title>'
    title_list = re.findall(compile_rule, Html)
    if title_list == []:
        title = ''
    else:
        title = title_list[0][7:-8].split('_')[0]
    print title

def baidu_json_syn(file):
    line = file.readline()
    num = 1
    num_entity = 0
    while line:
      if(num>=21565):
        cont = json.loads(line)
        print num
        print cont
        print json.dumps(json.loads(line), ensure_ascii=False)
        # 识别title的url
        url = cont['url'].split('/item')
        print url[0]
        # 识别链接实体
        for entity in cont['desc_entities']:
            entityname = entity[0]
            url_entity = entity[-1]
            all_url_entity = url[0] + url_entity
            # 爬到别名
            url1 = all_url_entity
            try:
                html = urllib.urlopen(url1).read()
                new_html = utf8_transfer(html)

                entityname1 = get_title_xpath(new_html)
                # get_title(new_html)
                if (entityname != entityname1):
                    print entityname, entityname1
                    # 建立词典
                    dict(entityname, entityname1)
                    num_entity += 1
            except Exception, e:
                print e
      line = file.readline()
      num += 1
    print num
    log(num)

def wiki_json_syn(file):
    line = file.readline()
    num = 1
    num_entity = 0
    while line:
        cont = json.loads(line)
        print num
        print cont
        print json.dumps(json.loads(line), ensure_ascii=False)
        # 识别链接实体
        for entity in cont['desc_entities']:
            entityname = entity[0]
            url_entity = entity[-1]
            all_url_entity = url_entity
            # 爬到别名
            url1 = all_url_entity
            html = urllib.urlopen(url1).read()
            new_html = utf8_transfer(html)
            try:
                entityname1 = get_title_xpath(new_html)
                # get_title(new_html)
                if (entityname != entityname1):
                    print entityname, entityname1
                    # 建立词典
                    dict(entityname, entityname1)
                    num_entity += 1
            except Exception, e:
                print e
        line = file.readline()
        num += 1
    print num

def wiki1_json_syn(file):
    line = file.readline()
    num = 1
    num_entity = 0
    while line:
        cont = json.loads(line)
        print num
        print cont
        print json.dumps(json.loads(line), ensure_ascii=False)
        # 识别title的url
        url = cont['url'].split('/wiki')
        print url[0]
        # 识别链接实体
        for entity in cont['desc_entities']:
            entityname = entity[0]
            url_entity = entity[-1]
            all_url_entity = url[0] + url_entity
            # 爬到别名
            url1 = all_url_entity
            try:
                print 1
                html = urllib.urlopen(url1).read()
                print 1
                new_html = utf8_transfer(html)
                print 1
                entityname1 = get_title(new_html)#get_title_xpath(new_html)
                # get_title(new_html)
                if (entityname != entityname1):
                    print entityname, entityname1
                    # 建立词典
                    dict(entityname, entityname1)
                    num_entity += 1
            except Exception, e:
                print e
        line = file.readline()
        num += 1
    print num


def wiki_file_json_syn(file,file_pa):
    # get syn from local document
    line = file.readline()
    line_pa=file_pa.readline()
    num = 1
    num_pa=1
    num_syn=0
    num_entity = 0
    while line:
        cont = json.loads(line)
        #print num
        #print cont
        #print json.dumps(cont, ensure_ascii=False)
        url = cont['url']
        #print url
        # compare url from document and process the sample for synword
        cont_pa=json.loads(line_pa)
        #print num_pa
        #print cont_pa
        #print json.dumps(cont_pa,ensure_ascii=False)
        url_pa=cont_pa['url']
        #print url_pa
        # find the infobox
        while(True):
         if(url==url_pa):
            #process the cont_pa
            summary_pa=cont_pa["summary"]
            #print summary_pa
            # parse html href
            soup = BeautifulSoup(summary_pa)
            #print soup.prettify()
            #re match the title and title_href
            #entity=soup.a.string
            #print entity
            url_list = soup.findAll(name='a')
            #print url_list
            for each_url in url_list:
                #print entity
                entity_pa=each_url.get('title')
                if(entity_pa!=None):
                   #print entity_pa
                   entity=each_url.text
                   #print entity
                   if(entity!=entity_pa):
                       #print entity,entity_pa
                       if not entity_pa.endswith(u'\uff08\u9875\u9762\u4e0d\u5b58\u5728\uff09'):
                          dict(entity, entity_pa)
                          print entity, entity_pa
                          num_syn+=1
            break
         else:
             num_pa+=1
             line_pa = file_pa.readline()
             cont_pa = json.loads(line_pa)
             #print num_pa
             # print cont_pa
             #print json.dumps(cont_pa, ensure_ascii=False)
             url_pa = cont_pa['url']
             #print url_pa
        #break
        line = file.readline()
        num += 1
        log(num)
    print num_syn

def dict(entityname,entitynamesynonmy):
    #save to json
    info={'entitysyn':[entityname,entitynamesynonmy]}
    file_syn.write(str(info)+'\n')

def log(num):
    file_log.write(str(num)+'\n')
if __name__ == '__main__':
   #file=open("D:\\share\\existed_linked_entity.baidu",'r')
   #file=open("D:\\share\\exist_linked_entities.hudong",'r')
   file=open("D:\\share\\existed_linked_entities.wiki",'r')
   file_pa=open(r"D:\share\Baike_Json\New\Wiki_Dili_0412.json",'r')
   #baidu_json_syn(file)
   wiki_file_json_syn(file,file_pa)

file.close()
file_syn.close()
file_log.close()