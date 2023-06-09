# Generated by Django 4.2.1 on 2023-05-08 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VK_app', '0003_alter_connection_subscribed_to_friend'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connection',
            old_name='subscribed_to',
            new_name='friend',
        ),
        migrations.RenameField(
            model_name='connection',
            old_name='creator',
            new_name='user',
        ),
        migrations.AddField(
            model_name='connection',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Approve'), (1, 'Request')], null=True),
        ),
        migrations.DeleteModel(
            name='Friend',
        ),
    ]
