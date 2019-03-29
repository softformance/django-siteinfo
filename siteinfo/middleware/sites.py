import re

from django.contrib.sites.models import Site
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured

from siteinfo.models import SiteAliasSettings, SiteSettings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class SiteRedirectMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(SiteRedirectMiddleware, self).__init__(*args, **kwargs)

        if getattr(settings, 'IS_DEV_SERVER', False) or 'django.contrib.sites' not in settings.INSTALLED_APPS:
            raise MiddlewareNotUsed()

    def process_request(self, request):
        host = request.get_host()
        site = Site.objects.get_current()

        try:
            if site.domain in host:
                return None
            else:
                site_alias = SiteAliasSettings.objects.filter(site=site, domain_alias__iendswith=host)
                if site_alias.count():
                    if site_alias[0].domain_alias == host:
                        return None
                    redirect_to = site_alias[0].domain_alias
                else:
                    redirect_to = site.domain
        except:
            return None
        return HttpResponsePermanentRedirect('%s://%s%s' % (
            request.is_secure() and 'https' or 'http',
            redirect_to,
            request.get_full_path(),
        ))


class GeoIPRedirectMiddleware(MiddlewareMixin):
    """
    GeoIP redirect middleware. If enabled, the middleware determines the 
    visitor's location by checking his REMOTE_ADDR with the GeoIP DB 
    (working GeoIP setup required, see: 'django.contrib.gis.utils.geoip.py').
    The determined country code is checked against 'settings.SITE_GEOIP_REDIRECT', 
    which must be a list of 2-tuples with iso country code 
    (see: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) and corresponding site_id.
    If a matching country_code setting is found, a redirect (302) is issued to the
    site's domain. 
    Author: Maik LUSTENBERGER, Divio GmbH, 2009
    """

    def __init__(self, *args, **kwargs):
        super(GeoIPRedirectMiddleware, self).__init__(*args, **kwargs)

        if getattr(settings, 'IS_DEV_SERVER', False) or 'django.contrib.sites' not in settings.INSTALLED_APPS:
            raise MiddlewareNotUsed()
        try:
            from django.contrib.gis.utils import GeoIP, GeoIPException
            self.g = GeoIP()
            self.redirect_sites = dict(settings.SITE_GEOIP_REDIRECT)
        except (ImportError, GeoIPException, ValueError, TypeError, AttributeError):
            raise ImproperlyConfigured(
                "The GeoIPRedirectMiddleware requires the"
                " setting SITE_GEOIP_REDIRECT and GEOIP_PATH to be defined"
                " along with a working GeoIP installation."
                " Please see 'django.contrib.gis.utils.geoip.py'.")
        self.srs_url_re = re.compile("^/siteinfo/srs/?$")
        self.srs_getvarname = getattr(settings, 'SITE_GEOIP_REDIRECT_GETVARNAME', 'srs')

    def process_request(self, request):
        assert hasattr(request, 'session'), \
            "The 'GeoIPRedirectMiddleware' requires the app" \
            " 'django.contrib.sessions' to be in INSTALLED_APPS." \
            " Also make sure that 'GeoIPRedirectMiddleware' comes" \
            " after 'django.contrib.sessions.middleware.SessionMiddleware'" \
            " in the setting 'MIDDLEWARE_CLASSES'."
        site_settings = SiteSettings.objects.get_current()
        if not site_settings.geoip_redirect:
            return None
        if self.srs_url_re.match(request.path):
            return None
        if request.GET.get(self.srs_getvarname, False):
            # Var ?srs=1 is in GET.
            # Set session key. ATTENTION: This does not work, if a subsequent request middleware does a redirect!
            request.session['site_redirect_stop'] = True
            return None
        if request.session.get('site_redirect_stop', False):
            # The redirect stop flag has been set by 'siteinfo.views.set_redirect_stop'
            return None
        if getattr(settings, 'SITE_GEOIP_REDIRECT_ONCE', True):
            if request.session.get('site_no_redirect', False):
                # Redirect info already lives in session. No need for redirect. So no further action.
                return None
            if request.COOKIES.get('site_no_redirect', False):
                # Redirect has already occurred. Write cookie info to session for accurate lifetime.
                request.session['site_no_redirect'] = True
                return None
        if getattr(settings, 'SITE_GEOIP_REDIRECT_ROOT_ONLY', True) and request.get_full_path() != '/':
            return None

        # Start with the geo action.
        ip = request.META.get('REMOTE_ADDR')
        geo_info = self.g.country(ip)
        try:
            country_code = geo_info['country_code'].lower()
        except (KeyError, AttributeError):
            return None
        if country_code in self.redirect_sites:
            site_id = self.redirect_sites[country_code]
            try:
                site = Site.objects.get(pk=site_id)
            except Site.DoesNotExist:
                return None
            host = request.get_host()
            if site.domain in host:
                return None
            if getattr(settings, 'SITE_GEOIP_REDIRECT_TO_FULL_PATH', False):
                path = request.get_full_path()
            else:
                path = ''
            response = HttpResponseRedirect('%s://%s%s' % (
                request.is_secure() and 'https' or 'http',
                site.domain,
                path,
            ))
            if getattr(settings, 'SITE_GEOIP_REDIRECT_ONCE', True):
                # Set a cookie for the lifetime of a (new) session, to let subsequent requests know of the redirect.
                # Also, subsequent requests will write this cookie information to the session for accurate lifetime.
                response.set_cookie(
                    'site_no_redirect',
                    '1',
                    max_age=(not settings.SESSION_EXPIRE_AT_BROWSER_CLOSE or None) and settings.SESSION_COOKIE_AGE
                )
            return response
