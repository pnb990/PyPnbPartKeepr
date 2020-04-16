from django.urls import path,reverse_lazy

from . import views,models,forms

def crud(pathPrefix,model,form_class,name):
    return [
            path(pathPrefix+'/list',
            views.PnbPartKeeprListView.as_view(model=model),
            name='PnbPartKeepr_'+name+'_list'
            ),
            path(pathPrefix+'/create',
            views.PnbPartKeeprCreateView.as_view(model=model),
            name='PnbPartKeepr_'+name+'_create'
            ),
            path(pathPrefix+'/<int:pk>/',
            views.PnbPartKeeprDetailView.as_view(model=model),
            name='PnbPartKeepr_'+name+'_detail'
            ),
            path(pathPrefix+'/<int:pk>/update',
            views.PnbPartKeeprUpdateView.as_view(model=model, form_class=form_class ),
            name='PnbPartKeepr_'+name+'_update'
            ),
            path(pathPrefix+'/<int:pk>/delete',
            views.PnbPartKeeprDeleteView.as_view(
                model=model, 
                success_url=reverse_lazy('PnbPartKeepr_'+name+'_list'),
                ),
            name='PnbPartKeepr_'+name+'_delete'
            )
            ]


urlpatterns = [
        #
        # Test
        #
    path( 'test/part_category', views.show_part_category ),
    path( 'test/part_category/<int:pk>/', views.move_category ),
        #
        # PartCategory
        #
    path( 'part_category/list', 
        views.PnbPartKeeprListView.as_view(model=models.PartCategory),
        name='PnbPartKeepr_partCategory_list'),
    path( 'part_category/<int:pk>/', 
        views.PnbPartKeeprDetailView.as_view(model=models.PartCategory),
        name='PnbPartKeepr_partCategory_detail'),
    ]

# PartCategory
urlpatterns += crud(
        'part_category',
        models.PartCategory,
        None, #forms.PartCategoryForm,
        'partCategory'
        )

# FootprintCategory
urlpatterns += crud(
        'footprint_category',
        models.FootprintCategory,
        None, #forms.FootprintCategoryForm,
        'footprintCategory'
        )

# storageLocationCategory
urlpatterns += crud(
        'storage_location_category',
        models.StorageLocationCategory,
        None, #forms.StorageLocationCategoryForm,
        'storageLocationCategory'
        )


# Part
urlpatterns += crud(
        'part',
        models.Part,
        forms.PartForm,
        'part'
        )

# Footprint
urlpatterns += crud(
        'footprint',
        models.Footprint,
        forms.FootprintForm,
        'footprint'
        )

# StorageLocation
urlpatterns += crud(
        'storageLocation',
        models.StorageLocation,
        forms.StorageLocationForm,
        'storageLocation'
        )


