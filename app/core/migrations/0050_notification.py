# Generated by Django 4.2.13 on 2024-07-16 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_termstatus_msf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.IntegerField(choices=[(1, 'new leads')], default=1)),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'active'), (2, 'deleted')], default=1)),
                ('is_seen', models.BooleanField(default=False)),
                ('date_deliver', models.DateTimeField(blank=True, null=True)),
                ('date_seen', models.DateTimeField(blank=True, null=True)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to='core.account')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to='core.account')),
            ],
        ),
    ]
