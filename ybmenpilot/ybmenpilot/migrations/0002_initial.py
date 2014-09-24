# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Update'
        db.create_table(u'ybmenpilot_update', (
            ('post_id', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='')),
            ('date_posted', self.gf('django.db.models.fields.TextField')(default='', max_length=100)),
            ('time_posted', self.gf('django.db.models.fields.CharField')(default='', max_length=25)),
            ('link', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('person_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('imagecontent', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('num_comments_recd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_likes_recd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('addl_content', self.gf('django.db.models.fields.TextField')(default='')),
            ('application', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
        ))
        db.send_create_signal(u'ybmenpilot', ['Update'])

        # Adding model 'Participant'
        db.create_table(u'ybmenpilot_participant', (
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=4000)),
            ('birthday', self.gf('django.db.models.fields.CharField')(default='', max_length=12)),
            ('expirytoken', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('num_likes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('hometown', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal(u'ybmenpilot', ['Participant'])

        # Adding model 'GroupPost'
        db.create_table(u'ybmenpilot_grouppost', (
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='')),
            ('date_posted', self.gf('django.db.models.fields.CharField')(default='', max_length=25)),
            ('time_posted', self.gf('django.db.models.fields.CharField')(default='', max_length=25)),
            ('num_comments_recd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_likes_recd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_shares', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('link', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('imagecontent', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
        ))
        db.send_create_signal(u'ybmenpilot', ['GroupPost'])

        # Adding model 'GroupComment'
        db.create_table(u'ybmenpilot_groupcomment', (
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date_posted', self.gf('django.db.models.fields.DateField')()),
            ('time_posted', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('num_likes_recd', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ybmenpilot', ['GroupComment'])


    def backwards(self, orm):
        # Deleting model 'Update'
        db.delete_table(u'ybmenpilot_update')

        # Deleting model 'Participant'
        db.delete_table(u'ybmenpilot_participant')

        # Deleting model 'GroupPost'
        db.delete_table(u'ybmenpilot_grouppost')

        # Deleting model 'GroupComment'
        db.delete_table(u'ybmenpilot_groupcomment')


    models = {
        u'ybmenpilot.groupcomment': {
            'Meta': {'object_name': 'GroupComment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_posted': ('django.db.models.fields.DateField', [], {}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'num_likes_recd': ('django.db.models.fields.IntegerField', [], {}),
            'time_posted': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'ybmenpilot.grouppost': {
            'Meta': {'object_name': 'GroupPost'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_posted': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'imagecontent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'num_comments_recd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_likes_recd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_shares': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time_posted': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'})
        },
        u'ybmenpilot.participant': {
            'Meta': {'object_name': 'Participant'},
            'birthday': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '12'}),
            'expirytoken': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'hometown': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'num_likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '4000'})
        },
        u'ybmenpilot.update': {
            'Meta': {'object_name': 'Update'},
            'addl_content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'application': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'date_posted': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '100'}),
            'imagecontent': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'num_comments_recd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_likes_recd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'person_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'post_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'time_posted': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'})
        }
    }

    complete_apps = ['ybmenpilot']