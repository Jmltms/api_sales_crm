# Generated by Django 4.2.13 on 2024-06-19 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_leadservices_revenue'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadservices',
            name='otf_payment',
            field=models.DateField(blank=True, null=True),
        ),
    ]
