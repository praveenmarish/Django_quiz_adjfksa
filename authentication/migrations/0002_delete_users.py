# Generated by Django 3.2.3 on 2021-06-02 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='users',
        ),
    ]