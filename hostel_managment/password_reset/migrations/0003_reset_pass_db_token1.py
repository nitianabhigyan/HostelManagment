# Generated by Django 2.0.5 on 2018-10-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('password_reset', '0002_auto_20181006_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='reset_pass_db',
            name='token1',
            field=models.CharField(max_length=35, null=True),
        ),
    ]
