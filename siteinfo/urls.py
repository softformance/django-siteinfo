import django
from django.conf import settings
from django.contrib.auth import views as auth_views

from siteinfo import views as siteinfo_views
from siteinfo.models import SiteSettings

site_settings = SiteSettings.objects.get_current()

if site_settings:
    agb_url = 'http://%s%s%s' % (site_settings.site.domain, settings.MEDIA_URL, site_settings.gtc)
else:
    agb_url = ""


if django.VERSION < (1, 8):
    try:
        from django.conf.urls.defaults import patterns, url
    except:
        from django.conf.urls import patterns, url

    urlpatterns = patterns('',
                           url(r'^login/$', auth_views.login, name='login_url'),
                           url(r'^logout/$', auth_views.logout, name='logout_url'),

                           url(r'^srs/?$', siteinfo_views.set_redirect_stop, name='set_redirect_stop'),
                           url(r'^test_offline_page/?$', siteinfo_views.test_offline_page,
                               name='siteinfo-test_offline_page'),
                           )
    if django.VERSION < (1, 5):
        urlpatterns += patterns('',
            url(r'^agb/?$', django.views.generic.simple.redirect_to, {'url': agb_url}, name="agb"),
        )
    else:
        from django.views.generic.base import RedirectView

        urlpatterns += patterns('',
            url(r'^agb/?$', RedirectView.as_view(url=agb_url), name="agb"),
        )

else:
    from django.conf.urls import url
    from django.views.generic import RedirectView

    urlpatterns = [
        url(r'^login/$', auth_views.login, name='login_url'),
        url(r'^logout/$', auth_views.logout, name='logout_url'),
        url(r'^agb/?$', RedirectView.as_view(url=agb_url), name="agb"),
        url(r'^srs/?$', siteinfo_views.set_redirect_stop, name='set_redirect_stop'),
        url(r'^test_offline_page/?$', siteinfo_views.test_offline_page, name='siteinfo-test_offline_page'),
    ]
