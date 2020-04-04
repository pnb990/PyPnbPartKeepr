#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os

example_text = '''info: You need to have pymslq. python3-pymslq in debian like distribution.  '''

parser = argparse.ArgumentParser(
        description='Database import from old partKeeper',
        epilog=example_text,
        )
#formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('--host',           type=str, default='localhost')
parser.add_argument('-p','--port',      type=int, default='3306')
parser.add_argument('-u','--user',      type=str, default='')
parser.add_argument('-P','--password',  type=str, default='')
parser.add_argument('database',  type=str, default='partkeeprdb')

args = parser.parse_args()


# connecting to old database
import pymysql
connection = pymysql.connect(
        host=args.host,
        user=args.user,
        password=args.password,
        db=args.database
        )
cursor = connection.cursor()

# loading django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyPnbPartKeepr.settings")
import django
django.setup()
from PnbPartKeepr import models

cursor.execute("SELECT  `id`,  `name`,  LEFT(`address`, 256),  `url`,  `phone`,  `fax`,  `email`,  LEFT(`comment`, 256),  `skuurl`,  `enabledForReports` FROM `distributor` LIMIT 1000;")
for id,name,address,url,phone,fax,email,comment,skuurl,enabledForReports in cursor:
    distributor,created = models.Distributor.objects.get_or_create(id=id)
    if created:
        print("Distributor id {} name {} created".format(id,name))
    distributor.name        = name
    distributor.address     = name
    distributor.url         = url
    distributor.phone       = phone
    distributor.fax         = fax
    distributor.email       = email
    distributor.comment     = comment
    distributor.skuurl      = skuurl
    distributor.forReports  = enabledForReports
    distributor.save()

cursor.execute("SELECT  `id`,  `parent_id`,  `lft`,  `rgt`,  `lvl`,  `root`,  `name`,  LEFT(`description`, 256),  LEFT(`categoryPath`, 256) FROM `footprintcategory` LIMIT 1000;")
for id,parent_id,lft,rgt,lvl,root,name,description,categoryPath in cursor:
    category,created = models.FootprintCategory.objects.get_or_create(id=id)
    if created:
        print("category id {} name {} created".format(id,name))
    category.parent_id      = parent_id
    category.lft            = lft
    category.rght           = rgt
    category.level          = lvl
    category.tree_id        = root
    category.name           = name
    category.description    = description if description != None else ''
    category.save()

#cursor.execute("SELECT  `id`,  `category_id`,  `name`,  LEFT(`description`, 256) FROM `testdb`.`footprint` LIMIT 1000;")
#for id,category_id,name,description in cursor:
#    footprint,created = models.Footprint.objects.get_or_create(id=id)
    print("Footprint id {} name {} created".format(id,name))
#    footprint.name        = name

