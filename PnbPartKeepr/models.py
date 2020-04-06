from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from .Currency import CURRENCY_LIST_ACRONYM 

def get_default_user_id():
    u,created = User.objects.get_or_create(username="nobody")
    if created:
        print("Created %s"%str(u))
    return u.id



###############################################################################
# Category
###############################################################################

class Category(MPTTModel):
    class Meta:
        abstract = True

    name = models.CharField(
            blank=False,
            help_text='name',
            max_length=255
            )
    parent = TreeForeignKey(
           'self',
           on_delete=models.SET_NULL,
           null=True,
           related_name='children'
           )
    description = models.TextField(
            blank=True,
            help_text='Some details'
            )
    class MPTTMeta:
        order_insertion_by = ['name']


class PartCategory(Category):
    pass

class FootprintCategory(Category):
    pass

class StorageLocationCategory(Category):
    pass

###############################################################################
# Storage
###############################################################################

class StorageLocation(models.Model):
    name = models.CharField(
            unique=True,
            blank=False,
            help_text='name',
            max_length=255
            )
    image = models.ImageField(
            upload_to='stockLocation/images/%Y/%m/%d/', 
            null=True,
            help_text='Image'
            )
    category = models.ForeignKey(
            StorageLocationCategory, 
            on_delete=models.PROTECT, 
            help_text='Category'
            )


###############################################################################
# Footprint
###############################################################################

class Footprint(models.Model):
    name = models.CharField(
            unique=True,
            blank=False,
            help_text='name',
            max_length=255
            )
    description = models.TextField(
            blank=True,
            help_text='Some details'
            )
    category = models.ForeignKey(
            FootprintCategory, 
            on_delete=models.PROTECT, 
            help_text='Category'
            )
    image = models.ImageField(
            upload_to='footprint/images/%Y/%m/%d/', 
            null=True,
            help_text='Image'
            )

###############################################################################
# Company
###############################################################################

class Company(models.Model):
    class Meta:
        abstract = True

    UPLOAD_TO=None

    name = models.CharField(
            unique=True,
            blank=False,
            help_text='name',
            max_length=255
            )
    address = models.TextField(
            blank=True,
            help_text='Postal address'
            )
    url = models.URLField(
            null=True,
            help_text='Web site url'
            )
    phone = PhoneField(
            null=True,
            help_text='Contact phone number'
            )
    fax = PhoneField(
            null=True,
            help_text='Contact fax number'
            )
    email = models.EmailField(
            null=True,
            help_text='Contact fax number'
            )
    comment = models.TextField(
            blank=True,
            help_text='Comment'
            )
    image = models.ImageField(
            upload_to=UPLOAD_TO, 
            null=True,
            help_text='Image'
            )

class Distributor(Company):
    UPLOAD_TO = 'distributor/images/%Y/%m/%d/'
    skuUrl = models.URLField(
            blank=True,
            help_text='SKU URL'
            )
    forReports = models.BooleanField(
            blank=False,
            default=True,
            help_text='Use this one for pricing calculation'
            )

class Manufacturer(models.Model):
    UPLOAD_TO = 'manufacturer/images/%Y/%m/%d/'

###############################################################################
# Unit
###############################################################################

class SiPrefix(models.Model):
    prefix = models.CharField(
            help_text='System International prefix name (e.g. yotta, deca, deci, centi)',
            max_length=255
            )
    symbol = models.CharField(
            help_text='Symbol of System International prefix (e.g. m, M, G)',
            max_length=255
            )
    exponent = models.IntegerField(
            help_text='The exponent of the System International prefix (e.g. milli = 10^-3)'
            )
    base = models.IntegerField(
            help_text='The base of the System International (e.g. 2^-3)'
            )

    """
    Calculates the product for a given value.
    @param $value float The value to calculate the product
    @return float The resulting value
    """
    def calculateProduct(value):
        return value * self.base**self.exponent

class Unit(models.Model):
    name = models.CharField(
            help_text='The name of the unit (e.g. Volts, Ampere, Farad, Metres)',
            max_length=255
            )
    symbol = models.CharField(
            help_text='The symbol of the unit (e.g. V, A, F, m)',
            max_length=255
            )
    prefixes = models.ManyToManyField(SiPrefix,
             help_text='Defines the allowed System International prefix for this parameter unit'
             )

class PartMeasurementUnit(models.Model):
    name = models.CharField(
            help_text='name',
            max_length=255
            )

    shortName = models.CharField(
            help_text='Short name',
            max_length=16
            )


###############################################################################
# Part 
###############################################################################

