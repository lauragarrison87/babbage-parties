# Generated by Django 5.0.3 on 2024-04-15 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0011_rename_guest_mention'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mention',
            options={'ordering': ['party', 'guest']},
        ),
        migrations.RenameField(
            model_name='mention',
            old_name='name',
            new_name='guest',
        ),
        migrations.AlterUniqueTogether(
            name='mention',
            unique_together={('party', 'guest', 'source')},
        ),
    ]