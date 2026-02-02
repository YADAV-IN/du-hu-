from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_advanced_society_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='society',
            name='convenor_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
