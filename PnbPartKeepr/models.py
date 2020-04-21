import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from phone_field import PhoneField
from mptt.models import MPTTModel, TreeForeignKey
from .Currency import CURRENCY_LIST_ACRONYM

def get_default_user_id():
    u,created = User.objects.get_or_create(username="nobody")
    if created:
        print("Created %s"%str(u))
    return u.id

class ReverseUrlMixin(object):
    def get_name_url(self,action='detail'):
        return 'pnbpartkeepr.{}.{}'.format(self.__class__.__name__.lower(),action)

    def get_name_update_url(self):
        return self.get_name_url('update')

    def get_name_delete_url(self):
        return self.get_name_url('delete')

    def get_absolute_url(self,action='detail'):
        return reverse(self.get_name_url(action), args=[str(self.id)])

    def get_absolute_update_url(self):
        return self.get_absolute_url('update')

    def get_absolute_delete_url(self):
        return self.get_absolute_url('delete')



###############################################################################
# Category
###############################################################################

class Category(ReverseUrlMixin,MPTTModel):
    class Meta:
        abstract = True

    name = models.CharField(
            help_text='name',
            max_length=255
            )
    parent = TreeForeignKey(
           'self',
           on_delete=models.SET_NULL,
           null=True,
           blank=True,
           related_name='children'
           )
    description = models.TextField(
            blank=True,
            default='',
            help_text='Some details'
            )
    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return  self.name

    def path(self,sep=' > ',name = None):
        s = self.name
        if self.parent != None:
            s = self.parent.path()+sep+s
        if name != None:
            s = s+sep+name
        return s


class PartCategory(Category):
    @staticmethod
    def get_object_name():
        return "part category"

class FootprintCategory(Category):
    @staticmethod
    def get_object_name():
        return "part category"

class StorageLocationCategory(Category):
    @staticmethod
    def get_object_name():
        return "part category"


###############################################################################
# Storage
###############################################################################

class StorageLocation(ReverseUrlMixin,models.Model):
    name = models.CharField(
            unique=True,
            help_text='name',
            max_length=255
            )
    image = models.ImageField(
            upload_to='stockLocation/images/%Y/%m/%d/',
            null=True,
            blank=True,
            help_text='Image'
            )
    category = TreeForeignKey(
            StorageLocationCategory,
            on_delete=models.PROTECT,
            help_text='Category'
            )

    @staticmethod
    def get_object_name():
        return "storage location"

    def __str__(self):
        return self.category.path(name=self.name)


###############################################################################
# Footprint
###############################################################################

class Footprint(ReverseUrlMixin,models.Model):
    name = models.CharField(
            unique=True,
            help_text='name',
            max_length=255
            )
    description = models.TextField(
            blank=True,
            default='',
            help_text='Some details'
            )
    category = TreeForeignKey(
            FootprintCategory,
            on_delete=models.PROTECT,
            help_text='Category'
            )
    image = models.ImageField(
            upload_to='footprint/images/%Y/%m/%d/',
            null=True,
            blank=True,
            help_text='Image'
            )

    @staticmethod
    def get_object_name():
        return "footprint"

    def __str__(self):
        return self.name

    def get_addattachment_url(self):
        return reverse('pnbpartkeepr.footprintattachment.create', args=[str(self.id)])


###############################################################################
# Company
###############################################################################

class Company(ReverseUrlMixin,models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
            unique=True,
            help_text='name',
            max_length=255
            )
    address = models.TextField(
            blank=True,
            default='',
            help_text='Postal address'
            )
    url = models.URLField(
            blank=True,
            help_text='Web site url'
            )
    phone = PhoneField(
            blank=True,
            default='',
            help_text='Contact phone number'
            )
    fax = PhoneField(
            blank=True,
            default='',
            help_text='Contact fax number'
            )
    email = models.EmailField(
            blank=True,
            default='',
            help_text='Contact fax number'
            )
    comment = models.TextField(
            blank=True,
            default='',
            help_text='Comment'
            )

    def __str__(self):
        return self.name


class Distributor(Company):

    image = models.ImageField(
            upload_to='distributor/images/%Y/%m/%d/',
            null=True,
            blank=True,
            help_text='Image'
            )
    skuUrl = models.URLField(
            blank=True,
            default='',
            help_text='SKU URL'
            )
    forReports = models.BooleanField(
            blank=False,
            default=True,
            help_text='Use this one for pricing calculation'
            )

    @staticmethod
    def get_object_name():
        return "distributor"


