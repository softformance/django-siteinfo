from django.db import migrations, models
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteAliasSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain_alias', models.CharField(help_text='Without www.', unique=True, max_length=100)),
                ('google_maps_api_key', models.CharField(max_length=255, blank=True)),
                ('google_analytics_id', models.CharField(help_text='Google Analytics Web Property-ID for this site.', max_length=20, blank=True)),
                ('google_webmasters_verifytag', models.CharField(max_length=100, blank=True)),
                ('site', models.ForeignKey(related_name='sitealias_settings', to='sites.Site', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'site alias settings',
                'verbose_name_plural': 'site alias settings',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('active_start', models.DateTimeField(null=True, blank=True)),
                ('active_end', models.DateTimeField(null=True, blank=True)),
                ('description', models.TextField(help_text='Keep between 150 and 1000 characters long. Important for search engine indexing.', verbose_name='site description', blank=True)),
                ('keywords', models.TextField(help_text='Comma separated. Important for search engine indexing.', verbose_name='site keywords', blank=True)),
                ('site_topic', models.TextField(help_text='Keep between 150 and 1000 characters long. Important for search engine indexing.', verbose_name='site topic', blank=True)),
                ('company', models.CharField(max_length=100, verbose_name='company', blank=True)),
                ('first_name', models.CharField(max_length=100, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=100, verbose_name='last name', blank=True)),
                ('address', models.CharField(max_length=100, verbose_name='address', blank=True)),
                ('zip_code', models.PositiveSmallIntegerField(null=True, verbose_name='ZIP code', blank=True)),
                ('city', models.CharField(max_length=100, verbose_name='city', blank=True)),
                ('country', models.CharField(max_length=100, verbose_name='country', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email', blank=True)),
                ('phone', models.CharField(max_length=17, verbose_name='phone', blank=True)),
                ('phone_mobile', models.CharField(max_length=17, verbose_name='mobile phone', blank=True)),
                ('fax', models.CharField(max_length=17, verbose_name='fax', blank=True)),
                ('imprint', models.TextField(help_text='This imprint may be displayed at the bottom of your webpages.', verbose_name='imprint', blank=True)),
                ('favicon', models.FileField(help_text='Provide an image (Windows icon image, 16 x 16 pixels) which is used in browser bookmarks and such.', upload_to=b'uploads', verbose_name='favicon', blank=True)),
                ('require_login', models.CharField(blank=True, help_text='Choose if a valid login is needed to view this site', max_length=10, verbose_name='require login', choices=[(b'yes', 'login required'), (b'staff', 'staff login required')])),
                ('geoip_redirect', models.BooleanField(default=False, help_text='If GeoIP redirection is enabled for your deployment, visitors of this site are being redirected to the configured country sites.', verbose_name='GeoIP redirect')),
                ('inactive_image', models.ImageField(help_text='Provide an image that will be displayed when the site is inactive', upload_to=b'uploads', verbose_name='inactive image', blank=True)),
                ('inactive_text', models.TextField(help_text='This text will be displayed when the site is set to inactive', verbose_name='inactive text', blank=True)),
                ('gtc_file', filer.fields.file.FilerFileField(blank=True, to='filer.File', help_text='Provide your "General Terms and Conditions" document for download.', null=True, verbose_name='GTC', on_delete=models.SET_NULL)),
                ('site', models.ForeignKey(related_name='site_settings', to='sites.Site', unique=True, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'site settings',
                'verbose_name_plural': 'site settings',
            },
        ),
    ]
