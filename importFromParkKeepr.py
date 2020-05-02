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
parser.add_argument('-d','--data-dir',  type=str, default='.', required=True)
parser.add_argument('database',  type=str, default='partkeeprdb')

args = parser.parse_args()


# connecting to old database
import pymysql
oldDbConn = pymysql.connect(
        host=args.host,
        user=args.user,
        password=args.password,
        db=args.database
        )
oldDbCursor = oldDbConn.cursor()

def get_user(user_id):
    oldDbCursor2 = oldDbConn.cursor()
    user = None
    if user_id != None:
        nbr = oldDbCursor2.execute("SELECT `id`, `username` FROM `PartKeeprUser` WHERE id={};".format(user_id))
        if nbr != 1:
            print("Warning user_id {} is not unique !".format(user_id))
        for id,username in oldDbCursor2:
            if id == user_id:
                user,created = User.objects.get_or_create(username=username)
                if created:
                    print('user {} {} created'.format(user_id,username))
    return user

def get_image_filename(basepath,tableName,column_id_name,image_id):
    """
    Give a tuple with image filename and opened image.
    basepath        : old location folder
    tableName       : tableName in old database
    column_id_name  : name of column in old database for image id
    image_id        : image id in old database
    """

    oldDbCursor2 = oldDbConn.cursor()
    image       = None
    filename    = None
    if image_id != None:
        nbr = oldDbCursor2.execute("SELECT `id`, `{0}`, `filename`, `originalname`, `mimetype`, `extension` FROM `{1}` WHERE {0}={2};".format(
            column_id_name,
            tableName,
            image_id
            )
            )
        if nbr > 1:
            print("Warning in table {} for column {}, {} is not unique !".format(tableName,column_id_name,image_id))
        for id, column, filename, originalname, mimetype, extension in oldDbCursor2:
            if nbr > 1 :
                print(id, column, filename, mimetype, extension)
            if column == image_id:

                if extension == '':
                    extension = mimetype.split('/')[1]

                image = "{}.{}".format(os.path.join(args.data_dir,basepath,filename),extension)
                filename = originalname

    if image != None:
        image = open(image,'rb')
    return filename,image

# loading django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyPnbPartKeepr.settings")
import django
django.setup()
from django.contrib.auth.models import User
from PnbPartKeepr import models

models_list = []

###############################################################################
# User
###############################################################################

#models_list.append(User)
print("importing {} --------------------------------------------".format('PartKeeprUser'))
oldDbCursor.execute("SELECT `username`, `email` FROM `PartKeeprUser`;")
for username,email in oldDbCursor:

    user,created = User.objects.get_or_create(username=username)
    if created:
        print("Created %s"%str(user))

    user.username   = username
    user.email      = email
    user.save()


###############################################################################
# Category
###############################################################################

for table,obj in [
        ('FootprintCategory',models.FootprintCategory),
        ('PartCategory',models.PartCategory),
        ('StorageLocationCategory',models.StorageLocationCategory)
        ]:
    models_list.append(obj)
    print("importing {} --------------------------------------------".format(table))
    oldDbCursor.execute("SELECT  `id`,  `parent_id`,  `lft`,  `rgt`,  `lvl`,  `root`,  `name`,  `description`,  `categoryPath` FROM `{}`;".format(table))
    for id,parent_id,lft,rgt,lvl,root,name,description,categoryPath in oldDbCursor:
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

models_list.append(models.StorageLocationCategory)
print("importing {} --------------------------------------------".format('StorageLocation'))
oldDbCursor.execute("SELECT  `id`,  `category_id`,  `name` FROM `StorageLocation`;")
for id,category_id,name in oldDbCursor:
    category = models.StorageLocationCategory.objects.get(id=category_id)

    filename,image = get_image_filename(
            'images/storagelocation',
            'StorageLocationImage',
            'storagelocation_id', 
            id
            )

    storagelocation,created = models.StorageLocation.objects.get_or_create(id=id,category=category)
    if created:
        print("    StorageLocation id {} name {} created".format(id,name))


    storagelocation.category    = category
    storagelocation.name        = name

    storagelocation.image.delete()
    storagelocation.image = None
    if image != None:
        storagelocation.image.save(filename,image)
    storagelocation.save()