class Manufacturer(Company):
    image = models.ImageField(
            upload_to='manufacturer/images/%Y/%m/%d/',
            null=True,
            blank=True,
            help_text='Image'
            )

    @staticmethod
    def get_object_name():
        return "manufacturer"


###############################################################################
# Unit
###############################################################################

class SiPrefix(ReverseUrlMixin,models.Model):
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


class Unit(ReverseUrlMixin,models.Model):
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

class PartMeasurementUnit(ReverseUrlMixin,models.Model):
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

class Part(ReverseUrlMixin,models.Model):
    name = models.CharField(
            help_text='name',
            max_length=255
            )
    description = models.TextField(
            blank=True,
            default='',
            help_text='Some details'
            )
    category = TreeForeignKey(
            PartCategory,
            on_delete=models.PROTECT,
            help_text='Category'
            )
    image = models.ImageField(
            upload_to='footprint/images/%Y/%m/%d/',
            null=True,
            blank=True,
            help_text='Image'
            )
    footprint = models.ForeignKey(
            Footprint,
            on_delete=models.PROTECT,
            null=True,
            blank=True,
            help_text='footprint'
            )
    storageLocation = models.ForeignKey(
            StorageLocation,
            on_delete=models.PROTECT,
            help_text='Storage location'
            )
    comment = models.TextField(
            blank=True,
            default='',
            help_text='Some comments'
            )

    minStockLevel = models.PositiveIntegerField(
            help_text='Number minimum of part in stock allowed'
            )

    averagePrice = models.DecimalField(
            max_digits=13,
            decimal_places=4,
            null=True,
            blank=True,
            help_text='General average part\'s price'
            )
    status = models.CharField(
            blank=True,
            default='',
            help_text='a status ... may be active/end of life/development ???',
            max_length=255
            )
    needsReview = models.BooleanField(
            default=True,
            help_text='Use this one for pricing calculation'
            )
    partCondition = models.CharField(
            blank=True,
            default='',
            help_text='I don\' know...',
            max_length=255
            )
    createDate = models.DateTimeField(
            default=timezone.now
            )
    internalPartNumber = models.CharField(
            blank=True,
            default='',
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
            blank=True,
            help_text=''
            )

    productionRemarks = models.CharField(
            blank=True,
            default='',
            help_text='Remarks done by production',
            max_length=255
            )
    metaPart = models.BooleanField(
            default=False,
            help_text='is a meta part ?'
            )

    def stockLevel(self):
        #TODO review to optimise this request with https://docs.djangoproject.com/fr/3.0/topics/db/aggregation/
        return sum([i.quantity for i in self.stockentry_set.all()])

    def __str__(self):
        if self.footprint:
            return "{} / {}".format(self.name,self.footprint.name)
        return self.name

    @staticmethod
    def get_object_name():
        return "part"


class PartDistributor(ReverseUrlMixin,models.Model):
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
    orderNumber = models.CharField( # not unique 2 distributor may have same part number
            blank=True,
            help_text='name',
            max_length=255,
            default=''
            )
    packagingUnit = models.PositiveIntegerField(
            help_text='Part quantity per package'
            )
    price = models.DecimalField(
            max_digits=13,
            decimal_places=4,
            null=True,
            blank=True,
            help_text='Price per part'
            )
    currency = models.CharField(
            help_text='Money system',
            max_length=3,
            choices=CURRENCY_LIST_ACRONYM
            )
    sku = models.CharField( # not unique 2 distributor may have same part number
            blank=True,
            default='',
            help_text='Stock keeping unit',
            max_length=255
            )
    forReports = models.BooleanField(
            default=True,
            help_text='Use this one for pricing calculation'
            )

class PartManufacturer(ReverseUrlMixin,models.Model):
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
    partNumber = models.CharField( # not unique 2 Manufacturer may have same part number
            blank=True,
            default='',
            help_text='name',
            max_length=255
            )


###############################################################################
# Project
###############################################################################

