# Generated by Django 2.0.5 on 2019-01-27 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_student_db_room_no'),
        ('entry_exit', '0004_student_still_out'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='entry_table',
            new_name='Entry_Exit',
        ),
    ]