###############################################################################
# Footprint
###############################################################################

models_list.append(models.FootprintCategory)
print("importing {} --------------------------------------------".format('Footprint'))
oldDbCursor.execute("SELECT  `id`,  `category_id`,  `name`,  `description` FROM `Footprint`;")
for id,category_id,name,description in oldDbCursor:
    if category_id == None:
        category_id = 1
    category = models.FootprintCategory.objects.get(id=category_id)

    filename,image = get_image_filename(
            'images/footprint',
            'FootprintImage',
            'footprint_id',
            id
            )

    footprint,created = models.Footprint.objects.get_or_create(id=id,name=name,category=category)
    if created:
        print("Footprint id {} name {} created".format(id,name))
    footprint.name          = name
    footprint.description   = description if description != None else ''
    footprint.category      = category
    
    footprint.image.delete()
    footprint.image = None
    if image != None:
        footprint.image.save(filename,image)

    footprint.save()


###############################################################################
# Company
###############################################################################

models_list.append(models.Distributor)
print("importing {} --------------------------------------------".format('Distributor'))
oldDbCursor.execute("SELECT  `id`,  `name`,  `address`,  `url`,  `phone`,  `fax`,  `email`,  `comment`,  `skuurl`,  `enabledForReports` FROM `Distributor` ")
for id,name,address,url,phone,fax,email,comment,skuurl,enabledForReports in oldDbCursor:
    distributor,created = models.Distributor.objects.get_or_create(id=id)
    if created:
        print("    Distributor id {} name {} created".format(id,name))
    distributor.name        = name
    distributor.address     = address           if address              != None else ''
    distributor.url         = url               if url                  != None else ''
    distributor.phone       = phone             if phone                != None else ''
    distributor.fax         = fax               if fax                  != None else ''
    distributor.email       = email             if email                != None else ''
    distributor.comment     = comment           if comment              != None else ''
    distributor.skuurl      = skuurl            if skuurl               != None else ''
    distributor.forReports  = enabledForReports if enabledForReports    != None else False
    distributor.image       = None

#    distributor.image       = get_image_filename(
#            "distributor/images",
#            'DistributorImage',
#            'distributor_id',
#            id
#            )
    distributor.save()

models_list.append(models.Manufacturer)
print("importing {} --------------------------------------------".format('Manufacturer'))
oldDbCursor.execute("SELECT  `id`,  `name`,  `address`,  `url`,  `phone`,  `fax`,  `email`,  `comment` FROM `Manufacturer` ")
for id,name,address,url,phone,fax,email,comment in oldDbCursor:

    filename,image = get_image_filename(
            'images/iclogo',
            'ManufacturerICLogo',
            'manufacturer_id',
            id
            )

    manufacturer,created = models.Manufacturer.objects.get_or_create(id=id)
    if created:
        print("    Manufacturer id {} name {} created".format(id,name))

    manufacturer.name        = name
    manufacturer.address     = address           if address              != None else ''
    manufacturer.url         = url               if url                  != None else ''
    manufacturer.phone       = phone             if phone                != None else ''
    manufacturer.fax         = fax               if fax                  != None else ''
    manufacturer.email       = email             if email                != None else ''
    manufacturer.comment     = comment           if comment              != None else ''

    manufacturer.image.delete()
    manufacturer.image = None
    if image != None:
        manufacturer.image.save(filename,image)

    manufacturer.save()

###############################################################################
# Unit
###############################################################################

models_list.append(models.SiPrefix)
print("importing {} --------------------------------------------".format('SiPrefix'))
oldDbCursor.execute("SELECT  `id`,  `prefix`,  `symbol`,  `exponent`,  `base` FROM `SiPrefix` ")
for id,prefix,symbol,exponent,base in oldDbCursor:
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

models_list.append(models.Unit)
print("importing {} --------------------------------------------".format('Unit'))
oldDbCursor.execute("SELECT  `id`,  `name`,  `symbol`  FROM `Unit` ")
for id,name,symbol in oldDbCursor:
    unit,created = models.Unit.objects.get_or_create(id=id)
    if created:
        print("    Unit id {} name {} created".format(id,name))
    siprefix.name       = name
    siprefix.symbol     = symbol
    siprefix.save()

