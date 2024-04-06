# Generated by Django 5.0.3 on 2024-04-06 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0007_remove_party_id_party_pid_alter_person_qid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='party',
            options={'ordering': ['year', 'month', 'day'], 'verbose_name_plural': 'parties'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['name', 'qid']},
        ),
        migrations.AlterModelOptions(
            name='source',
            options={'ordering': ['sid']},
        ),
    ]
