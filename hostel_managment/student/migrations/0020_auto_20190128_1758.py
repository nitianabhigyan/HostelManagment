# Generated by Django 2.0.5 on 2019-01-28 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0019_auto_20190128_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application_db',
            options={'verbose_name': 'Application', 'verbose_name_plural': 'Applications Managment'},
        ),
        migrations.AlterModelOptions(
            name='complaints_db',
            options={'verbose_name': 'Complaint ', 'verbose_name_plural': 'Complaints Managment'},
        ),
    ]
