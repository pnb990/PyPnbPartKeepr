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


###############################################################################
# Category
###############################################################################

for table,obj in [
        ('footprintcategory',models.FootprintCategory),
        ('partcategory',models.PartCategory),
        ('storagelocationcategory',models.StorageLocationCategory)
        ]:
    print("importing {} --------------------------------------------".format(table))
    cursor.execute("SELECT  `id`,  `parent_id`,  `lft`,  `rgt`,  `lvl`,  `root`,  `name`,  `description`,  `categoryPath` FROM `{}`;".format(table))
    for id,parent_id,lft,rgt,lvl,root,name,description,categoryPath in cursor:
        category,created = obj.objects.get_or_create(id=id)
        if created:
            print("    {} id {} name {} created".format(table,id,name))
        category.parent_id      = parent_id
        category.lft            = lft
        category.rght           = rgt
        category.level          = lvl
        category.tree_id        = root
        category.name           = name
        category.description    = description if description != None else ''
        category.save()

###############################################################################
# StorageLocation
###############################################################################

print("importing {} --------------------------------------------".format('storagelocation'))
cursor.execute("SELECT  `id`,  `category_id`,  `name` FROM `storagelocation`;")
for id,category_id,name in cursor:
    category = models.StorageLocationCategory.objects.get(id=category_id)

    storagelocation,created = models.StorageLocation.objects.get_or_create(id=id,category=category)
    if created:
        print("    StorageLocation id {} name {} created".format(id,name))
    storagelocation.category    = category
    storagelocation.name        = name
    storagelocation.save()


###############################################################################
# Footprint
###############################################################################

print("importing {} --------------------------------------------".format('footprint'))
cursor.execute("SELECT  `id`,  `category_id`,  `name`,  `description` FROM `footprint`;")
for id,category_id,name,description in cursor:
    if category_id == None:
        category_id = 1
    category = models.FootprintCategory.objects.get(id=category_id)
    footprint,created = models.Footprint.objects.get_or_create(id=id,name=name,category=category)
    if created:
        print("Footprint id {} name {} created".format(id,name))
    footprint.name          = name
    footprint.description   = description
    footprint.category      = category


###############################################################################
# Company
###############################################################################

print("importing {} --------------------------------------------".format('distributor'))
cursor.execute("SELECT  `id`,  `name`,  `address`,  `url`,  `phone`,  `fax`,  `email`,  `comment`,  `skuurl`,  `enabledForReports` FROM `distributor` ")
for id,name,address,url,phone,fax,email,comment,skuurl,enabledForReports in cursor:
    distributor,created = models.Distributor.objects.get_or_create(id=id)
    if created:
        print("    Distributor id {} name {} created".format(id,name))
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

print("importing {} --------------------------------------------".format('manufacturer'))
cursor.execute("SELECT  `id`,  `name`,  `address`,  `url`,  `phone`,  `fax`,  `email`,  `comment` FROM `manufacturer` ")
for id,name,address,url,phone,fax,email,comment in cursor:
    manufacturer,created = models.Manufacturer.objects.get_or_create(id=id)
    if created:
        print("    Manufacturer id {} name {} created".format(id,name))
    manufacturer.name        = name
    manufacturer.address     = name
    manufacturer.url         = url
    manufacturer.phone       = phone
    manufacturer.fax         = fax
    manufacturer.email       = email
    manufacturer.comment     = comment
    manufacturer.save()

###############################################################################
# Unit
###############################################################################

print("importing {} --------------------------------------------".format('siPrefix'))
cursor.execute("SELECT  `id`,  `prefix`,  `symbol`,  `exponent`,  `base` FROM `siprefix` ")
for id,prefix,symbol,exponent,base in cursor:
    siprefix,created = models.SiPrefix.objects.get_or_create(
            id=id,
            exponent=exponent,
            base=base
            )
    if created:
        print("    SiPrefix id {} siprefix {} {} created".format(id,prefix,symbol))
    siprefix.prefix     = prefix
    siprefix.symbol     = symbol
    siprefix.exponent   = exponent
    siprefix.base       = base
    siprefix.save()

print("importing {} --------------------------------------------".format('unit'))
cursor.execute("SELECT  `id`,  `name`,  `symbol`  FROM `unit` ")
for id,name,symbol in cursor:
    unit,created = models.Unit.objects.get_or_create(id=id)
    if created:
        print("    Unit id {} name {} created".format(id,name))
    siprefix.name       = name
    siprefix.symbol     = symbol
    siprefix.save()

print("importing {} --------------------------------------------".format('unit/siPrefix link'))
cursor.execute("SELECT  `unit_id`,  `siprefix_id`  FROM `unitsiprefixes` ")
for unit_id,siprefix_id in cursor:
    unit = models.Unit.objects.get(     id=unit_id      )
    siprefix = models.SiPrefix.objects.get( id=siprefix_id  )
    unit.prefixes.add(siprefix)
    

###############################################################################
# Part 
###############################################################################

print("importing {} --------------------------------------------".format('part'))
cursor.execute("SELECT  `id`,  `category_id`,  `footprint_id`,  `name`,  `description`,  `comment`,  `stockLevel`,  `minStockLevel`,  `averagePrice`,  `status`,  `needsReview`,  `partCondition`,  `createDate`,  `internalPartNumber`,  `removals`,  `lowStock`,  `partUnit_id`,  `storageLocation_id`,  `productionRemarks`,  `metaPart` FROM `part` ;")
for id, name, category_id, footprint_id, name, description, comment, stockLevel, minStockLevel, averagePrice, status, needsReview, partCondition, createDate, internalPartNumber, removals, lowStock, partUnit_id, storageLocation_id, productionRemarks, metaPart in cursor:

    category        = models.PartCategory.objects.get(      id=category_id          )
    footprint       = models.Footprint.objects.get(         id=footprint_id         )
    storagelocation = models.StorageLocation.objects.get(   id=storageLocation_id   )

    part,created = models.Manufacturer.objects.get_or_create(
            id=id,
            category=category,
            footprint=footprint
            )
    if created:
        print("    Part id {} name {} created".format(id,name))
    part.name               = name
    part.description        = description
    part.category           = category
    part.footprint          = footprint
    part.storagelocation    = storagelocation
    part.comment            = comment
    part.save()


