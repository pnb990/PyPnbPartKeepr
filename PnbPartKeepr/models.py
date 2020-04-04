from django.conf import settings
from django.db import models
from phone_field import PhoneField
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone

def get_default_user_id():
    u,created = User.objects.get_or_create(username="inconnu")
    if created:
        print("Created %s"%str(u))
    return u.id

###############################################################################
# Category
###############################################################################

class Category(MPTTModel):
    name = models.CharField(
            unique=True,
            blank=False,
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
            help_text='Some details'
            )
    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        abstract = True


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
            blank=True,
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
            blank=True,
            help_text='Image'
            )

###############################################################################
# Company
###############################################################################

class Company(models.Model):
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
            blank=True,
            help_text='Web site url'
            )
    phone = PhoneField(
            blank=True,
            help_text='Contact phone number'
            )
    fax = PhoneField(
            blank=True,
            help_text='Contact fax number'
            )
    email = models.EmailField(
            blank=True,
            help_text='Contact fax number'
            )
    comment = models.TextField(
            blank=True,
            help_text='Comment'
            )
    image = models.ImageField(
            upload_to=UPLOAD_TO, 
            null=True,
            blank=True,
            help_text='Image'
            )
    class Meta:
        abstract = True

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
# Part 
###############################################################################

class Part(models.Model):
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
            PartCategory, 
            on_delete=models.PROTECT, 
            help_text='Category'
            )
    image = models.ImageField(
            upload_to='footprint/images/%Y/%m/%d/', 
            blank=True,
            help_text='Image'
            )
    footprint = models.ForeignKey(
            Footprint, 
            on_delete=models.PROTECT, 
            blank=True,
            help_text='footprint'
            )
    storageLocation = models.ForeignKey(
            StorageLocation, 
            on_delete=models.PROTECT, 
            blank=False,
            help_text='Storage location'
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
            blank=False,
            help_text='name',
            max_length=255
            )
    packagingUnit = models.PositiveIntegerField(
            help_text='Part quantity per package'
            )
    price = models.DecimalField(
            max_digits=13,
            decimal_places=4,
            blank=True,
            help_text='Price per part'
            )
    currency = models.CharField(
            unique=True,
            blank=False,
            help_text='Money system',
            max_length=3
            )
    sku = models.CharField(
            unique=True,
            blank=True,
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
            blank=False,
            help_text='name',
            max_length=255
            )



###############################################################################
# Stock
###############################################################################

class StockEntry(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
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
            blank=True,
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
    UPLOAD_TO = None
    filename = models.CharField(
            blank=False,
            help_text='original filename',
            max_length=255
            )
    uploadedAt = models.DateTimeField(
            auto_now_add=True,
            help_text='Upload date of filename',
            )
    content = models.FileField(upload_to=UPLOAD_TO,
            null=False,
            blank=False,
            help_text='Footprint attachment content'
            )

    class Meta:
        abstract = True

class PartAttachment(Attachment):
    UPLOAD_TO = 'attachment/images/%Y/%m/%d/' 

    part = models.ForeignKey(
            Part, 
            on_delete=models.CASCADE, 
            help_text='footprint'
            )

class FootprintAttachment(Attachment):
    UPLOAD_TO = 'attachment/images/%Y/%m/%d/' 

    footprint = models.ForeignKey(
            Footprint, 
            on_delete=models.CASCADE, 
            help_text='footprint'
            )


