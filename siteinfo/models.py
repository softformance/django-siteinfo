

import datetime
import warnings

from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from filer.fields.file import FilerFileField


# Create your models here.
class SiteSettingsManager(models.Manager):
    def get_current(self):
        site = Site.objects.get_current()
        try:
            # FUCK IT! not sure why, but i wasnt able to start saison server
            # because of this
            return site.site_settings.get_or_create(id__isnull=False, defaults={
                'site': site,
                'favicon': 'favicon.ico'
            })[0]
        except:
            # so i had add this try / except block
            try:
                return site.site_settings.filter(site=site)[0]
            except IndexError:
                return None


REQUIRE_LOGIN_CHOICES = (
    ('yes', _('login required')),
    ('staff', _('staff login required')),
)


@python_2_unicode_compatible
class SiteSettings(models.Model):
    site = models.ForeignKey(Site, related_name='site_settings', unique=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    active_start = models.DateTimeField(null=True, blank=True)
    active_end = models.DateTimeField(null=True, blank=True)

    description = models.TextField(_('site description'),
                                   help_text='%s %s' % (
                                       _('Keep between 150 and 1000 characters long.'),
                                       _('Important for search engine indexing.'),
                                   ), blank=True)
    keywords = models.TextField(_('site keywords'),
                                help_text='%s %s' % (
                                    _('Comma separated.'),
                                    _('Important for search engine indexing.'),
                                ), blank=True)
    site_topic = models.TextField(_('site topic'),
                                  help_text='%s %s' % (
                                      _('Keep between 150 and 1000 characters long.'),
                                      _('Important for search engine indexing.'),
                                  ), blank=True)
    company = models.CharField(_('company'), max_length=100, blank=True)
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)
    address = models.CharField(_('address'), max_length=100, blank=True)
    zip_code = models.PositiveSmallIntegerField(_('ZIP code'), blank=True, null=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    email = models.EmailField(_('email'), blank=True)
    phone = models.CharField(_('phone'), max_length=17, blank=True)
    phone_mobile = models.CharField(_('mobile phone'), max_length=17, blank=True)
    fax = models.CharField(_('fax'), max_length=17, blank=True)
    gtc_file = FilerFileField(verbose_name=_('GTC'),
                              help_text=_('Provide your "General Terms and Conditions" document for download.'),
                              blank=True, null=True)
    imprint = models.TextField(_('imprint'),
                               help_text=_('This imprint may be displayed at the bottom of your webpages.'), blank=True)
    favicon = models.FileField(_('favicon'), help_text=_(
        'Provide an image (Windows icon image, 16 x 16 pixels) which is used in browser bookmarks and such.'),
                               upload_to="uploads", blank=True)
    require_login = models.CharField(_('require login'),
                                     help_text=_('Choose if a valid login is needed to view this site'),
                                     choices=REQUIRE_LOGIN_CHOICES, max_length=10, blank=True)
    geoip_redirect = models.BooleanField(
        _('GeoIP redirect'),
        default=False,
        help_text=_('If GeoIP redirection is enabled for your deployment, '
                    'visitors of this site are being redirected to the configured country sites.'))
    inactive_image = models.ImageField(_('inactive image'),
                                       help_text=_('Provide an image that will be displayed when the site is inactive'),
                                       upload_to="uploads", blank=True)
    inactive_text = models.TextField(_('inactive text'),
                                     help_text=_('This text will be displayed when the site is set to inactive'),
                                     blank=True)

    objects = SiteSettingsManager()

    class Meta:
        verbose_name = _('site settings')
        verbose_name_plural = _('site settings')

    def __str__(self):
        return _('for site %s') % str(self.site)

    def get_full_address(self, separator="<br />"):
        address = "%s%s%s %s" % (self.address, separator, self.zip_code or "", self.city)
        return mark_safe(address)

    def is_active_now(self):
        now = datetime.datetime.now()
        return self.is_active_on_date(now)

    def is_active_on_date(self, on_date):
        if self.active:
            if self.active_start and self.active_start > on_date:
                return False
            if self.active_end and self.active_end < on_date:
                return False
            return True
        else:
            return False

    @property
    def author(self):
        if self.company and self.last_name and self.first_name:
            return '%s, %s %s' % (self.company, self.first_name, self.last_name)
        elif self.company and self.last_name and not self.first_name:
            return '%s, %s' % (self.company, self.last_name)
        else:
            return '%s%s' % (self.last_name and self.last_name + ', ', self.first_name)

    @property
    def email_local_part(self):
        if not self.email and not '@' in self.email:
            return ''
        return self.email.split('@')[0]

    @property
    def email_domain_part(self):
        if not self.email and '@' not in self.email:
            return ''
        return self.email.split('@')[1]

    @property
    def gtc(self):
        """
        for backward compatibility.
        """
        warnings.warn("django-siteinfo: the sitesettings.gtc property is depreciated. please use sitesettings.gtc_file",
                      DeprecationWarning)
        return getattr(self.gtc_file, 'file', None)


@python_2_unicode_compatible
class SiteAliasSettings(models.Model):
    site = models.ForeignKey(Site, related_name='sitealias_settings', on_delete=models.CASCADE)
    domain_alias = models.CharField(max_length=100, unique=True, help_text=_('Without www.'))
    google_maps_api_key = models.CharField(max_length=255, blank=True)
    google_analytics_id = models.CharField(max_length=20,
                                           help_text=_('Google Analytics Web Property-ID for this site.'), blank=True)
    google_webmasters_verifytag = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = _('site alias settings')
        verbose_name_plural = _('site alias settings')

    def __str__(self):
        return 'Site alias %s' % self.domain_alias
