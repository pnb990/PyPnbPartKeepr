from django.urls import path,reverse_lazy

from . import views,models,forms


def crud(className, category=False):
    name    = className.lower()
    model   = getattr(models,className)
    form    = getattr(forms,className+'Form')

    urls = [
            path(name+'/detail/<int:pk>',
                views.DetailView.as_view(model=model),
                name='pnbpartkeepr.'+name+'.detail'
                ),
            path(name+'/update/<int:pk>',
                views.UpdateView.as_view(model=model, form_class=form ),
                name='pnbpartkeepr.'+name+'.update'
                ),
            path(name+'/delete/<int:pk>',
                views.DeleteView.as_view(
                    model=model, 
                    success_url=reverse_lazy('pnbpartkeepr.'+name+'.list'),
                    ),
                name='pnbpartkeepr.'+name+'.delete'
                ),
            ]

    if issubclass(model,models.Attachment):
        urls += [
                path(name+'/create/<int:attached_id>',
                    views.CreateView.as_view(model=model, form_class=form ),
                    name='pnbpartkeepr.'+name+'.create'
                    ),
                ]
    else:
        urls += [
                path(name+'/list',
                    views.ListView.as_view(model=model),
                    name='pnbpartkeepr.'+name+'.list'
                    ),
                path(name+'/create',
                    views.CreateView.as_view(model=model, form_class=form ),
                    name='pnbpartkeepr.'+name+'.create'
                    ),
                ]

    if issubclass(model,models.Category):
        urls += [
                path(name+'/list/<int:pk>',
                    views.ListView.as_view(model=model),
                    name='pnbpartkeepr.'+name+'.list'
                    )
                ]
    return urls


urlpatterns = [
        #
        # Test
        #
    path( 'test/part_category/<int:pk>/', views.move_category ),
    ]


urlpatterns += crud( 'Project'                  )
urlpatterns += crud( 'ProjectAttachment'        )

urlpatterns += crud( 'Part'                     )
urlpatterns += crud( 'PartCategory'             )
urlpatterns += crud( 'PartAttachment'           )

urlpatterns += crud( 'Footprint'                )
urlpatterns += crud( 'FootprintCategory'        )
urlpatterns += crud( 'FootprintAttachment'      )

urlpatterns += crud( 'StorageLocation'          )
urlpatterns += crud( 'StorageLocationCategory'  )


