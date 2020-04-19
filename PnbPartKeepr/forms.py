from django import forms
from . import models

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


class FootprintForm(forms.ModelForm):
    class Meta:
        model = models.Footprint
        fields = (
                'name',
                'description',
                'category',
                'image',
                )

class StorageLocationForm(forms.ModelForm):
    class Meta:
        model = models.StorageLocation
        fields = (
                'name',
                'category',
                'image',
                )



