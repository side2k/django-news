import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class PublishedNewsManager(models.Manager):
    """
        Filters out all unpublished and items with a publication date in the future
    """
    def get_query_set(self):
        return super(PublishedNewsManager, self).get_query_set() \
                    .filter(is_published=True) \
                    .filter(pub_date__lte=datetime.datetime.now()) \
                    .filter(Q(unpub_date__exact=None) | Q(unpub_date__gt=datetime.datetime.now()))
    
class News(models.Model):
    """
    News
    """
    
    title           = models.CharField(_('Title'), max_length=255)
    title.pub_place_filter = True
    slug            = models.SlugField(_('Slug'), unique_for_date='pub_date', 
                        help_text=_('A slug is a short name which uniquely identifies the news item for this day'))
    excerpt         = models.TextField(_('Excerpt'), blank=True)
    content         = models.TextField(_('Content'), blank=True)
    
    is_published    = models.BooleanField(_('Published'), default=False)
    pub_date        = models.DateTimeField(_('Publication date'), default=datetime.datetime.now())
    unpub_date      = models.DateTimeField(_('Unpublication date'), default=None, null=True, blank=True)
    
    created         = models.DateTimeField(auto_now_add=True, editable=False)
    updated         = models.DateTimeField(auto_now=True, editable=False)
    
    published = PublishedNewsManager()
    objects = models.Manager()
	
	#tags field
    tags			= models.ManyToManyField("tagging.Tag", verbose_name=_("Tags"))

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ('-pub_date', )
    
    def pub_place(self):
        result = _("Not specified")
        tag_ids = []
        for tag in self.tags.all():
            tag_ids += ["%d" % tag.id]
        tag_ids = "_".join(tag_ids)
        for (place_code, place_name) in settings.PUBLICATION_PLACES:
            if place_code == tag_ids:
                result = place_name
                break
        return result
        
    def __unicode__(self):
        return self.title
    @models.permalink
    def get_absolute_url(self):
        return ('news_detail', (), { 'year': self.pub_date.strftime("%Y"),
                                     'month': self.pub_date.strftime("%m"),
                                     'day': self.pub_date.strftime("%d"),
                                     'slug': self.slug })