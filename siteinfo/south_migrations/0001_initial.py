from south.db import db
from django.db import models
from siteinfo.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'SiteAliasSettings'
        db.create_table('siteinfo_sitealiassettings', (
            ('id', orm['siteinfo.SiteAliasSettings:id']),
            ('site', orm['siteinfo.SiteAliasSettings:site']),
            ('domain_alias', orm['siteinfo.SiteAliasSettings:domain_alias']),
            ('google_maps_api_key', orm['siteinfo.SiteAliasSettings:google_maps_api_key']),
            ('google_analytics_id', orm['siteinfo.SiteAliasSettings:google_analytics_id']),
            ('google_webmasters_verifytag', orm['siteinfo.SiteAliasSettings:google_webmasters_verifytag']),
        ))
        db.send_create_signal('siteinfo', ['SiteAliasSettings'])
        
        # Adding model 'SiteSettings'
        db.create_table('siteinfo_sitesettings', (
            ('id', orm['siteinfo.SiteSettings:id']),
            ('site', orm['siteinfo.SiteSettings:site']),
            ('active', orm['siteinfo.SiteSettings:active']),
            ('description', orm['siteinfo.SiteSettings:description']),
            ('keywords', orm['siteinfo.SiteSettings:keywords']),
            ('site_topic', orm['siteinfo.SiteSettings:site_topic']),
            ('company', orm['siteinfo.SiteSettings:company']),
            ('first_name', orm['siteinfo.SiteSettings:first_name']),
            ('last_name', orm['siteinfo.SiteSettings:last_name']),
            ('address', orm['siteinfo.SiteSettings:address']),
            ('zip_code', orm['siteinfo.SiteSettings:zip_code']),
            ('city', orm['siteinfo.SiteSettings:city']),
            ('country', orm['siteinfo.SiteSettings:country']),
            ('email', orm['siteinfo.SiteSettings:email']),
            ('phone', orm['siteinfo.SiteSettings:phone']),
            ('phone_mobile', orm['siteinfo.SiteSettings:phone_mobile']),
            ('fax', orm['siteinfo.SiteSettings:fax']),
            ('gtc', orm['siteinfo.SiteSettings:gtc']),
            ('imprint', orm['siteinfo.SiteSettings:imprint']),
            ('favicon', orm['siteinfo.SiteSettings:favicon']),
            ('require_login', orm['siteinfo.SiteSettings:require_login']),
        ))
        db.send_create_signal('siteinfo', ['SiteSettings'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'SiteAliasSettings'
        db.delete_table('siteinfo_sitealiassettings')
        
        # Deleting model 'SiteSettings'
        db.delete_table('siteinfo_sitesettings')
        
    
    
    models = {
        'siteinfo.sitealiassettings': {
            'domain_alias': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
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
            'gtc': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imprint': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
