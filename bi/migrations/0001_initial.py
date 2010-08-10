
from south.db import db
from django.db import models
from bi.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'QueryCondition'
        db.create_table('bi_querycondition', (
            ('id', models.AutoField(primary_key=True)),
            ('query', models.ForeignKey(orm.Query)),
            ('expression', models.CharField(max_length=200)),
        ))
        db.send_create_signal('bi', ['QueryCondition'])
        
        # Adding model 'Query'
        db.create_table('bi_query', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.SlugField(unique=True)),
            ('title', models.CharField(max_length=50, blank=True)),
            ('kind', models.CharField(default='visual', max_length=10, db_index=True, blank=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], null=True, blank=True)),
            ('limit', models.IntegerField(default=0, blank=True)),
            ('url', models.CharField(default='', max_length=200)),
        ))
        db.send_create_signal('bi', ['Query'])
        
        # Adding model 'QueryField'
        db.create_table('bi_queryfield', (
            ('id', models.AutoField(primary_key=True)),
            ('query', models.ForeignKey(orm.Query)),
            ('name', models.CharField(max_length=50, db_index=True)),
            ('title', models.CharField(max_length=50, blank=True)),
            ('kind', models.CharField(default='value', max_length=10, db_index=True, blank=True)),
            ('expression', models.TextField(blank=True)),
            ('sequence', models.SmallIntegerField(default=0, blank=True)),
            ('choices', models.TextField(blank=True)),
        ))
        db.send_create_signal('bi', ['QueryField'])
        
        # Adding model 'QueryOrder'
        db.create_table('bi_queryorder', (
            ('id', models.AutoField(primary_key=True)),
            ('query', models.ForeignKey(orm.Query)),
            ('field_name', models.CharField(max_length=50)),
            ('kind', models.CharField(default='', max_length=1, db_index=True, blank=True)),
        ))
        db.send_create_signal('bi', ['QueryOrder'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'QueryCondition'
        db.delete_table('bi_querycondition')
        
        # Deleting model 'Query'
        db.delete_table('bi_query')
        
        # Deleting model 'QueryField'
        db.delete_table('bi_queryfield')
        
        # Deleting model 'QueryOrder'
        db.delete_table('bi_queryorder')
        
    
    
    models = {
        'bi.queryorder': {
            'field_name': ('models.CharField', [], {'max_length': '50'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'kind': ('models.CharField', [], {'default': "''", 'max_length': '1', 'db_index': 'True', 'blank': 'True'}),
            'query': ('models.ForeignKey', ["orm['bi.Query']"], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'bi.query': {
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'kind': ('models.CharField', [], {'default': "'visual'", 'max_length': '10', 'db_index': 'True', 'blank': 'True'}),
            'limit': ('models.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'name': ('models.SlugField', [], {'unique': 'True'}),
            'title': ('models.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'url': ('models.CharField', [], {'default': "''", 'max_length': '200'})
        },
        'bi.queryfield': {
            'Meta': {'ordering': "('sequence',)"},
            'choices': ('models.TextField', [], {'blank': 'True'}),
            'expression': ('models.TextField', [], {'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'kind': ('models.CharField', [], {'default': "'value'", 'max_length': '10', 'db_index': 'True', 'blank': 'True'}),
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