print("link {} --------------------------------------------".format('Unit/siPrefix link'))
oldDbCursor.execute("SELECT  `unit_id`,  `siprefix_id`  FROM `UnitSiPrefixes` ")
for unit_id,siprefix_id in oldDbCursor:
    unit = models.Unit.objects.get(     id=unit_id      )
    siprefix = models.SiPrefix.objects.get( id=siprefix_id  )
    unit.prefixes.add(siprefix)
    unit.save()
    
models_list.append(models.PartMeasurementUnit)
print("importing {} --------------------------------------------".format('PartUnit'))
oldDbCursor.execute("SELECT  `id`, `name`, `shortName`, `is_default`   FROM `PartUnit` ")
for id,name,shortName,is_default in oldDbCursor:
    partUnit,created = models.PartMeasurementUnit.objects.get_or_create(id=id)
    if created:
        print("    PartMeasurementUnit id {} name {} created".format(id,name))
    partUnit.name       = name
    partUnit.shortName  = shortName
    partUnit.save()

###############################################################################
# Part 
###############################################################################

models_list.append(models.PartCategory)
print("importing {} --------------------------------------------".format('Part'))
oldDbCursor.execute("SELECT  `id`,  `category_id`,  `footprint_id`,  `name`,  `description`,  `comment`,  `stockLevel`,  `minStockLevel`,  `averagePrice`,  `status`,  `needsReview`,  `partCondition`,  `createDate`,  `internalPartNumber`,  `removals`,  `lowStock`,  `partUnit_id`,  `storageLocation_id`,  `productionRemarks`,  `metaPart` FROM `Part` ;")
for id, category_id, footprint_id, name, description, comment, stockLevel, minStockLevel, averagePrice, status, needsReview, partCondition, createDate, internalPartNumber, removals, lowStock, partUnit_id, storageLocation_id, productionRemarks, metaPart in oldDbCursor:

    category        = models.PartCategory.objects.get(          id=category_id          )
    if footprint_id != None:
        footprint       = models.Footprint.objects.get(         id=footprint_id         )
    storageLocation = models.StorageLocation.objects.get(       id=storageLocation_id   )
    partUnit        = models.PartMeasurementUnit.objects.get(   id=partUnit_id          )

    timezone = pytz.timezone("UTC")
    createDateUtc = timezone.localize(createDate)

    filename,image = get_image_filename(
            'images/part',
            'PartImage',
            'part_id',
            id
            )

    if productionRemarks == None:
        productionRemarks = ''

    part,created = models.Part.objects.get_or_create(
            id=id,
            category=category,
            storageLocation=storageLocation,
            partUnit=partUnit,
            minStockLevel=minStockLevel
            )
    if created:
        print("    Part id {} name {} created".format(id,name))
    part.name               = name
    part.description        = description
    part.category           = category
    if footprint_id != None:
        part.footprint          = footprint
    part.storagelocation    = storagelocation
    part.comment            = comment               if comment              != None else ''
    part.minStockLevel      = minStockLevel
    part.averagePrice       = averagePrice
    part.status             = status                if status               != None else ''
    part.needsReview        = needsReview
    part.partCondition      = partCondition         if partCondition        != None else ''
    part.createDate         = createDateUtc
    part.internalPartNumber = internalPartNumber    if internalPartNumber   != None else ''
    part.removals           = removals
    part.partUnit           = partUnit
    part.productionRemarks  = productionRemarks     if productionRemarks    != None else ''
    part.metaPart           = metaPart

    part.image.delete()
    part.image = None
    if image != None:
        part.image.save(filename,image)


    part.save()

