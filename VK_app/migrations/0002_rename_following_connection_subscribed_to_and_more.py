# Generated by Django 4.2.1 on 2023-05-07 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('VK_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connection',
            old_name='following',
            new_name='subscribed_to',
        ),
        migrations.AlterField(
            model_name='connection',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
