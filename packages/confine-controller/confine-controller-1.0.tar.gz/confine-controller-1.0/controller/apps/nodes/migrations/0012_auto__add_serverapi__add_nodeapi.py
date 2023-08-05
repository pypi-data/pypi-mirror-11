# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("mgmtnetworks", "0002_datamigration_create_mgmt_net_for_existing_objects"),
    )

    def forwards(self, orm):
        # Adding model 'ServerApi'
        db.create_table(u'nodes_serverapi', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('base_uri', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('cert', self.gf('controller.models.fields.NullableTextField')(unique=True, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(related_name='api', to=orm['nodes.Server'])),
            ('island', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nodes.Island'], null=True, blank=True)),
        ))
        db.send_create_signal(u'nodes', ['ServerApi'])

        # Adding model 'NodeApi'
        db.create_table(u'nodes_nodeapi', (
            ('base_uri', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('cert', self.gf('controller.models.fields.NullableTextField')(unique=True, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='node', max_length=16)),
            ('node', self.gf('django.db.models.fields.related.OneToOneField')(related_name='api', unique=True, primary_key=True, to=orm['nodes.Node'])),
        ))
        db.send_create_signal(u'nodes', ['NodeApi'])


    def backwards(self, orm):
        # Deleting model 'ServerApi'
        db.delete_table(u'nodes_serverapi')

        # Deleting model 'NodeApi'
        db.delete_table(u'nodes_nodeapi')


    models = {
        u'nodes.directiface': {
            'Meta': {'unique_together': "(['name', 'node'],)", 'object_name': 'DirectIface'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'direct_ifaces'", 'to': u"orm['nodes.Node']"})
        },
        u'nodes.island': {
            'Meta': {'object_name': 'Island'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'nodes.node': {
            'Meta': {'object_name': 'Node'},
            'arch': ('django.db.models.fields.CharField', [], {'default': "'i686'", 'max_length': '16'}),
            'boot_sn': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'cert': ('controller.models.fields.NullableTextField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['users.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nodes.Island']", 'null': 'True', 'blank': 'True'}),
            'local_iface': ('django.db.models.fields.CharField', [], {'default': "'eth0'", 'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'priv_ipv4_prefix': ('controller.models.fields.NullableCharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'set_state': ('django.db.models.fields.CharField', [], {'default': "'debug'", 'max_length': '16'}),
            'sliver_mac_prefix': ('controller.models.fields.NullableCharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'sliver_pub_ipv4': ('django.db.models.fields.CharField', [], {'default': "'dhcp'", 'max_length': '8'}),
            'sliver_pub_ipv4_range': ('controller.models.fields.NullableCharField', [], {'default': "'#8'", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'sliver_pub_ipv6': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '8'})
        },
        u'nodes.nodeapi': {
            'Meta': {'object_name': 'NodeApi'},
            'base_uri': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'cert': ('controller.models.fields.NullableTextField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'api'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['nodes.Node']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'node'", 'max_length': '16'})
        },
        u'nodes.nodeprop': {
            'Meta': {'unique_together': "(('node', 'name'),)", 'object_name': 'NodeProp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'properties'", 'to': u"orm['nodes.Node']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'nodes.server': {
            'Meta': {'object_name': 'Server'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'nodes.serverapi': {
            'Meta': {'object_name': 'ServerApi'},
            'base_uri': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'cert': ('controller.models.fields.NullableTextField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'island': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nodes.Island']", 'null': 'True', 'blank': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api'", 'to': u"orm['nodes.Server']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'nodes.serverprop': {
            'Meta': {'unique_together': "(('server', 'name'),)", 'object_name': 'ServerProp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'properties'", 'to': u"orm['nodes.Server']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'users.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'allow_nodes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_slices': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        }
    }

    complete_apps = ['nodes']