models_list.append(models.PartDistributor)
print("importing {} --------------------------------------------".format('partDistributor'))
oldDbCursor.execute("SELECT  `id`, `part_id`, `distributor_id`, `orderNumber`, `packagingUnit`, `price`, `sku`, `currency`, `ignoreForReports`   FROM `PartDistributor` ")
for id, part_id, distributor_id, orderNumber, packagingUnit, price, sku, currency, ignoreForReports in oldDbCursor:

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
        print("    PartDistributor id {} orderNumber {} created".format(id,orderNumber))

    forReports = True
    if ignoreForReports:
        forReports = False

    partDistributor.part            = part
    partDistributor.distributor     = distributor
    partDistributor.orderNumber     = orderNumber   if orderNumber  != None else ''
    partDistributor.packagingUnit   = packagingUnit
    partDistributor.price           = price
    partDistributor.sku             = sku           if sku          != None else ''
    partDistributor.currency        = currency
    partDistributor.forReports      = forReports
    partDistributor.save()

models_list.append(models.PartManufacturer)
print("importing {} --------------------------------------------".format('PartManufacturer'))
oldDbCursor.execute("SELECT  `id`, `part_id`, `manufacturer_id`, `partNumber` FROM `PartManufacturer` ")
for id, part_id, manufacturer_id, partNumber in oldDbCursor:

    part            = models.Part.objects.get(          id=part_id          )
    manufacturer    = models.Manufacturer.objects.get(  id=manufacturer_id  )

    partManufacturer,created = models.PartManufacturer.objects.get_or_create(
            id=id,
            part=part,
            manufacturer=manufacturer
            )
    if created:
        print("    PartManufacturer id {} partNumber {} created".format(id,partNumber))

    forReports = True
    if ignoreForReports:
        forReports = False

    partManufacturer.part            = part
    partManufacturer.manufacturer    = manufacturer
    partManufacturer.partNumber      = partNumber if partNumber != None else ''
    partManufacturer.save()

###############################################################################
# Project
###############################################################################

models_list.append(models.Project)
print("importing {} --------------------------------------------".format('Project'))
oldDbCursor.execute("SELECT  `id`, `user_id`, `name`, `description` FROM `Project` ")
for id, user_id, name, description in oldDbCursor:

    user = get_user(user_id)

    project,created = models.Project.objects.get_or_create(
            id=id,
            name=name
            )
    if created:
        print("    Project id {} name {} created".format(id,name))

    project.name        = name
    project.owner       = user
    project.description = description   if description  != None else ''
    project.save()

models_list.append(models.ProjectPart)
print("importing {} --------------------------------------------".format('ProjectPart'))
oldDbCursor.execute("SELECT  `id`, `part_id`, `project_id`, `quantity`, `remarks`, `overageType`, `overage`, `lotNumber` FROM `ProjectPart` ")
for id, part_id, project_id, quantity, remarks, overageType, overage, lotNumber in oldDbCursor:

    part    = models.Part.objects.get(      id=part_id          )
    project = models.Project.objects.get(   id=project_id  )

    projectPart,created = models.ProjectPart.objects.get_or_create(
            id=id,
            part=part,
            project=project,
            quantity=quantity
            )
    if created:
        print("    ProjectPart id {} created".format(id))

    projectPart.part       = part
    projectPart.project    = project
    projectPart.quantity   = quantity
    projectPart.remarks    = remarks        if remarks      != None else ''
    projectPart.overageType= overageType
    projectPart.overage    = overage
    projectPart.lotNumber  = lotNumber      if lotNumber    != None else ''
    projectPart.save()

models_list.append(models.ProjectRun)
print("importing {} --------------------------------------------".format('ProjectRun'))
oldDbCursor.execute("SELECT  `id`, `runDateTime`, `project_id`, `quantity` FROM `ProjectRun` ")
for id, part_id, project_id, quantity, remarks, overageType, overage, lotNumber in oldDbCursor:

    project = models.Project.objects.get(   id=project_id  )

    timezone = pytz.timezone("UTC")
    runDateTimeUtc = timezone.localize(runDateTime)

    projectRun,created = models.ProjectRun.objects.get_or_create(
            id=id,
            project=project,
            quantity=quantity
            )
    if created:
        print("    ProjectRun id {} created".format(id))

    projectRun.runDateTime= runDateTimeUtc
    projectRun.project    = project
    projectRun.quantity   = quantity
    projectRun.save()

