import django
from django.conf import settings
from django.contrib.auth import views as auth_views

from siteinfo import views as siteinfo_views
from siteinfo.models import SiteSettings
from django.urls import path, re_path
from django.views.generic import RedirectView

site_settings = SiteSettings.objects.get_current()

if site_settings:
    agb_url = 'http://%s%s%s' % (site_settings.site.domain, settings.MEDIA_URL, site_settings.gtc)
else:
    agb_url = ""


urlpatterns = [
    path('login/', auth_views.login, name='login_url'),
    path('logout/', auth_views.logout, name='logout_url'),
    re_path(r'^agb/?$', RedirectView.as_view(url=agb_url), name="agb"),
    re_path(r'^srs/?$', siteinfo_views.set_redirect_stop, name='set_redirect_stop'),
    re_path(r'^test_offline_page/?$', siteinfo_views.test_offline_page, name='siteinfo-test_offline_page'),
]