class Part(models.Model):
    name = models.CharField(
            blank=False,
            help_text='name',
            max_length=255
            )
    description = models.TextField(
            blank=True,
            help_text='Some details'
            )
    category = models.ForeignKey(
            PartCategory, 
            on_delete=models.PROTECT, 
            help_text='Category'
            )
    image = models.ImageField(
            upload_to='footprint/images/%Y/%m/%d/', 
            null=True,
            help_text='Image'
            )
    footprint = models.ForeignKey(
            Footprint, 
            on_delete=models.PROTECT, 
            null=True,
            help_text='footprint'
            )
    storageLocation = models.ForeignKey(
            StorageLocation, 
            on_delete=models.PROTECT, 
            help_text='Storage location'
            )
    comment = models.TextField(
            blank=True,
            help_text='Some comments'
            )

    minStockLevel = models.PositiveIntegerField(
            help_text='Number minimum of part in stock allowed'
            )

    averagePrice = models.DecimalField(
            max_digits=13,
            decimal_places=4,
            null=True,
            help_text='General average part\'s price'
            )
    status = models.CharField(
            null=True,
            help_text='a status ... may be active/end of life/development ???',
            max_length=255
            )
    needsReview = models.BooleanField(
            default=True,
            help_text='Use this one for pricing calculation'
            )
    partCondition = models.CharField(
            null=True,
            help_text='I don\' know...',
            max_length=255
            )
    createDate = models.DateTimeField(
            default=timezone.now
            )
    internalPartNumber = models.CharField(
            blank=True,
            help_text='part number used in internal data base',
            max_length=255
            )
    removals = models.BooleanField(
            default=False,
            help_text='Need to be removed ?'
            )
    partUnit = models.ForeignKey(
            PartMeasurementUnit, 
            on_delete=models.CASCADE, 
            null=True,
            help_text=''
            )

    productionRemarks = models.CharField(
            blank=True,
            help_text='Remarks done by production',
            max_length=255
            )
    metaPart = models.BooleanField(
            default=False,
            help_text='is a meta part ?'
            )

class PartDistributor(models.Model):
    part = models.ForeignKey(
            Part, 
            on_delete=models.CASCADE, 
            help_text='part'
            )
    distributor = models.ForeignKey(
            Distributor, 
            on_delete=models.CASCADE, 
            help_text='Distributor'
            )
    orderNumber = models.CharField(
            unique=True,
            null=True,
            help_text='name',
            max_length=255
            )
    packagingUnit = models.PositiveIntegerField(
            help_text='Part quantity per package'
            )
    price = models.DecimalField(
            max_digits=13,
            decimal_places=4,
            null=True,
            help_text='Price per part'
            )
    currency = models.CharField(
            blank=False,
            help_text='Money system',
            max_length=3,
            choices=CURRENCY_LIST_ACRONYM
            )
    sku = models.CharField(
            unique=True,
            null=True,
            help_text='Stock keeping unit',
            max_length=255
            )
    forReports = models.BooleanField(
            blank=False,
            default=True,
            help_text='Use this one for pricing calculation'
            )

class PartManufacturer(models.Model):
    part = models.ForeignKey(
            Part, 
            on_delete=models.CASCADE, 
            help_text='part'
            )
    manufacturer = models.ForeignKey(
            Manufacturer, 
            on_delete=models.CASCADE, 
            help_text='Manufacturer'
            )
    partNumber = models.CharField(
            unique=True,
            null=True,
            help_text='name',
            max_length=255
            )


###############################################################################
# Project
###############################################################################


class Project(models.Model):

    name = models.CharField(
            help_text='name',
            max_length=255
            )

    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='+',
            null=True,
            on_delete=models.SET_NULL,
            default=get_default_user_id
            )

    description = models.CharField(
            blank=True,
            help_text='description',
            max_length=255
            )

class ProjectPart(models.Model): 

    # TODO check utility PNB
    OVERAGE_TYPE_ABSOLUTE = "absolute";
    OVERAGE_TYPE_PERCENT = "percent";
    OVERAGE_TYPE_CHOICES = [
            (OVERAGE_TYPE_ABSOLUTE, 'absolute'),
            (OVERAGE_TYPE_PERCENT,  'percent' )
            ]

    part = models.ForeignKey(
            Part, 
            blank=False,
            on_delete=models.PROTECT, 
            help_text='part'
            )

    quantity = models.PositiveIntegerField(
            help_text='Part quantity inside'
            )
            
    project = models.ForeignKey(
            Project, 
            on_delete=models.CASCADE, 
            help_text='project'
            )

    remarks = models.CharField(
            blank=True,
            help_text='Remarks',
            max_length=255
            )

    overageType = models.CharField(
            blank=False,
            help_text='The type of the value',
            max_length=10,
            choices=OVERAGE_TYPE_CHOICES
            )

    overage = models.PositiveIntegerField(
            default=0,
            help_text='the overage can either be percent or an absolute value depending on overageType.'
            )

    lotNumber = models.CharField(
            blank=True,
            help_text='the lot number',
            max_length=10
            )

    # TODO Kept but i don't know what it is. PNB
    totalQuantity = models.PositiveIntegerField(
            default=0,
            help_text='The total quantity including overage',
            )


class ProjectRun(models.Model):

    runDateTime = models.DateTimeField(
            default=timezone.now
            )

    project = models.ForeignKey(
            Project, 
            on_delete=models.CASCADE, 
            help_text='project'
            )

    quantity = models.PositiveIntegerField(
            default=0,
            help_text='The quantity project has been build',
            )


