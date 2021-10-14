from south.db import db
from django.db import models
from siteinfo.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'SiteSettings.inactive_text'
        db.add_column('siteinfo_sitesettings', 'inactive_text', orm['siteinfo.sitesettings:inactive_text'])
        
        # Adding field 'SiteSettings.inactive_image'
        db.add_column('siteinfo_sitesettings', 'inactive_image', orm['siteinfo.sitesettings:inactive_image'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'SiteSettings.inactive_text'
        db.delete_column('siteinfo_sitesettings', 'inactive_text')
        
        # Deleting field 'SiteSettings.inactive_image'
        db.delete_column('siteinfo_sitesettings', 'inactive_image')
        
    
    
    models = {
        'siteinfo.sitealiassettings': {
            'domain_alias': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'google_analytics_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'google_maps_api_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'google_webmasters_verifytag': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sitealias_settings'", 'to': "orm['sites.Site']"})
        },
        'siteinfo.sitesettings': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'favicon': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'geoip_redirect': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'gtc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imprint': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'inactive_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'inactive_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'phone_mobile': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'require_login': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'site_settings'", 'unique': 'True', 'to': "orm['sites.Site']"}),
            'site_topic': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'zip_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['siteinfo']
