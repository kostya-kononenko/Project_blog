# Generated by Django 4.2.2 on 2023-06-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_post_snippet"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="post_image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="post",
            name="snippet",
            field=models.CharField(max_length=255),
        ),
    ]
