# Generated by Django 2.0.5 on 2019-01-28 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_auto_20181028_2049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application_db',
            options={'verbose_name': 'Applications Managment'},
        ),
        migrations.AlterModelOptions(
            name='complaints_db',
            options={'verbose_name': 'Complaint Managment', 'verbose_name_plural': 'Complaints Managment'},
        ),
    ]