class ProjectRunPart(models.Model):

    projectRun = models.ForeignKey(
            ProjectRun, 
            on_delete=models.CASCADE, 
            help_text='project run'
            )

    part = models.ForeignKey(
            Part, 
            on_delete=models.PROTECT, 
            help_text='the part used in a production run'
            )

    quantity = models.PositiveIntegerField(
            help_text='the quantity of a production run'
            )

    lotNumber = models.CharField(
            blank=True,
            help_text='the lot number use in production',
            max_length=10
            )

###############################################################################
# Parameter
###############################################################################

class Parameter(models.Model):
    class Meta:
        abstract = True

    TYPE_NUMERIC    = 'numeric'
    TYPE_STRING     = 'string'
    TYPE_CHOICES = (
        (TYPE_NUMERIC   , 'numeric' ),
        (TYPE_STRING    , 'string'  ),
    )
    
    value   = models.FloatField(
            help_text='value'
            )

    normalizedValue = models.FloatField(
            null=True,
            help_text="normalized value"
            )

    siPrefix = models.ForeignKey(
            SiPrefix,
            related_name='+',
            on_delete=models.PROTECT,
            help_text='The SiPrefix of the unit'
            )

    stringValue = models.CharField(
            null=True,
            help_text='Value in case of string',
            max_length=255
            )

    valueType = models.CharField(
            null=True,
            help_text='The type of the value',
            max_length=10,
            choices=TYPE_CHOICES
            )

    unit = models.ForeignKey(
            Unit,
            null=True,
            on_delete=models.CASCADE, 
            help_text="The unit for this type. May be null"
            )




class PartParameter(models.Model):
    part = models.ForeignKey(
            Part, 
            on_delete=models.CASCADE, 
            help_text='parameter criteria ???'
            )

    name = models.CharField(
            help_text='name',
            max_length=255
            )

    description = models.CharField(
            help_text='description',
            max_length=255
            )

    minValue   = models.FloatField(
            help_text='minimum value'
            )

    normalizedMinValue = models.FloatField(
            null=True,
            help_text="normalized minimum value"
            )

    minSiPrefix = models.ForeignKey(
            SiPrefix,
            related_name='+',
            on_delete=models.PROTECT,
            help_text='The SiPrefix of the unit for minimum value'
            )

    maxValue   = models.FloatField(
            help_text='maximum value'
            )

    normalizedMaxValue = models.FloatField(
            null=True,
            help_text="normalized maximum value"
            )

    maxSiPrefix = models.ForeignKey(
            SiPrefix,
            related_name='+',
            on_delete=models.PROTECT,
            help_text='The SiPrefix of the unit for maximum value'
            )



class MetaPartParameterCriteria(Parameter):

    TYPE_NUMERIC    = 'numeric'
    TYPE_STRING     = 'string'
    TYPE_CHOICES = (
        (TYPE_NUMERIC   , 'numeric' ),
        (TYPE_STRING    , 'string'  ),
    )
    
    part = models.ForeignKey(
            Part, 
            on_delete=models.CASCADE, 
            help_text='parameter criteria ???'
            )
    name = models.CharField(
            help_text='name',
            max_length=255
            )
    operator = models.CharField(
            help_text='operator ???',
            max_length=255
            )


###############################################################################
# Stock
###############################################################################

class StockEntry(models.Model):
    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='+',
            null=True,
            on_delete=models.SET_NULL,
            default=get_default_user_id
            )
    quantity = models.PositiveIntegerField(
            help_text='Part quantity inside'
            )
    part = models.ForeignKey(
            Part, 
            on_delete=models.PROTECT, 
            help_text='part'
            )
    price = models.DecimalField(
            max_digits=13,
            decimal_places=4,
            null=True,
            help_text='Bought stock price per part'
            )
    boughtAt = models.DateTimeField(
            default=timezone.now
            )
    comment = models.TextField(
            blank=True,
            help_text='Comment'
            )


###############################################################################
# Attachment
###############################################################################
class Attachment(models.Model):
    class Meta:
        abstract = True

    UPLOAD_TO = None
    filename = models.CharField(
            help_text='original filename',
            max_length=255
            )
    uploadedAt = models.DateTimeField(
            auto_now_add=True,
            help_text='Upload date of filename',
            )
    description = models.TextField(
            blank=True,
            help_text='Some details'
            )
    content = models.FileField(upload_to=UPLOAD_TO,
            null=False,
            blank=False,
            help_text='Footprint attachment content'
            )

class ProjectAttachment(Attachment):
    UPLOAD_TO = 'project/attachments/%Y/%m/%d/' 

    project = models.ForeignKey(
            Project, 
            on_delete=models.CASCADE, 
            help_text='project'
            )


class PartAttachment(Attachment):
    UPLOAD_TO = 'part/attachments/%Y/%m/%d/' 

    part = models.ForeignKey(
            Part, 
            on_delete=models.CASCADE, 
            help_text='footprint'
            )

class FootprintAttachment(Attachment):
    UPLOAD_TO = 'footprint/attachments/%Y/%m/%d/' 

    footprint = models.ForeignKey(
            Footprint, 
            on_delete=models.CASCADE, 
            help_text='footprint'
            )


