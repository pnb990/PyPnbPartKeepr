from django import forms
from . import models

class PnbPartKeeprPartForm(forms.ModelForm):
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


class PnbPartKeeprFootprintForm(forms.ModelForm):
    class Meta:
        model = models.Footprint
        fields = (
                'name',
                'description',
                'category',
                'image',
                )



