from django.urls import path,reverse_lazy

from . import views,models,forms

urlpatterns = [
        #
        # Test
        #
    path( 'test/part_category', views.show_part_category ),
    path( 'test/part_category/<int:pk>/', views.move_category ),
        #
        # PartCategory
        #
    path( 'part_category/<int:pk>/', 
        views.PnbPartKeeprDetailView.as_view(model=models.PartCategory),
        name='PnbPartKeepr_part_category_detail'),
        #
        # Part
        #
    path(
        'part/create',
        views.PnbPartKeeprCreateView.as_view(model=models.Part),
        name='PnbPartKeepr_part_create'
        ),
    path(
        'part/list',
        views.PnbPartKeeprListView.as_view(model=models.Part),
        name='PnbPartKeepr_part_list'
        ),
    path(
        'part/<int:pk>/',
        views.PnbPartKeeprDetailView.as_view(model=models.Part),
        name='PnbPartKeepr_part_detail'
        ),
    path(
        'part/<int:pk>/update',
        views.PnbPartKeeprUpdateView.as_view( model=models.Part, form_class=forms.PnbPartKeeprPartForm ),
        name='PnbPartKeepr_part_update'
        ),
    path(
        'part/<int:pk>/delete',
        views.PnbPartKeeprDeleteView.as_view(model=models.Part),
        name='PnbPartKeepr_part_delete'
        ),
        #
        # Footprint
        #
    path(
        'footprint/create',
        views.PnbPartKeeprCreateView.as_view(model=models.Footprint),
        name='PnbPartKeepr_footprint_create'
        ),
    path(
        'footprint/list',
        views.PnbPartKeeprListView.as_view(model=models.Footprint),
        name='PnbPartKeepr_footprint_list'
        ),
    path(
        'footprint/<int:pk>/',
        views.PnbPartKeeprDetailView.as_view(model=models.Footprint),
        name='PnbPartKeepr_footprint_detail'
        ),
    path(
        'footprint/<int:pk>/update',
        views.PnbPartKeeprUpdateView.as_view(
            model=models.Footprint, 
            form_class=forms.PnbPartKeeprFootprintForm 
            ),
        name='PnbPartKeepr_footprint_update'
        ),
    path(
        'footprint/<int:pk>/delete',
        views.PnbPartKeeprDeleteView.as_view(model=models.Footprint),
        name='PnbPartKeepr_footprint_delete'
        ),
        #
        # StorageLocation
        #
    path(
        'storage_location/list',
        views.PnbPartKeeprListView.as_view(model=models.StorageLocation),
        name='PnbPartKeepr_storageLocation_list'
        ),
    path(
        'storage_location/<int:pk>/',
        views.PnbPartKeeprDetailView.as_view(model=models.StorageLocation),
        name='PnbPartKeepr_storageLocation_detail'
        ),
    path(
        'storage_location/<int:pk>/update',
        views.PnbPartKeeprUpdateView.as_view(model=models.StorageLocation),
        name='PnbPartKeepr_storageLocation_update'
        ),
    path(
        'storage_location/<int:pk>/delete',
        views.PnbPartKeeprDeleteView.as_view(model=models.StorageLocation),
        name='PnbPartKeepr_storageLocation_delete'
        ),
]

