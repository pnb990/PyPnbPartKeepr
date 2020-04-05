#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import pytz

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
    unit.save()
    
print("importing {} --------------------------------------------".format('partunit'))
cursor.execute("SELECT  `id`, `name`, `shortName`, `is_default`   FROM `partunit` ")
for id,name,shortName,is_default in cursor:
    partUnit,created = models.PartMeasurementUnit.objects.get_or_create(id=id)
    if created:
        print("    PartMeasurementUnit id {} name {} created".format(id,name))
    partUnit.name       = name
    partUnit.shortName  = shortName
    partUnit.save()

###############################################################################
# Part 
###############################################################################

print("importing {} --------------------------------------------".format('part'))
cursor.execute("SELECT  `id`,  `category_id`,  `footprint_id`,  `name`,  `description`,  `comment`,  `stockLevel`,  `minStockLevel`,  `averagePrice`,  `status`,  `needsReview`,  `partCondition`,  `createDate`,  `internalPartNumber`,  `removals`,  `lowStock`,  `partUnit_id`,  `storageLocation_id`,  `productionRemarks`,  `metaPart` FROM `part` ;")
for id, category_id, footprint_id, name, description, comment, stockLevel, minStockLevel, averagePrice, status, needsReview, partCondition, createDate, internalPartNumber, removals, lowStock, partUnit_id, storageLocation_id, productionRemarks, metaPart in cursor:

    category        = models.PartCategory.objects.get(          id=category_id          )
    if footprint_id != None:
        footprint       = models.Footprint.objects.get(             id=footprint_id         )
    storageLocation = models.StorageLocation.objects.get(       id=storageLocation_id   )
    partUnit        = models.PartMeasurementUnit.objects.get(   id=partUnit_id          )

    timezone = pytz.timezone("UTC")
    createDateUtc = timezone.localize(createDate)

    if productionRemarks == None:
        productionRemarks = ''

    part,created = models.Part.objects.get_or_create(
            id=id,
            category=category,
            storageLocation=storageLocation,
            partUnit=partUnit,
            minStockLevel=minStockLevel,
            productionRemarks=productionRemarks
            )
    if created:
        print("    Part id {} name {} created".format(id,name))
    part.name               = name
    part.description        = description
    part.category           = category
    if footprint_id != None:
        part.footprint          = footprint
    part.storagelocation    = storagelocation
    part.comment            = comment
    part.minStockLevel      = minStockLevel
    part.averagePrice       = averagePrice
    part.status             = status
    part.needsReview        = needsReview
    part.partCondition      = partCondition
    part.createDate         = createDateUtc
    part.internalPartNumber = internalPartNumber
    part.removals           = removals
    part.partUnit           = partUnit
    part.productionRemarks  = productionRemarks
    part.metaPart           = metaPart
    part.save()

print("importing {} --------------------------------------------".format('partdistributor'))
cursor.execute("SELECT  `id`, `part_id`, `distributor_id`, `orderNumber`, `packagingUnit`, `price`, `sku`, `currency`, `ignoreForReports`   FROM `partdistributor` ")
for id, part_id, distributor_id, orderNumber, packagingUnit, price, sku, currency, ignoreForReports in cursor:

    part        = models.Part.objects.get(          id=part_id          )
    distributor = models.Distributor.objects.get(   id=distributor_id   )

    if currency == None:
        currency = 'eur'

    partDistributor,created = models.PartDistributor.objects.get_or_create(
            id=id,
            packagingUnit=packagingUnit,
            part=part,
            distributor=distributor,
            currency=currency
            )
    if created:
        print("    PartDistributor id {} name {} created".format(id,name))

    forReports = True
    if ignoreForReports:
        forReports = False

    partDistributor.part            = part
    partDistributor.distributor     = distributor
    partDistributor.orderNumber     = orderNumber if orderNumber != '' else None
    partDistributor.packagingUnit   = packagingUnit
    partDistributor.price           = price
    partDistributor.sku             = sku if sku != '' else None
    partDistributor.currency        = currency
    partDistributor.forReports      = forReports
    partDistributor.save()

print("importing {} --------------------------------------------".format('partmanufacturer'))
cursor.execute("SELECT  `id`, `part_id`, `manufacturer_id`, `partNumber` FROM `partmanufacturer` ")
for id, part_id, manufacturer_id, partNumber in cursor:

    part            = models.Part.objects.get(          id=part_id          )
    manufacturer    = models.Manufacturer.objects.get(  id=manufacturer_id  )

    partManufacturer,created = models.PartManufacturer.objects.get_or_create(
            id=id,
            part=part,
            manufacturer=manufacturer
            )
    if created:
        print("    PartManufacturer id {} name {} created".format(id,name))

    forReports = True
    if ignoreForReports:
        forReports = False

    partManufacturer.part            = part
    partManufacturer.manufacturer    = manufacturer
    partManufacturer.partNumber      = partNumber if partNumber != '' else None
    partManufacturer.save()

###############################################################################
# Project
###############################################################################

print("importing {} --------------------------------------------".format('project'))
cursor.execute("SELECT  `id`, `user_id`, `name`, `description` FROM `project` ")
for id, user_id, name, description in cursor:

    #TODO try to import user owner PNB

    project,created = models.Project.objects.get_or_create(
            id=id,
            owner=None,
            name=name
            )
    if created:
        print("    Project id {} name {} created".format(id,name))

    project.name        = name
    project.owner       = None
    project.description = description
    project.save()

