# Generated by Django 5.0.1 on 2024-01-23 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_product_tags_delete_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='life',
            field=models.CharField(default='1 day', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_count',
            field=models.CharField(default='10', max_length=100),
        ),
    ]
