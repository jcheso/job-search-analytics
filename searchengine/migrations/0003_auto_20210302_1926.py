# Generated by Django 3.1.2 on 2021-03-02 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('searchengine', '0002_auto_20210302_1920'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SearchData',
            new_name='SearchInput',
        ),
    ]
