# Generated by Django 2.0.5 on 2018-08-26 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_auto_20180826_2303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complaints_db',
            old_name='student_regn_no',
            new_name='regn_no',
        ),
    ]
