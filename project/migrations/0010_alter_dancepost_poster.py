# Generated by Django 4.2.16 on 2024-12-10 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0009_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dancepost",
            name="poster",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dance_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
