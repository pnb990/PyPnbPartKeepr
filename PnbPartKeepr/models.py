from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

def get_default_user_id():
    u,created = User.objects.get_or_create(username="inconnu")
    if created:
        print("Created %s"%str(u))
    return u.id

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
    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        abstract = True

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
    phone = models.PhoneField(
            blank=True,
            help_text='Contact phone number'
            )
    fax = models.PhoneField(
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
    image = ImageField(
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
            help_text='Use this one for pricing calculation'
            )
    parts = models.ForeignKey(
            Part, 
            models.PROTECT, 
            help_text='Parts'
            )

class Manufacturer(models.Model):
    UPLOAD_TO = 'manufacturer/images/%Y/%m/%d/'

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
            models.PROTECT, 
            help_text='Category'
            )
    image = ImageField(
            upload_to='footprint/images/%Y/%m/%d/', 
            null=True,
            blank=True,
            help_text='Image'
            )

class FootprintCategory(Category):
    pass

class FootprintAttachment(Attachment):
    UPLOAD_TO = 'attachment/images/%Y/%m/%d/' 

    footprint = models.ForeignKey(
            Footprint, 
            models.CASCADE, 
            help_text='footprint'
            )


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
            FootprintCategory, 
            models.PROTECT, 
            help_text='Category'
            )
    image = ImageField(
            upload_to='footprint/images/%Y/%m/%d/', 
            blank=True,
            help_text='Image'
            )
    footprint = models.ForeignKey(
            Footprint, 
            models.PROTECT, 
            blank=True,
            help_text='footprint'
            )
    storageLocation = models.ForeignKey(
            StorageLocation, 
            models.PROTECT, 
            blank=False,
            help_text='Storage location'
            )


class PartCategory(Category):
    pass

class PartAttachment(Attachment):
    UPLOAD_TO = 'attachment/images/%Y/%m/%d/' 

    part = models.ForeignKey(
            Part, 
            models.CASCADE, 
            help_text='footprint'
            )

class PartManufacturer(models.Model):
    partNumber = models.CharField(
            blank=False,
            help_text='Part\'s number',
            max_length=255
            )
    part = models.ForeignKey(
            Part, 
            models.PROTECT, 
            help_text='part'
            )
    manufacturer = models.ForeignKey(
            Manufacturer, 
            models.PROTECT, 
            help_text='footprint'
            )


class StockEntry(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            default=get_default_user_id
            )
    quantity = IntegerField(
            min_length = 0
            help_text='Part quantity inside'
            )
    part = models.ForeignKey(
            Part, 
            models.PROTECT, 
            help_text='part'
            )
    price = DecimalField(
            max_digits=13,
            decimal_place=4
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


class StorageLocation(models.Model):
    name = models.CharField(
            unique=True,
            blank=False,
            help_text='name',
            max_length=255
            )
    image = ImageField(
            upload_to='stockLocation/images/%Y/%m/%d/', 
            null=True,
            blank=True,
            help_text='Image'
            )
    category = models.ForeignKey(
            StorageLocationCategory, 
            models.PROTECT, 
            help_text='Category'
            )
    part = models.ForeignKey(
            Part, 
            models.PROTECT, 
            help_text='part'
            )


class StorageLocationCategory(Category):
    pass


