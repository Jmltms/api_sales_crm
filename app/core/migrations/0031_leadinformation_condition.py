# Generated by Django 4.2.13 on 2024-05-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_alter_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadinformation',
            name='condition',
            field=models.IntegerField(choices=[(1, 'active'), (2, 'deleted')], default=1),
        ),
    ]