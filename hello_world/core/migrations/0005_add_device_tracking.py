# Generated migration for device tracking and timezone support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_add_convenor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalchatmessage',
            name='device_type',
            field=models.CharField(
                choices=[('web', 'Web Browser'), ('mobile', 'Mobile'), ('tablet', 'Tablet'), ('desktop', 'Desktop'), ('unknown', 'Unknown')],
                default='unknown',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='globalchatmessage',
            name='device_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='globalchatmessage',
            name='user_timezone',
            field=models.CharField(default='UTC', max_length=100),
        ),
        migrations.AddField(
            model_name='globalchatmessage',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='globalchatmessage',
            index=models.Index(fields=['-created_at'], name='core_globalc_created_idx'),
        ),
        migrations.AddIndex(
            model_name='globalchatmessage',
            index=models.Index(fields=['user_name'], name='core_globalc_user_idx'),
        ),
        migrations.AddField(
            model_name='societychatmessage',
            name='device_type',
            field=models.CharField(
                choices=[('web', 'Web Browser'), ('mobile', 'Mobile'), ('tablet', 'Tablet'), ('desktop', 'Desktop'), ('unknown', 'Unknown')],
                default='unknown',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='societychatmessage',
            name='device_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='societychatmessage',
            name='user_timezone',
            field=models.CharField(default='UTC', max_length=100),
        ),
        migrations.AddField(
            model_name='societychatmessage',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='societychatmessage',
            index=models.Index(fields=['society', '-created_at'], name='core_society_idx'),
        ),
        migrations.AddIndex(
            model_name='societychatmessage',
            index=models.Index(fields=['user_name'], name='core_society_user_idx'),
        ),
    ]
