# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Kiosk'
        db.create_table(u'woistbier_rest_kiosk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=600, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('geo_lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=10, blank=True)),
            ('geo_long', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=10, blank=True)),
            ('is_valid_address', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'woistbier_rest', ['Kiosk'])

        # Adding unique constraint on 'Kiosk', fields ['city', 'street', 'number', 'zip_code']
        db.create_unique(u'woistbier_rest_kiosk', ['city', 'street', 'number', 'zip_code'])

        # Adding model 'Beer'
        db.create_table(u'woistbier_rest_beer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brew', self.gf('django.db.models.fields.CharField')(default='pils', max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'woistbier_rest', ['Beer'])

        # Adding model 'Comment'
        db.create_table(u'woistbier_rest_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Anonymer Alkoholiker', max_length=25)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('kiosk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['woistbier_rest.Kiosk'])),
        ))
        db.send_create_signal(u'woistbier_rest', ['Comment'])

        # Adding model 'BeerPrice'
        db.create_table(u'woistbier_rest_beerprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.FloatField')(default=0.5, max_length=1)),
            ('kiosk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_kiosk', to=orm['woistbier_rest.Kiosk'])),
            ('beer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_beer', to=orm['woistbier_rest.Beer'])),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('score', self.gf('django.db.models.fields.FloatField')(default=1, max_length=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'woistbier_rest', ['BeerPrice'])

        # Adding unique constraint on 'BeerPrice', fields ['beer', 'kiosk', 'size']
        db.create_unique(u'woistbier_rest_beerprice', ['beer_id', 'kiosk_id', 'size'])

        # Adding model 'Image'
        db.create_table(u'woistbier_rest_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=300, blank=True)),
            ('kiosk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['woistbier_rest.Kiosk'])),
        ))
        db.send_create_signal(u'woistbier_rest', ['Image'])


    def backwards(self, orm):
        # Removing unique constraint on 'BeerPrice', fields ['beer', 'kiosk', 'size']
        db.delete_unique(u'woistbier_rest_beerprice', ['beer_id', 'kiosk_id', 'size'])

        # Removing unique constraint on 'Kiosk', fields ['city', 'street', 'number', 'zip_code']
        db.delete_unique(u'woistbier_rest_kiosk', ['city', 'street', 'number', 'zip_code'])

        # Deleting model 'Kiosk'
        db.delete_table(u'woistbier_rest_kiosk')

        # Deleting model 'Beer'
        db.delete_table(u'woistbier_rest_beer')

        # Deleting model 'Comment'
        db.delete_table(u'woistbier_rest_comment')

        # Deleting model 'BeerPrice'
        db.delete_table(u'woistbier_rest_beerprice')

        # Deleting model 'Image'
        db.delete_table(u'woistbier_rest_image')


    models = {
        u'woistbier_rest.beer': {
            'Meta': {'object_name': 'Beer'},
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'brew': ('django.db.models.fields.CharField', [], {'default': "'pils'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'woistbier_rest.beerprice': {
            'Meta': {'unique_together': "(('beer', 'kiosk', 'size'),)", 'object_name': 'BeerPrice'},
            'beer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_beer'", 'to': u"orm['woistbier_rest.Beer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kiosk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_kiosk'", 'to': u"orm['woistbier_rest.Kiosk']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '1', 'max_length': '1'}),
            'size': ('django.db.models.fields.FloatField', [], {'default': '0.5', 'max_length': '1'})
        },
        u'woistbier_rest.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kiosk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['woistbier_rest.Kiosk']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Anonymer Alkoholiker'", 'max_length': '25'})
        },
        u'woistbier_rest.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '300', 'blank': 'True'}),
            'kiosk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['woistbier_rest.Kiosk']"})
        },
        u'woistbier_rest.kiosk': {
            'Meta': {'unique_together': "(('city', 'street', 'number', 'zip_code'),)", 'object_name': 'Kiosk'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True', 'blank': 'True'}),
            'geo_lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '10', 'blank': 'True'}),
            'geo_long': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_valid_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['woistbier_rest']