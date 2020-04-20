from django import forms
from . import models

###############################################################################
# Category
###############################################################################

class CategoryForm(forms.ModelForm):
    pass 

class PartCategoryForm(CategoryForm):
    class Meta:
        model = models.PartCategory
        fields = (
                'name',
                'parent',
                'description',
                )

class FootprintCategoryForm(CategoryForm):
    class Meta:
        model = models.FootprintCategory
        fields = (
                'name',
                'parent',
                'description',
                )

class StorageLocationCategoryForm(CategoryForm):
    class Meta:
        model = models.StorageLocationCategory
        fields = (
                'name',
                'parent',
                'description',
                )

###############################################################################
# Storage
###############################################################################

class StorageLocationForm(forms.ModelForm):
    class Meta:
        model = models.StorageLocation
        fields = (
                'name',
                'category',
                'image',
                )

###############################################################################
# Footprint
###############################################################################

class FootprintForm(forms.ModelForm):
    class Meta:
        model = models.Footprint
        fields = (
                'name',
                'description',
                'category',
                'image',
                )

###############################################################################
# Company
###############################################################################

class CompanyForm(forms.ModelForm):
    pass

class DistributorForm(CompanyForm):
    class Meta:
        model = models.Distributor
        fields = (
                'name',
                'address',
                'url',
                'phone',
                'fax',
                'email',
                'comment',
                'image',
                'skuUrl',
                'forReports',
                )

class ManufacturerForm(CompanyForm):
    class Meta:
        model = models.Manufacturer
        fields = (
                'name',
                'address',
                'url',
                'phone',
                'fax',
                'email',
                'comment',
                'image',
                )
        
###############################################################################
# Unit
###############################################################################

# TODO Unit Form ? 

###############################################################################
# Part 
###############################################################################

class PartForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = (
                'name',
                'description',
                'category',
                'image',
                'footprint',
                'storageLocation',
                'comment',
                'minStockLevel',
                'averagePrice',
                'status',
                'needsReview',
                'partCondition',
                'createDate',
                'internalPartNumber',
                'removals',
                'partUnit',
                'productionRemarks',
                'metaPart',
                )

###############################################################################
# Project
###############################################################################

class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = (
            'name',
            'owner',
            'description',
            )

class ProjectPartForm(forms.ModelForm): 
    class Meta:
        model = models.ProjectPart
        fields = (
            'part',
            'quantity',
            'project',
            'remarks',
            'overageType',
            'overage',
            'lotNumber',
            'totalQuantity',
            )

class ProjectRunForm(forms.ModelForm):
    class Meta:
        model = models.ProjectRun
        fields = (
            'runDateTime',
            'project',
            'quantity',
            )

###############################################################################
# Parameter
###############################################################################

# TODO Parameter Form ? 

###############################################################################
# Stock
###############################################################################

class StockEntryForm(forms.ModelForm):
    class Meta:
        model = models.StockEntry
        fields = (
                'owner',
                'quantity',
                'part',
                'price',
                'boughtAt',
                'comment',
                )

###############################################################################
# Attachment
###############################################################################

class AttachmentForm(forms.ModelForm):
    pass

class ProjectAttachmentForm(forms.ModelForm):
    class Meta:
        model = models.ProjectAttachment
        fields = (
                'description',
                'content',
                )

class PartAttachmentForm(forms.ModelForm):
    class Meta:
        model = models.PartAttachment
        fields = (
                'description',
                'content',
                )

class FootprintAttachmentForm(forms.ModelForm):
    class Meta:
        model = models.PartAttachment
        fields = (
                'description',
                'content',
                )

