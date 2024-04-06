# Generated by Django 5.0.3 on 2024-04-06 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0005_alter_source_sid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.SmallIntegerField()),
                ('month', models.SmallIntegerField(null=True)),
                ('day', models.SmallIntegerField(null=True)),
            ],
        ),
    ]
