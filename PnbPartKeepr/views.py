
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from view_breadcrumbs import ListBreadcrumbMixin

from django.http import \
         HttpResponse,   \
         HttpResponseRedirect, \
         JsonResponse
from django.views.generic import \
         CreateView,\
         UpdateView,\
         DetailView,\
         ListView,\
         DeleteView,\
         ArchiveIndexView,\
         FormView
from django.shortcuts import \
         render,\
         get_object_or_404, \
         redirect

from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm

from . import models

#TODO remove for MPTT teste
def show_part_category(request):
    return render(request,"show_part_category.html",{'category':models.PartCategory.objects.all()})

#TODO remove for MPTT teste
def move_category(request, pk):
    category = get_object_or_404(models.PartCategory, pk=pk)
    if request.method == 'POST':
        form = MoveNodeForm(category, request.POST)
        if form.is_valid():
            try:
                category = form.save()
                return HttpResponseRedirect(category.get_absolute_url())
            except InvalidMove:
                pass
    else:
        form = MoveNodeForm(category)

    return render(request,'PnbPartKeepr/footprint_form.html', {
        'form': form,
        'category': category,
        'category_tree': models.PartCategory.objects.all(),
    })

class PnbPartKeeprCreateView(LoginRequiredMixin,CreateView):
    pass


class PnbPartKeeprDetailView(LoginRequiredMixin,DetailView):
    def get_queryset(self):
            return self.model.objects.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

#        if self.model == models.track_session:
#            context['object_list'] = [context['object'],]
#            context['showed'] = file_types_showed(context['object_list'])

        return context

class PnbPartKeeprDeleteView(LoginRequiredMixin,DeleteView):
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(PnbPartKeeprDeleteView, self).get_object()
        if self.model == models.Part:
            if obj.stockentry_set.count() > 0 :
                raise PermissionDenied("At least one strock entry use this part")
            if obj.projectpart_set.count() > 0 :
                raise PermissionDenied("At least one project use this part")
            if obj.projectrunpart_set.count() > 0 :
                raise PermissionDenied("At least one project run use this part")
        return obj

class PnbPartKeeprUpdateView(LoginRequiredMixin,UpdateView):
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(PnbPartKeeprUpdateView, self).get_object()
#       TODO some validation is it modifiable
#        if not obj.owner == self.request.user:
#            raise PermissionDenied
        return obj

class PnbPartKeeprListView(LoginRequiredMixin,ListView):
    paginate_by = 10

#    def get_queryset(self):
#
#        track_id    = self.get_id('track') 
#        owner_id    = self.get_id('owner')
#        vehicle_id  = self.get_id('vehicle')
#
#        objects = self.model.objects
#        if owner_id :
#            objects = objects.filter(owner_id=int(owner_id))
#        if track_id :
#            objects = objects.filter(track_id=int(track_id))
#        if vehicle_id :
#            objects = objects.filter(vehicle_id=int(vehicle_id))
#
#        return objects.all()


#    def get_context_data(self, **kwargs):
#        page_key = "page_%s"%(self.model._meta.model_name)
#
#        page_kwarg = self.page_kwarg
#        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or None
#        if page == None:
#            try: 
#                self.kwargs[self.page_kwarg] = self.request.session[page_key]
#            except:
#                pass
#
#        context = super(get_list, self).get_context_data(**kwargs)
#
#        self.request.session[page_key] = context['page_obj'].number
#
#        track_id = self.get_id('track') 
#        owner_id = self.get_id('owner')
#        vehicle_id = self.get_id('vehicle')
#
#        if owner_id :
#            context['owner']    = get_object_or_404(User,id=owner_id)
#        if track_id :
#            context['track']    = get_object_or_404(models.track_detail,id=track_id)
#        if vehicle_id :
#            context['vehicle']  = get_object_or_404(models.vehicle,id=vehicle_id)
#
#        context['owner_list']   = User.objects.all()
#        context['track_list']   = models.track_detail.objects.all()
#
#        vehicle_list = models.vehicle.objects
#
#        if owner_id :
#            vehicle_list = vehicle_list.filter(owner__pk=owner_id).all()
#
#        context['vehicle_list'] = vehicle_list.all()
#        context['compare_list'] = get_compare_list(self)
#
#        return context

