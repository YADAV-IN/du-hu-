# Generated migration for model updates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='society',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='society',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='society',
            name='logo_image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='society',
            name='poster_image',
        ),
        migrations.AddField(
            model_name='event',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='event',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.RenameField(
            model_name='event',
            old_name='image',
            new_name='event_image',
        ),
        migrations.AddField(
            model_name='announcement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
