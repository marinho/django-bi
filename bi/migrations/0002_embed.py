
from south.db import db
from django.db import models
from bi.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Query.embed_html'
        db.add_column('bi_query', 'embed_html', models.TextField(blank=True, default=''))
        
        # Changing field 'Query.url'
        db.alter_column('bi_query', 'url', models.CharField(default='', max_length=200, blank=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Query.embed_html'
        db.delete_column('bi_query', 'embed_html')
        
        # Changing field 'Query.url'
        db.alter_column('bi_query', 'url', models.CharField(default='', max_length=200))
        
    
    
    models = {
        'bi.queryorder': {
            'field_name': ('models.CharField', [], {'max_length': '50'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'kind': ('models.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True', 'db_index': 'True'}),
            'query': ('models.ForeignKey', ["orm['bi.Query']"], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'bi.query': {
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'null': 'True', 'blank': 'True'}),
            'embed_html': ('models.TextField', [], {'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'kind': ('models.CharField', [], {'default': "'visual'", 'max_length': '10', 'blank': 'True', 'db_index': 'True'}),
            'limit': ('models.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'name': ('models.SlugField', [], {'unique': 'True'}),
            'title': ('models.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'url': ('models.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'bi.queryfield': {
            'Meta': {'ordering': "('sequence',)"},
            'choices': ('models.TextField', [], {'blank': 'True'}),
            'expression': ('models.TextField', [], {'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'kind': ('models.CharField', [], {'default': "'value'", 'max_length': '10', 'blank': 'True', 'db_index': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'query': ('models.ForeignKey', ["orm['bi.Query']"], {}),
            'sequence': ('models.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('models.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'bi.querycondition': {
            'expression': ('models.CharField', [], {'max_length': '200'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'query': ('models.ForeignKey', ["orm['bi.Query']"], {})
        }
    }
    
    complete_apps = ['bi']
