# Generated by Django 5.0.3 on 2024-04-06 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0006_party'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='party',
            name='id',
        ),
        migrations.AddField(
            model_name='party',
            name='pid',
            field=models.CharField(default=None, max_length=80, primary_key=True, serialize=False, verbose_name='Party ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='qid',
            field=models.PositiveBigIntegerField(primary_key=True, serialize=False, verbose_name='Wikidata QID'),
        ),
    ]