models_list.append(models.ProjectRunPart)
print("importing {} --------------------------------------------".format('ProjectRunPart'))
oldDbCursor.execute("SELECT  `id`, `part_id`, `quantity`, `lotNumber`, `projectRun_id` FROM `ProjectRunPart` ")
for id, part_id, quantity, lotNumber, projectRun_id in oldDbCursor:

    part    = models.Part.objects.get(      id=part_id     )
    project = models.Project.objects.get(   id=project_id  )

    projectRunPart,created = models.ProjectRunPart.objects.get_or_create(
            id=id,
            projectRun=projectRun,
            quantity=quantity
            )
    if created:
        print("    ProjectRunPart id {} lotNumber {} created".format(id,lotNumber))

    projectRunPart.part        = part
    projectRunPart.projectRun  = projectRun
    projectRunPart.quantity    = quantity
    projectRunPart.lotNumber   = lotNumber      if lotNumber    != None else ''
    projectRunPart.save()

###############################################################################
# Parameter
###############################################################################

models_list.append(models.PartParameter)
print("importing {} --------------------------------------------".format('PartParameter'))
oldDbCursor.execute("SELECT  `id`, `part_id`, `unit_id`, `name`, `description`, `value`, `siPrefix_id`, `normalizedValue`, `maximumValue`, `normalizedMaxValue`, `minimumValue`, `normalizedMinValue`, `stringValue`, `valueType`, `minSiPrefix_id`, `maxSiPrefix_id`, `description` FROM `PartParameter` ")
for id, part_id, unit_id, name, description, value, siPrefix_id, normalizedValue, maximumValue, normalizedMaxValue, minimumValue, normalizedMinValue, stringValue, valueType, minSiPrefix_id, maxSiPrefix_id in oldDbCursor:

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
    partParamter.stringValue        =stringValue    if stringValue != None else ''
    partParamter.valueType          =valueType      if stringValue != None else 'string'
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

models_list.append(models.MetaPartParameterCriteria)
print("importing {} --------------------------------------------".format('MetaPartParameterCriteria'))
oldDbCursor.execute("SELECT  `id`, `part_id`, `unit_id`, `partParameterName`, `operator`, `value`, `normalizedValue`, `stringValue`, `valueType`, `siPrefix_id` FROM `MetaPartParameterCriteria` ")
for id, part_id, unit_id, partParameterName, operator, value, normalizedValue, stringValue, valueType, siPrefix_id  in oldDbCursor:

    part        = models.Part.objects.get(      id=part_id     )
    unit        = models.Unit.objects.get(      id=unit_id     )
    siPrefix    = models.SiPrefix.objects.get(  id=siPrefix_id )

    metaPartParameterCriteria,created = models.MetaPartParameterCriteria.objects.get_or_create(
            id =id,
            )
    if created:
        print("    MetaPartParameterCriteria id {} name {} created".format(id,partParameterName))

    metaPartParameterCriteria.part             =part
    metaPartParameterCriteria.unit             =unit,
    metaPartParameterCriteria.name             =partParameterName,
    metaPartParameterCriteria.operator         =operator,
    metaPartParameterCriteria.value            =value
    metaPartParameterCriteria.normalizedValue  =normalizedValue
    metaPartParameterCriteria.stringValue      =stringValue    if stringValue != None else ''
    metaPartParameterCriteria.valueType        =valueType      if stringValue != None else 'string'
    metaPartParameterCriteria.siPrefix         =siPrefix,
    metaPartParameterCriteria.save()

###############################################################################
# Stock
###############################################################################

models_list.append(models.StockEntry)
print("importing {} --------------------------------------------".format('StockEntry'))
oldDbCursor.execute("SELECT  `id`, `part_id`, `user_id`, `stockLevel`, `price`, `dateTime`, `correction`, `comment`  FROM `StockEntry` ")
for id, part_id, user_id, stockLevel, price, dateTime, correction, comment in oldDbCursor:

    part = models.Part.objects.get( id=part_id )
    user = get_user(user_id)

    stockEntry,created = models.StockEntry.objects.get_or_create(
            id=id,
            owner=user,
            part=part,
            quantity=quantity,
            )
    if created:
        print("    StockEntry id {} created".format(id))

    timezone = pytz.timezone("UTC")
    dateTimeUtc = timezone.localize(dateTime)

    stockEntry.owner        =user
    stockEntry.quantity     =quantity
    stockEntry.part         =part
    stockEntry.price        =price
    stockEntry.boughtAt     =dateTimeUtc
    stockEntry.description  =description
    stockEntry.comment      =comment if comment != None else ''
    stockEntry.save()