class Project(ReverseUrlMixin,models.Model):

    name = models.CharField(
            help_text='name',
            max_length=255
            )

    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='+',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            default=get_default_user_id
            )

    description = models.CharField(
            blank=True,
            default='',
            help_text='description',
            max_length=255
            )

    @staticmethod
    def get_object_name():
        return "project"

    def get_addattachment_url(self):
        return reverse('pnbpartkeepr.projectattachment.create', args=[str(self.id)])


class ProjectPart(ReverseUrlMixin,models.Model):

    # TODO check utility PNB
    OVERAGE_TYPE_ABSOLUTE = "absolute";
    OVERAGE_TYPE_PERCENT = "percent";
    OVERAGE_TYPE_CHOICES = [
            (OVERAGE_TYPE_ABSOLUTE, 'absolute'),
            (OVERAGE_TYPE_PERCENT,  'percent' )
            ]

    part = models.ForeignKey(
            Part,
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
            default='',
            help_text='Remarks',
            max_length=255
            )

    overageType = models.CharField(
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
            default='',
            help_text='the lot number',
            max_length=10
            )

    # TODO Kept but i don't know what it is. PNB
    totalQuantity = models.PositiveIntegerField(
            default=0,
            help_text='The total quantity including overage',
            )


class ProjectRun(ReverseUrlMixin,models.Model):

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

    @staticmethod
    def get_object_name():
        return "project run"


class ProjectRunPart(ReverseUrlMixin,models.Model):

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
            default='',
            help_text='the lot number use in production',
            max_length=10
            )

###############################################################################
# Parameter
###############################################################################

class Parameter(ReverseUrlMixin,models.Model):
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
            blank=True,
            default='',
            help_text='Value in case of string',
            max_length=255
            )

    valueType = models.CharField(
            help_text='The type of the value',
            max_length=10,
            choices=TYPE_CHOICES
            )

    unit = models.ForeignKey(
            Unit,
            null=True,
            blank=True,
            on_delete=models.CASCADE,
            help_text="The unit for this type. May be null"
            )




class PartParameter(ReverseUrlMixin,models.Model):
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

class StockEntry(ReverseUrlMixin,models.Model):
    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='+',
            null=True,
            blank=True,
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
            default='',
            help_text='Comment'
            )


###############################################################################
# Attachment
###############################################################################
# TODO see if it is usefull or not  PolymorphicModel https://github.com/bconstantin/django_polymorphic
class Attachment(ReverseUrlMixin,models.Model):
    class Meta:
        abstract = True

    uploadedAt = models.DateTimeField(
            auto_now = True,
            help_text='Upload date of filename',
            )
    description = models.TextField(
            blank=True,
            default='',
            help_text='Some details'
            )

    def save(self, *args, **kwargs):
        #TODO find a way to update update time if self.content has changed.
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def filename(self):
        return os.path.basename(self.content.name)

class ProjectAttachment(Attachment):
    content = models.FileField(upload_to='project/attachments/%Y/%m/%d/',
            help_text='Project attachment file'
            )

    project = models.ForeignKey(
            Project,
            on_delete=models.CASCADE,
            help_text='project'
            )

    def __str__(self):
        return "{} file of project {}".format(self.filename(),self.project)

    @staticmethod
    def get_object_name():
        return "project attachment"

    def get_success_url(self):
        return self.project.get_absolute_url()


class PartAttachment(Attachment):
    content = models.FileField(upload_to='part/attachments/%Y/%m/%d/',
            help_text='Part attachment file'
            )

    part = models.ForeignKey(
            Part,
            on_delete=models.CASCADE,
            help_text='footprint'
            )

    def __str__(self):
        return "'{}' file of part '{}'".format(self.filename(),self.part)

    @staticmethod
    def get_object_name():
        return "part attachment"

    def get_success_url(self):
        return self.part.get_absolute_url()


class FootprintAttachment(Attachment):
    content = models.FileField(upload_to='footprint/attachments/%Y/%m/%d/',
            help_text='Footprint attachment file'
            )

    footprint = models.ForeignKey(
            Footprint,
            on_delete=models.CASCADE,
            help_text='footprint'
            )

    def get_success_url(self):
        return self.footprint.get_absolute_url()

    def __str__(self):
        return "'{}' file of footprint '{}'".format(self.filename(),self.footprint)

    @staticmethod
    def get_object_name():
        return "footprint attachment"


