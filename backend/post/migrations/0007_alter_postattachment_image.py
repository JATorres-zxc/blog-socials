# Generated by Django 5.0.3 on 2024-03-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_alter_postattachment_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postattachment',
            name='image',
            field=models.ImageField(upload_to='post_attachments'),
        ),
    ]
