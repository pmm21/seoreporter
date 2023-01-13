from django.contrib import admin
from django.conf import settings
from urllib.parse import urlparse
from urllib.parse import parse_qs
from import_export.admin import ImportExportModelAdmin, ImportMixin
from .inlines import TopicInline
from . import models, inlines, resources

# Register your models here.

class ProjecAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'domain', 
                        'search_domain', 'language', 'country',
                            'location', 'device', 'creator']
    change_form_template = 'app_serp/project_view.html'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(creator=request.user)
    
    def add_view(self, request, form_url='', extra_context=None):
        settings.JAZZMIN_SETTINGS['changeform_format_overrides'] = {'app_serp.ProjectModel':'single'}
        
        self.fieldsets = (
                (None, {'fields':['project_name','domain', 'search_domain', 'language', 'country', 'location', 'device']}),
            )
        self.readonly_fields = ()
        self.inlines = [TopicInline]
        return super().add_view(request, form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fieldsets = (
                (None, {'fields':[]}),
                ('Project Info', {'fields': ('project_name','domain', 'search_domain', 'language', 'country', 'location', 'device')})
            )
        self.readonly_fields = ('domain', 'search_domain', 'language', 'country', 'location', 'device')
        self.inlines = []
        object_ = models.ProjectModel.objects.get(pk=object_id)
        extra_context = {
            'object_':object_
        }
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            keywords = instance.keywords
            instance.keywords = 'applied'
            instance.save()

            for line in keywords.split('\n'):
                models.KeywordModel.objects.create(keyword=line.lower().strip(),topic = instance)
        formset.save_m2m()
        
class TopicAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        projects = models.ProjectModel.objects.filter(creator=request.user)
        return qs.filter(project__in = projects)

    def save_model(self, request, obj, form, change):
        first_create = False
        keywords = obj.keywords
        if not obj.pk:
            first_create = True
        obj.keywords = 'applied'
        super().save_model(request, obj, form, change)

        if first_create:
            for line in keywords.split('\n'):
                models.KeywordModel.objects.create(keyword=line.lower().strip(),topic = obj)

            models.PosToTrackModel.objects.create(topic=obj)
            models.AddvanceColumnShowModel.objects.create(topic=obj)

class KeywordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [resources.KeywordResource]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        projects = models.ProjectModel.objects.filter(creator=request.user)
        topics = models.TopicModel.objects.filter(project__in = projects)
        return qs.filter(topic__in = topics)

    def process_result(self, result, request):
        self.generate_log_entries(result, request)
        self.add_success_message(result, request)
        post_import.send(sender=None, model=self.model)

        url = reverse('admin:%s_%s_changelist' % self.get_model_info(),
                      current_app=self.admin_site.name)
        print('url', url)
        return HttpResponseRedirect(url)

    def get_import_data_kwargs(self, request, *args, **kwargs):
        """
        Prepare kwargs for import_data.
        """
        url = request.build_absolute_uri()
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        for item in query:
            kwargs[item]=query[item]

        form = kwargs.get('form')
        if form:
            kwargs.pop('form')
            return kwargs
        return {}



admin.site.register(models.ProjectModel, ProjecAdmin)
admin.site.register(models.TopicModel, TopicAdmin)
admin.site.register(models.KeywordModel, KeywordAdmin)


