# Generated by Django 2.0.5 on 2019-01-27 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry_exit', '0009_auto_20190127_2322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student_still_out',
            old_name='is_complete',
            new_name='is_completed',
        ),
    ]
