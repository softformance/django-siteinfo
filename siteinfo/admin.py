from django.contrib.sites.admin import SiteAdmin
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.admin.sites import NotRegistered
from django.contrib.admin.options import InlineModelAdmin, StackedInline, TabularInline

from siteinfo.models import SiteSettings, SiteAliasSettings

class SiteSettingsInlineAdmin(StackedInline):
    model = SiteSettings
    max_num = 1

class SiteAliasSettingsInlineAdmin(TabularInline):
    model = SiteAliasSettings

class ExtendedSiteAdmin(SiteAdmin):
    inlines = [
        SiteSettingsInlineAdmin,
        SiteAliasSettingsInlineAdmin,
    ]

try:
    admin.site.unregister(Site)
except NotRegistered:
    raise
admin.site.register(Site, ExtendedSiteAdmin)
