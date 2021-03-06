
from django.core.exceptions import ImproperlyConfigured,PermissionDenied
from django.urls import reverse_lazy
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from view_breadcrumbs import ListBreadcrumbMixin

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect

from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm

from . import models

#TODO remove for MPTT teste
def PartCategoryListView(request):
    return render(request,
                  "PnbPartKeepr/test/list_part_category.html",
                  {'category':models.PartCategory.objects.filter(parent_id=1)}
                  )

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

    return render(request,'PnbPartKeepr/test/footprint_form.html', {
        'form': form,
        'category': category,
        'category_tree': models.PartCategory.objects.all(),
    })



class DetailView(LoginRequiredMixin,generic.DetailView):
#    def get_queryset(self):
#            return self.model.objects.filter(id=self.kwargs['pk'])

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)

#        if self.model == models.track_session:
#            context['object_list'] = [context['object'],]
#            context['showed'] = file_types_showed(context['object_list'])

#        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name = 'PnbPartKeepr/confirm_delete.html'
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super().get_object()
        if self.model == models.Part:
            if obj.stockentry_set.count() > 0 :
                raise PermissionDenied("At least one strock entry use this part")
            if obj.projectpart_set.count() > 0 :
                raise PermissionDenied("At least one project use this part")
            if obj.projectrunpart_set.count() > 0 :
                raise PermissionDenied("At least one project run use this part")
        elif issubclass(self.model,models.Category):
            if obj.children.count() > 0 :
                raise PermissionDenied("At least one sub category_tree in it")
        return obj

    def get_success_url(self):
        if hasattr(self.object,'get_success_url'):
            return self.object.get_success_url()
        return super().get_success_url()


class CreateView(LoginRequiredMixin,generic.CreateView):
    template_name = 'PnbPartKeepr/update_form.html'

    def get_initial(self):
        ret = super().get_initial()
        ret['owner'] = self.request.user.pk
        return ret

    def form_valid(self, form):
        attached_id = self.kwargs.get('attached_id',None)
        if attached_id != None:
            instance = form.save(commit=False)
            if isinstance(instance,models.ProjectAttachment):
                instance.project = models.Project.objects.get(id=attached_id)
            elif ( isinstance(instance,models.PartAttachment) or
                   isinstance(instance,models.StockEntry)     ) :
                instance.part = models.Part.objects.get(id=attached_id)
            elif isinstance(instance,models.FootprintAttachment):
                instance.footprint = models.Footprint.objects.get(id=attached_id)
            else:
                raise ValueError("This instance is not linked to an other!")

        return super().form_valid(form)


class UpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = 'PnbPartKeepr/update_form.html'

class ListView(LoginRequiredMixin,generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if len(self.request.GET) != 0 and hasattr(self.model,'queryset'):
            queryset = self.model.queryset(queryset,self.request.GET)

        if issubclass(self.model,models.Category):
            queryset = queryset.filter(parent_id=self.kwargs.get('pk',None))

        if issubclass(self.model,models.StockEntry):
            queryset = queryset.filter(part_id=self.kwargs.get('pk',None))

        return queryset


    def get_context_data(self, **kwargs):
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
        context = super().get_context_data(**kwargs)

        context['search_fields'] = []
        for name in getattr(self.model,'SearchFields',{}).keys():
            context['search_fields'].append({
                "name":name,
                "val":self.request.GET.get(name,'')
            })

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
        return context

