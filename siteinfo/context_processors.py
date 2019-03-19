import datetime

from django.contrib.sites.models import Site
from django.conf import settings

from siteinfo.models import SiteSettings, SiteAliasSettings
from siteinfo.util import MetaTag


def siteinfo(request):
    context = {}
    site = Site.objects.get_current()
    site_settings = SiteSettings.objects.get_current()
    if site_settings:
        meta_tags = [
            MetaTag(name='', content='no', http_equiv='imagetoolbar'),
            MetaTag(name='generator', content='http://' + site.domain),
            MetaTag(name='page-topic', content=site_settings.site_topic),
            MetaTag(name='author', content=site_settings.author or site.name),
            MetaTag(name='publisher', content=site_settings.author or site.name),
            MetaTag(name='copyright', content=site_settings.author or site.name),
            MetaTag(name='date', content=datetime.datetime.now().strftime('%Y-%m-%d')),
            MetaTag(name='Last-Modified', content=datetime.datetime.now().strftime('%Y-%m-%d')),

            MetaTag(name='expires', content='0'),
            MetaTag(name='audience', content='all'),
            MetaTag(name='page-type', content=site.name),
            MetaTag(name='robots', content='index,follow,noodp'),
            MetaTag(name='revisit-after', content='14'),
        ]

        language_code = getattr(request, 'LANGUAGE_CODE', None)
        if language_code is not None:
            meta_tags.append(
                MetaTag(name='content-language', content=language_code))

        description = ""
        keywords = ""
        if "cms" in settings.INSTALLED_APPS:
            if hasattr(request, 'current_page'):
                page = request.current_page
                if hasattr(page, "get_meta_description"):
                    description = page.get_meta_description()
        if not description:
            description = site_settings.description
        if not keywords:
            keywords = site_settings.keywords     
        if description:
            meta_tags.append(MetaTag(name='description', content=description))
        if keywords:
            meta_tags.append(MetaTag(name='keywords', content=keywords))
    
        # Google Conf
        try:
            sitealias_settings_qs = site.sitealias_settings.filter(domain_alias__iendswith=request.get_host().lower())
            if sitealias_settings_qs:
                sitealias_settings = sitealias_settings_qs[0]
                context['GOOGLE_ANALYTICS_ID'] = sitealias_settings.google_analytics_id
                context['GOOGLE_MAPS_API_KEY'] = sitealias_settings.google_maps_api_key
                if sitealias_settings.google_webmasters_verifytag:
                    meta_tags.append(MetaTag(name='google-site-verification', content=sitealias_settings.google_webmasters_verifytag))
                    context['GOOGLE_SITE_VERIFICATION'] = sitealias_settings.google_webmasters_verifytag
        except SiteAliasSettings.DoesNotExist:
            context['GOOGLE_ANALYTICS_ID'] = context['GOOGLE_MAPS_API_KEY'] = None
        context['meta_tags'] = meta_tags
        context['site_settings'] = site_settings
    return context
