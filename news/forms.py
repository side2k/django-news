from django import forms
from news import settings
from tinymce.widgets import AdminTinyMCE
from news.models import News
from django.utils.translation import ugettext_lazy as _
from tagging.models import Tag

class NewsForm(forms.ModelForm):
    pub_places = forms.ChoiceField(label=_("Publication places"), choices=settings.PUBLICATION_PLACES, help_text=_("Place where the news will be published"))
    def _get_widget(self):
        return AdminTinyMCE()
        
        
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        #placeholder=kwargs["placeholder"]
        widget = self._get_widget()
        self.fields['content'].widget = widget
        #self.declared_fields["content"] = CharField(widget=widget, required=True)
        tag_ids = []
        if "instance" in kwargs:
            instance = kwargs["instance"]
            for tag in instance.tags.order_by("id"):
                tag_ids += ["%d" % tag.id]
            self.initial["pub_places"] = "_".join(tag_ids)    
        
    def save(self, **kwargs):
        tag_ids = self.cleaned_data["pub_places"].split("_")
        self.cleaned_data["tags"] = Tag.objects.filter(id__in = tag_ids).order_by("id")
        return super(NewsForm, self).save(**kwargs)
        
    class Meta:
        model = News
        fields = (
            "title",        
            "slug", 
            "is_published",
            "pub_places",
            "excerpt",
            "content",
            "pub_date",
            "unpub_date",
            "tags",
        )