###############################################################################
# Attachment
###############################################################################


def setAttachment(attachment, basepath, filename,  originalname,  mimetype,  extension,  description,  createAt):

    timezone = pytz.timezone("UTC")
    createatUtc = timezone.localize(createAt)

    if extension == '':
        extension = mimetype.split('/')[1]

    filePath = "{}.{}".format(os.path.join(args.data_dir,basepath,filename),extension)

    attachment.uploadedAt   = createatUtc
    attachment.description  = description if description != None else ''

    attachment.content  = None
    attachment.content.save(originalname,open(filePath,'rb'))

models_list.append(models.ProjectAttachment)
print("importing {} --------------------------------------------".format('ProjectAttachment'))
oldDbCursor.execute("SELECT  `id`,  `project_id`,  `type`,  `filename`,  `originalname`,  `mimetype`,  `size`,  `extension`,  `description`,  `created` FROM `ProjectAttachment` ")
for id,  project_id,  type,  filename,  originalname,  mimetype,  size,  extension,  description,  createAt in oldDbCursor:

    project = models.Project.objects.get( id=project_id )

    projectAttachment,created = models.ProjectAttachment.objects.get_or_create( 
            id=id,
            project=project
            )

    if created:
        print("    ProjectAttachment id {} filename {} created".format(id,filename))

    setAttachment(
            projectAttachment,
            'files/ProjectAttachment', 
            filename,  
            originalname,  
            mimetype, 
            extension,  
            description,  
            createAt
            )

    projectAttachment.project = project
    projectAttachment.save()

models_list.append(models.PartAttachment)
print("importing {} --------------------------------------------".format('PartAttachment'))
oldDbCursor.execute("SELECT  `id`,  `part_id`,  `type`,  `filename`,  `originalname`,  `mimetype`,  `size`,  `extension`,  `description`,  `created` FROM `PartAttachment` ")
for id,  part_id,  type,  filename,  originalname,  mimetype,  size,  extension,  description,  createAt in oldDbCursor:

    part = models.Part.objects.get( id=part_id )

    partAttachment,created = models.PartAttachment.objects.get_or_create(
            id=id,
            part=part
            )

    if created:
        print("    PartAttachment id {} filename {} created".format(id,filename))

    setAttachment(
            partAttachment,
            'files/PartAttachment', 
            filename,  
            originalname,  
            mimetype, 
            extension,
            description,
            createAt
            )

    partAttachment.part = part
    partAttachment.save()

models_list.append(models.FootprintAttachment)
print("importing {} --------------------------------------------".format('FootprintAttachment'))
oldDbCursor.execute("SELECT  `id`,  `footprint_id`,  `type`,  `filename`,  `originalname`,  `mimetype`,  `size`,  `extension`,  `description`,  `created` FROM `FootprintAttachment` ")
for id,  footprint_id,  type,  filename,  originalname,  mimetype,  size,  extension,  description,  createAt in oldDbCursor:

    footprint = models.Footprint.objects.get( id=footprint_id )

    footprintAttachment,created = models.FootprintAttachment.objects.get_or_create(
            id=id,
            footprint=footprint
            )

    if created:
        print("    FootprintAttachment id {} filename {} created".format(id,filename))

    setAttachment(
            footprintAttachment,
            'files/FootprintAttachment', 
            filename,
            originalname,
            mimetype,
            extension,
            description,
            createAt
            )

    footprintAttachment.footprint = footprint
    footprintAttachment.save()


from io import StringIO

os.environ['DJANGO_COLORS'] = 'nocolor'

from django.core.management import call_command
from django.apps import apps
from django.db import connection

commands = StringIO()
djangoCursor = connection.cursor()

for app in apps.get_app_configs():
    label = app.label
    print('get sequence SQL for ',label)
    call_command('sqlsequencereset', label, stdout=commands)

djangoCursor.execute(commands.getvalue())


