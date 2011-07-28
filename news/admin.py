from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from django.contrib import admin

from django.http import HttpResponse
from django.core import serializers

from news.forms import NewsForm
from news.models import News

from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec

class PlaceFilterSpec(ChoicesFilterSpec):
    def __init__(self, f, request, params, model, model_admin):
        super(PlaceFilterSpec, self).__init__(f, request, params, model,
                                                   model_admin)
        self.lookup_kwarg = '%s__istartswith' % f.name
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        values_list = model.objects.values_list(f.name, flat=True)
        # getting the first char of values
        self.lookup_choices = list(set(val[0] for val in values_list if val))
        self.lookup_choices.sort()

    def choices(self, cl):
        yield {'selected': self.lookup_val is None,
                'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                'display': _('All')}
        for val in self.lookup_choices:
            yield {'selected': smart_unicode(val) == self.lookup_val,
                    'query_string': cl.get_query_string({self.lookup_kwarg: val}),
                    'display': val.upper()}
    def title(self):
        return _('%(field_name)s that starts with') % \
            {'field_name': self.field.verbose_name}

FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'pub_place_filter', False), PlaceFilterSpec)) 


class NewsAdmin(admin.ModelAdmin):
    """
        Admin for news
    """
    date_hierarchy = 'pub_date'
    list_display = ('title', 'is_published', 'pub_place', 'pub_date', 'unpub_date')
    #list_editable = ('title', 'is_published')
    list_filter = ('is_published', 'tags', 'title')
    pub_place_filter = {'title':News.objects.all()}
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    form = NewsForm
    
    actions = ['make_published', 'make_unpublished']
    
    save_as = True
    save_on_top = True
    
    def queryset(self, request):
        """
            Override to use the objects and not just the default visibles only.
        """
        return News.objects.all()
       
    def make_published(self, request, queryset):
        """
            Marks selected news items as published
        """
        rows_updated = queryset.update(is_published=True)
        self.message_user(request, ungettext('%(count)d newsitem was published', 
                                            '%(count)d newsitems where published', 
                                            rows_updated) % {'count': rows_updated})
    make_published.short_description = _('Publish selected news')

    def make_unpublished(self, request, queryset):
        """
            Marks selected news items as unpublished
        """
        rows_updated =queryset.update(is_published=False)
        self.message_user(request, ungettext('%(count)d newsitem was unpublished', 
                                            '%(count)d newsitems where unpublished', 
                                            rows_updated) % {'count': rows_updated})
    make_unpublished.short_description = _('Unpublish selected news')


   
admin.site.register(News, NewsAdmin)
