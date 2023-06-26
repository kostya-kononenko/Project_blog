# Generated by Django 4.2.2 on 2023-06-25 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_post_post_image_alter_post_snippet"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="author",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="author",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
