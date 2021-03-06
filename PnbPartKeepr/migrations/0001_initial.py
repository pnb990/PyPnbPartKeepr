# Generated by Django 3.0.5 on 2020-05-01 12:06

import PnbPartKeepr.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255, unique=True)),
                ('address', models.TextField(blank=True, default='', help_text='Postal address')),
                ('url', models.URLField(blank=True, help_text='Web site url')),
                ('phone', phone_field.models.PhoneField(blank=True, default='', help_text='Contact phone number', max_length=31)),
                ('fax', phone_field.models.PhoneField(blank=True, default='', help_text='Contact fax number', max_length=31)),
                ('email', models.EmailField(blank=True, default='', help_text='Contact fax number', max_length=254)),
                ('comment', models.TextField(blank=True, default='', help_text='Comment')),
                ('image', models.ImageField(blank=True, help_text='Image', null=True, upload_to='distributor/images/%Y/%m/%d/')),
                ('skuUrl', models.URLField(blank=True, default='', help_text='SKU URL')),
                ('forReports', models.BooleanField(default=True, help_text='Use this one for pricing calculation')),
            ],
            options={
                'abstract': False,
            },
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Footprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255, unique=True)),
                ('description', models.TextField(blank=True, default='', help_text='Some details')),
                ('image', models.ImageField(blank=True, help_text='Image', null=True, upload_to='footprint/images/%Y/%m/%d/')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, PnbPartKeepr.models.SearchMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255, unique=True)),
                ('address', models.TextField(blank=True, default='', help_text='Postal address')),
                ('url', models.URLField(blank=True, help_text='Web site url')),
                ('phone', phone_field.models.PhoneField(blank=True, default='', help_text='Contact phone number', max_length=31)),
                ('fax', phone_field.models.PhoneField(blank=True, default='', help_text='Contact fax number', max_length=31)),
                ('email', models.EmailField(blank=True, default='', help_text='Contact fax number', max_length=254)),
                ('comment', models.TextField(blank=True, default='', help_text='Comment')),
                ('image', models.ImageField(blank=True, help_text='Image', null=True, upload_to='manufacturer/images/%Y/%m/%d/')),
            ],
            options={
                'abstract': False,
            },
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255)),
                ('description', models.TextField(blank=True, default='', help_text='Some details')),
                ('image', models.ImageField(blank=True, help_text='Image', null=True, upload_to='footprint/images/%Y/%m/%d/')),
                ('comment', models.TextField(blank=True, default='', help_text='Some comments')),
                ('minStockLevel', models.PositiveIntegerField(help_text='Number minimum of part in stock allowed')),
                ('averagePrice', models.DecimalField(blank=True, decimal_places=4, help_text="General average part's price", max_digits=13, null=True)),
                ('status', models.CharField(blank=True, default='', help_text='a status ... may be active/end of life/development ???', max_length=255)),
                ('needsReview', models.BooleanField(default=True, help_text='Use this one for pricing calculation')),
                ('partCondition', models.CharField(blank=True, default='', help_text="I don' know...", max_length=255)),
                ('createDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('internalPartNumber', models.CharField(blank=True, default='', help_text='part number used in internal data base', max_length=255)),
                ('removals', models.BooleanField(default=False, help_text='Need to be removed ?')),
                ('productionRemarks', models.CharField(blank=True, default='', help_text='Remarks done by production', max_length=255)),
                ('metaPart', models.BooleanField(default=False, help_text='is a meta part ?')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, PnbPartKeepr.models.SearchMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PartMeasurementUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255)),
                ('shortName', models.CharField(help_text='Short name', max_length=16)),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255)),
                ('description', models.CharField(blank=True, default='', help_text='description', max_length=255)),
                ('owner', models.ForeignKey(blank=True, default=PnbPartKeepr.models.get_default_user_id, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, PnbPartKeepr.models.SearchMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runDateTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity', models.PositiveIntegerField(default=0, help_text='The quantity project has been build')),
                ('project', models.ForeignKey(help_text='project', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Project')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SiPrefix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(help_text='System International prefix name (e.g. yotta, deca, deci, centi)', max_length=255)),
                ('symbol', models.CharField(help_text='Symbol of System International prefix (e.g. m, M, G)', max_length=255)),
                ('exponent', models.IntegerField(help_text='The exponent of the System International prefix (e.g. milli = 10^-3)')),
                ('base', models.IntegerField(help_text='The base of the System International (e.g. 2^-3)')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the unit (e.g. Volts, Ampere, Farad, Metres)', max_length=255)),
                ('symbol', models.CharField(help_text='The symbol of the unit (e.g. V, A, F, m)', max_length=255)),
                ('prefixes', models.ManyToManyField(help_text='Defines the allowed System International prefix for this parameter unit', to='PnbPartKeepr.SiPrefix')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StorageLocationCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255)),
                ('description', models.TextField(blank=True, default='', help_text='Some details')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='PnbPartKeepr.StorageLocationCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StorageLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, help_text='Image', null=True, upload_to='stockLocation/images/%Y/%m/%d/')),
                ('category', mptt.fields.TreeForeignKey(help_text='Category', on_delete=django.db.models.deletion.PROTECT, to='PnbPartKeepr.StorageLocationCategory')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, PnbPartKeepr.models.SearchMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StockEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(help_text='Part quantity inside')),
                ('price', models.DecimalField(decimal_places=4, help_text='Bought stock price per part', max_digits=13, null=True)),
                ('boughtAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.TextField(blank=True, default='', help_text='Comment')),
                ('owner', models.ForeignKey(blank=True, default=PnbPartKeepr.models.get_default_user_id, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('part', models.ForeignKey(help_text='part', on_delete=django.db.models.deletion.PROTECT, to='PnbPartKeepr.Part')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectRunPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(help_text='the quantity of a production run')),
                ('lotNumber', models.CharField(blank=True, default='', help_text='the lot number use in production', max_length=10)),
                ('part', models.ForeignKey(help_text='the part used in a production run', on_delete=django.db.models.deletion.PROTECT, to='PnbPartKeepr.Part')),
                ('projectRun', models.ForeignKey(help_text='project run', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.ProjectRun')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(help_text='Part quantity inside')),
                ('remarks', models.CharField(blank=True, default='', help_text='Remarks', max_length=255)),
                ('overageType', models.CharField(choices=[('absolute', 'absolute'), ('percent', 'percent')], help_text='The type of the value', max_length=10)),
                ('overage', models.PositiveIntegerField(default=0, help_text='the overage can either be percent or an absolute value depending on overageType.')),
                ('lotNumber', models.CharField(blank=True, default='', help_text='the lot number', max_length=10)),
                ('totalQuantity', models.PositiveIntegerField(default=0, help_text='The total quantity including overage')),
                ('part', models.ForeignKey(help_text='part', on_delete=django.db.models.deletion.PROTECT, to='PnbPartKeepr.Part')),
                ('project', models.ForeignKey(help_text='project', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Project')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadedAt', models.DateTimeField(auto_now=True, help_text='Upload date of filename')),
                ('description', models.TextField(blank=True, default='', help_text='Some details')),
                ('content', models.FileField(help_text='Project attachment file', upload_to='project/attachments/%Y/%m/%d/')),
                ('project', models.ForeignKey(help_text='project', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PartParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255)),
                ('description', models.CharField(help_text='description', max_length=255)),
                ('minValue', models.FloatField(help_text='minimum value')),
                ('normalizedMinValue', models.FloatField(help_text='normalized minimum value', null=True)),
                ('maxValue', models.FloatField(help_text='maximum value')),
                ('normalizedMaxValue', models.FloatField(help_text='normalized maximum value', null=True)),
                ('maxSiPrefix', models.ForeignKey(help_text='The SiPrefix of the unit for maximum value', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='PnbPartKeepr.SiPrefix')),
                ('minSiPrefix', models.ForeignKey(help_text='The SiPrefix of the unit for minimum value', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='PnbPartKeepr.SiPrefix')),
                ('part', models.ForeignKey(help_text='parameter criteria ???', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Part')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PartManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partNumber', models.CharField(blank=True, default='', help_text='name', max_length=255)),
                ('manufacturer', models.ForeignKey(help_text='Manufacturer', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Manufacturer')),
                ('part', models.ForeignKey(help_text='part', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Part')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PartDistributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderNumber', models.CharField(blank=True, default='', help_text='name', max_length=255)),
                ('packagingUnit', models.PositiveIntegerField(help_text='Part quantity per package')),
                ('price', models.DecimalField(blank=True, decimal_places=4, help_text='Price per part', max_digits=13, null=True)),
                ('currency', models.CharField(choices=[('AUD', 'Australia Dollar'), ('GBP', 'Great Britain Pound'), ('EUR', 'Euro'), ('JPY', 'Japan Yen'), ('CHF', 'Switzerland Franc'), ('USD', 'USA Dollar'), ('AFN', 'Afghanistan Afghani'), ('ALL', 'Albania Lek'), ('DZD', 'Algeria Dinar'), ('AOA', 'Angola Kwanza'), ('ARS', 'Argentina Peso'), ('AMD', 'Armenia Dram'), ('AWG', 'Aruba Florin'), ('AUD', 'Australia Dollar'), ('ATS', 'Austria Schilling'), ('BEF', 'Belgium Franc'), ('AZN', 'Azerbaijan New Manat'), ('BSD', 'Bahamas Dollar'), ('BHD', 'Bahrain Dinar'), ('BDT', 'Bangladesh Taka'), ('BBD', 'Barbados Dollar'), ('BYR', 'Belarus Ruble'), ('BZD', 'Belize Dollar'), ('BMD', 'Bermuda Dollar'), ('BTN', 'Bhutan Ngultrum'), ('BOB', 'Bolivia Boliviano'), ('BAM', 'Bosnia Mark'), ('BWP', 'Botswana Pula'), ('BRL', 'Brazil Real'), ('GBP', 'Great Britain Pound'), ('BND', 'Brunei Dollar'), ('BGN', 'Bulgaria Lev'), ('BIF', 'Burundi Franc'), ('XOF', 'CFA Franc BCEAO'), ('XAF', 'CFA Franc BEAC'), ('XPF', 'CFP Franc'), ('KHR', 'Cambodia Riel'), ('CAD', 'Canada Dollar'), ('CVE', 'Cape Verde Escudo'), ('KYD', 'Cayman Islands Dollar'), ('CLP', 'Chili Peso'), ('CNY', 'China Yuan/Renminbi'), ('COP', 'Colombia Peso'), ('KMF', 'Comoros Franc'), ('CDF', 'Congo Franc'), ('CRC', 'Costa Rica Colon'), ('HRK', 'Croatia Kuna'), ('CUC', 'Cuba Convertible Peso'), ('CUP', 'Cuba Peso'), ('CYP', 'Cyprus Pound'), ('CZK', 'Czech Koruna'), ('DKK', 'Denmark Krone'), ('DJF', 'Djibouti Franc'), ('DOP', 'Dominican Republich Peso'), ('XCD', 'East Caribbean Dollar'), ('EGP', 'Egypt Pound'), ('SVC', 'El Salvador Colon'), ('EEK', 'Estonia Kroon'), ('ETB', 'Ethiopia Birr'), ('EUR', 'Euro'), ('FKP', 'Falkland Islands Pound'), ('FIM', 'Finland Markka'), ('FJD', 'Fiji Dollar'), ('GMD', 'Gambia Dalasi'), ('GEL', 'Georgia Lari'), ('DMK', 'Germany Mark'), ('GHS', 'Ghana New Cedi'), ('GIP', 'Gibraltar Pound'), ('GRD', 'Greece Drachma'), ('GTQ', 'Guatemala Quetzal'), ('GNF', 'Guinea Franc'), ('GYD', 'Guyana Dollar'), ('HTG', 'Haiti Gourde'), ('HNL', 'Honduras Lempira'), ('HKD', 'Hong Kong Dollar'), ('HUF', 'Hungary Forint'), ('ISK', 'Iceland Krona'), ('INR', 'India Rupee'), ('IDR', 'Indonesia Rupiah'), ('IRR', 'Iran Rial'), ('IQD', 'Iraq Dinar'), ('IED', 'Ireland Pound'), ('ILS', 'Israel New Shekel'), ('ITL', 'Italy Lira'), ('JMD', 'Jamaica Dollar'), ('JPY', 'Japan Yen'), ('JOD', 'Jordan Dinar'), ('KZT', 'Kazakhstan Tenge'), ('KES', 'Kenya Shilling'), ('KWD', 'Kuwait Dinar'), ('KGS', 'Kyrgyzstan Som'), ('LAK', 'Laos Kip'), ('LVL', 'Latvia Lats'), ('LBP', 'Lebanon Pound'), ('LSL', 'Lesotho Loti'), ('LRD', 'Liberia Dollar'), ('LYD', 'Libya Dinar'), ('LTL', 'Lithuania Litas'), ('LUF', 'Luxembourg Franc'), ('MOP', 'Macau Pataca'), ('MKD', 'Macedonia Denar'), ('MGA', 'Malagasy Ariary'), ('MWK', 'Malawi Kwacha'), ('MYR', 'Malaysia Ringgit'), ('MVR', 'Maldives Rufiyaa'), ('MTL', 'Malta Lira'), ('MRO', 'Mauritania Ouguiya'), ('MUR', 'Mauritius Rupee'), ('MXN', 'Mexico Peso'), ('MDL', 'Moldova Leu'), ('MNT', 'Mongolia Tugrik'), ('MAD', 'Morocco Dirham'), ('MZN', 'Mozambique New Metical'), ('MMK', 'Myanmar Kyat'), ('ANG', 'NL Antilles Guilder'), ('NAD', 'Namibia Dollar'), ('NPR', 'Nepal Rupee'), ('NLG', 'Netherlands Guilder'), ('NZD', 'New Zealand Dollar'), ('NIO', 'Nicaragua Cordoba Oro'), ('NGN', 'Nigeria Naira'), ('KPW', 'North Korea Won'), ('NOK', 'Norway Kroner'), ('OMR', 'Oman Rial'), ('PKR', 'Pakistan Rupee'), ('PAB', 'Panama Balboa'), ('PGK', 'Papua New Guinea Kina'), ('PYG', 'Paraguay Guarani'), ('PEN', 'Peru Nuevo Sol'), ('PHP', 'Philippines Peso'), ('PLN', 'Poland Zloty'), ('PTE', 'Portugal Escudo'), ('QAR', 'Qatar Rial'), ('RON', 'Romania New Lei'), ('RUB', 'Russia Rouble'), ('RWF', 'Rwanda Franc'), ('WST', 'Samoa Tala'), ('STD', 'Sao Tome/Principe Dobra'), ('SAR', 'Saudi Arabia Riyal'), ('RSD', 'Serbia Dinar'), ('SCR', 'Seychelles Rupee'), ('SLL', 'Sierra Leone Leone'), ('SGD', 'Singapore Dollar'), ('SKK', 'Slovakia Koruna'), ('SIT', 'Slovenia Tolar'), ('SBD', 'Solomon Islands Dollar'), ('SOS', 'Somali Shilling'), ('ZAR', 'South Africa Rand'), ('KRW', 'South Korea Won'), ('ESP', 'Spain Peseta'), ('LKR', 'Sri Lanka Rupee'), ('SHP', 'St Helena Pound'), ('SDG', 'Sudan Pound'), ('SRD', 'Suriname Dollar'), ('SZL', 'Swaziland Lilangeni'), ('SEK', 'Sweden Krona'), ('CHF', 'Switzerland Franc'), ('SYP', 'Syria Pound'), ('TWD', 'Taiwan Dollar'), ('TZS', 'Tanzania Shilling'), ('THB', 'Thailand Baht'), ('TOP', "Tonga Pa'anga"), ('TTD', 'Trinidad/Tobago Dollar'), ('TND', 'Tunisia Dinar'), ('TRY', 'Turkish New Lira'), ('TMM', 'Turkmenistan Manat'), ('USD', 'USA Dollar'), ('UGX', 'Uganda Shilling'), ('UAH', 'Ukraine Hryvnia'), ('UYU', 'Uruguay Peso'), ('AED', 'United Arab Emirates Dirham'), ('VUV', 'Vanuatu Vatu'), ('VEB', 'Venezuela Bolivar'), ('VND', 'Vietnam Dong'), ('YER', 'Yemen Rial'), ('ZMK', 'Zambia Kwacha'), ('ZWD', 'Zimbabwe Dollar')], help_text='Money system', max_length=3)),
                ('sku', models.CharField(blank=True, default='', help_text='Stock keeping unit', max_length=255)),
                ('forReports', models.BooleanField(default=True, help_text='Use this one for pricing calculation')),
                ('distributor', models.ForeignKey(help_text='Distributor', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Distributor')),
                ('part', models.ForeignKey(help_text='part', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Part')),
            ],
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PartCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255)),
                ('description', models.TextField(blank=True, default='', help_text='Some details')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='PnbPartKeepr.PartCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PartAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadedAt', models.DateTimeField(auto_now=True, help_text='Upload date of filename')),
                ('description', models.TextField(blank=True, default='', help_text='Some details')),
                ('content', models.FileField(help_text='Part attachment file', upload_to='part/attachments/%Y/%m/%d/')),
                ('part', models.ForeignKey(help_text='footprint', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Part')),
            ],
            options={
                'abstract': False,
            },
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.AddField(
            model_name='part',
            name='category',
            field=mptt.fields.TreeForeignKey(help_text='Category', on_delete=django.db.models.deletion.PROTECT, to='PnbPartKeepr.PartCategory'),
        ),
        migrations.AddField(
            model_name='part',
            name='footprint',
            field=models.ForeignKey(blank=True, help_text='footprint', null=True, on_delete=django.db.models.deletion.PROTECT, to='PnbPartKeepr.Footprint'),
        ),
        migrations.AddField(
            model_name='part',
            name='partUnit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.PartMeasurementUnit'),
        ),
        migrations.AddField(
            model_name='part',
            name='storageLocation',
            field=models.ForeignKey(help_text='Storage location', on_delete=django.db.models.deletion.PROTECT, to='PnbPartKeepr.StorageLocation'),
        ),
        migrations.CreateModel(
            name='MetaPartParameterCriteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(help_text='value')),
                ('normalizedValue', models.FloatField(help_text='normalized value', null=True)),
                ('stringValue', models.CharField(blank=True, default='', help_text='Value in case of string', max_length=255)),
                ('valueType', models.CharField(choices=[('numeric', 'numeric'), ('string', 'string')], help_text='The type of the value', max_length=10)),
                ('name', models.CharField(help_text='name', max_length=255)),
                ('operator', models.CharField(help_text='operator ???', max_length=255)),
                ('part', models.ForeignKey(help_text='parameter criteria ???', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Part')),
                ('siPrefix', models.ForeignKey(help_text='The SiPrefix of the unit', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='PnbPartKeepr.SiPrefix')),
                ('unit', models.ForeignKey(blank=True, help_text='The unit for this type. May be null', null=True, on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Unit')),
            ],
            options={
                'abstract': False,
            },
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FootprintCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name', max_length=255)),
                ('description', models.TextField(blank=True, default='', help_text='Some details')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='PnbPartKeepr.FootprintCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FootprintAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadedAt', models.DateTimeField(auto_now=True, help_text='Upload date of filename')),
                ('description', models.TextField(blank=True, default='', help_text='Some details')),
                ('content', models.FileField(help_text='Footprint attachment file', upload_to='footprint/attachments/%Y/%m/%d/')),
                ('footprint', models.ForeignKey(help_text='footprint', on_delete=django.db.models.deletion.CASCADE, to='PnbPartKeepr.Footprint')),
            ],
            options={
                'abstract': False,
            },
            bases=(PnbPartKeepr.models.ReverseUrlMixin, models.Model),
        ),
        migrations.AddField(
            model_name='footprint',
            name='category',
            field=mptt.fields.TreeForeignKey(help_text='Category', on_delete=django.db.models.deletion.PROTECT, to='PnbPartKeepr.FootprintCategory'),
        ),
    ]