print("importing {} --------------------------------------------".format('projectpart'))
cursor.execute("SELECT  `id`, `part_id`, `project_id`, `quantity`, `remarks`, `overageType`, `overage`, `lotNumber` FROM `projectpart` ")
for id, part_id, project_id, quantity, remarks, overageType, overage, lotNumber in cursor:

    part    = models.Part.objects.get(      id=part_id          )
    project = models.Project.objects.get(   id=project_id  )

    projectPart,created = models.ProjectPart.objects.get_or_create(
            id=id,
            part=part,
            project=project,
            quantity=quantity
            )
    if created:
        print("    ProjectPart id {} name {} created".format(id,name))

    projectPart.part       = part
    projectPart.project    = project
    projectPart.quantity   = quantity
    projectPart.remarks    = remarks
    projectPart.overageType= overageType
    projectPart.overage    = overage
    projectPart.lotNumber  = lotNumber
    projectPart.save()

print("importing {} --------------------------------------------".format('projectrun'))
cursor.execute("SELECT  `id`, `runDateTime`, `project_id`, `quantity` FROM `projectrun` ")
for id, part_id, project_id, quantity, remarks, overageType, overage, lotNumber in cursor:

    project = models.Project.objects.get(   id=project_id  )

    timezone = pytz.timezone("UTC")
    runDateTimeUtc = timezone.localize(runDateTime)

    projectRun,created = models.ProjectRun.objects.get_or_create(
            id=id,
            project=project,
            quantity=quantity
            )
    if created:
        print("    ProjectRun id {} name {} created".format(id,name))

    projectRun.runDateTime= runDateTimeUtc
    projectRun.project    = project
    projectRun.quantity   = quantity
    projectRun.save()

print("importing {} --------------------------------------------".format('projectrunpart'))
cursor.execute("SELECT  `id`, `part_id`, `quantity`, `lotNumber`, `projectRun_id` FROM `projectrunpart` ")
for id, part_id, quantity, lotNumber, projectRun_id in cursor:

    part    = models.Part.objects.get(      id=part_id     )
    project = models.Project.objects.get(   id=project_id  )

    projectRunPart,created = models.ProjectRunPart.objects.get_or_create(
            id=id,
            projectRun=projectRun,
            quantity=quantity
            )
    if created:
        print("    ProjectRunPart id {} name {} created".format(id,name))

    projectRunPart.part        = part
    projectRunPart.projectRun  = projectRun
    projectRunPart.quantity    = quantity
    projectRunPart.lotNumber   = lotNumber
    projectRunPart.save()

###############################################################################
# Parameter
###############################################################################

print("importing {} --------------------------------------------".format('partparameter'))
cursor.execute("SELECT  `id`, `part_id`, `unit_id`, `name`, `description`, `value`, `siPrefix_id`, `normalizedValue`, `maximumValue`, `normalizedMaxValue`, `minimumValue`, `normalizedMinValue`, `stringValue`, `valueType`, `minSiPrefix_id`, `maxSiPrefix_id`, `description` FROM `partparameter` ")
for id, part_id, unit_id, name, description, value, siPrefix_id, normalizedValue, maximumValue, normalizedMaxValue, minimumValue, normalizedMinValue, stringValue, valueType, minSiPrefix_id, maxSiPrefix_id in cursor:

    part        = models.Part.objects.get(      id=part_id     )
    unit        = models.Unit.objects.get(      id=unit_id     )
    siPrefix    = models.SiPrefix.objects.get(  id=siPrefix_id )
    minSiPrefix = models.SiPrefix.objects.get(  id=minSiPrefix_id )
    maxSiPrefix = models.SiPrefix.objects.get(  id=maxSiPrefix_id )

    partParamter,created = models.PartParameter.objects.get_or_create(
            id          =id,
            )
    if created:
        print("    PartParameter id {} name {} created".format(id,name))

    partParamter.value              =value
    partParamter.normalizedValue    =normalizedValue
    partParamter.siPrefix           =siPrefix,
    partParamter.stringValue        =stringValue
    partParamter.valueType          =valueType
    partParamter.unit               =unit,

    partParamter.part               =part,
    partParamter.name               =name,
    partParamter.description        =description

    partParamter.minValue           =minValue
    partParamter.normalizedMinValue =normalizedMinValue
    partParamter.minSiPrefix =minSiPrefix,

    partParamter.maxValue           =minValue
    partParamter.normalizedMaxValue =normalizedMinValue
    partParamter.maxSiPrefix =minSiPrefix,

    partParamter.save()

print("importing {} --------------------------------------------".format('metapartparametercriteria'))
cursor.execute("SELECT  `id`, `part_id`, `unit_id`, `partParameterName`, `operator`, `value`, `normalizedValue`, `stringValue`, `valueType`, `siPrefix_id` FROM `metapartparametercriteria` ")
for id, part_id, unit_id, partParamterName, operator, value, normalizedValue, stringValue, valueType, siPrefix_id  in cursor:

    part        = models.Part.objects.get(      id=part_id     )
    unit        = models.Unit.objects.get(      id=unit_id     )
    siPrefix    = models.SiPrefix.objects.get(  id=siPrefix_id )

    metaPartParameterCriteria,created = models.MetaPartParameterCriteria.objects.get_or_create(
            id =id,
            )
    if created:
        print("    MetaPartParameterCriteria id {} name {} created".format(id,name))

    metaPartParameterCriteria.part             =part
    metaPartParameterCriteria.unit             =unit,
    metaPartParameterCriteria.name             =partParamterName,
    metaPartParameterCriteria.operator         =operator,
    metaPartParameterCriteria.value            =value
    metaPartParameterCriteria.normalizedValue  =normalizedValue
    metaPartParameterCriteria.stringValue      =stringValue
    metaPartParameterCriteria.valueType        =valueType
    metaPartParameterCriteria.siPrefix         =siPrefix,
    metaPartParameterCriteria.save()

