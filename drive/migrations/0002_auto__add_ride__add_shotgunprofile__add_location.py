# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ride'
        db.create_table(u'drive_ride', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('driver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('fromLocation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ride_from_set', to=orm['drive.Location'])),
            ('toLocation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ride_to_set', to=orm['drive.Location'])),
            ('leavingOn', self.gf('django.db.models.fields.DateField')()),
            ('gasMoney', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('luggageRoom', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'drive', ['Ride'])

        # Adding model 'ShotgunProfile'
        db.create_table(u'drive_shotgunprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
        ))
        db.send_create_signal(u'drive', ['ShotgunProfile'])

        # Adding model 'Location'
        db.create_table(u'drive_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=6)),
            ('formatted_address', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'drive', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Ride'
        db.delete_table(u'drive_ride')

        # Deleting model 'ShotgunProfile'
        db.delete_table(u'drive_shotgunprofile')

        # Deleting model 'Location'
        db.delete_table(u'drive_location')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'drive.location': {
            'Meta': {'object_name': 'Location'},
            'formatted_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '6'})
        },
        u'drive.ride': {
            'Meta': {'object_name': 'Ride'},
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'fromLocation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ride_from_set'", 'to': u"orm['drive.Location']"}),
            'gasMoney': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leavingOn': ('django.db.models.fields.DateField', [], {}),
            'luggageRoom': ('django.db.models.fields.IntegerField', [], {}),
            'toLocation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ride_to_set'", 'to': u"orm['drive.Location']"})
        },
        u'drive.shotgunprofile': {
            'Meta': {'object_name': 'ShotgunProfile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['drive']