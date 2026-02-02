# Migration for advanced society features

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_missing_fields'),
    ]

    operations = [
        # Add new fields to Society
        migrations.AddField(
            model_name='society',
            name='category',
            field=models.CharField(choices=[('technical', 'Technical'), ('cultural', 'Cultural'), ('sports', 'Sports'), ('literary', 'Literary'), ('social', 'Social Service'), ('music', 'Music & Arts'), ('debate', 'Debate & MUN'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='society',
            name='tagline',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='long_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='founding_year',
            field=models.IntegerField(default=2020),
        ),
        migrations.AddField(
            model_name='society',
            name='member_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='society',
            name='president_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='vice_president',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='faculty_advisor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='society',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='society',
            name='views_count',
            field=models.IntegerField(default=0),
        ),
        
        # Create SocietyMember model
        migrations.CreateModel(
            name='SocietyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('president', 'President'), ('vice_president', 'Vice President'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('tech_head', 'Tech Head'), ('creative_head', 'Creative Head'), ('pr_head', 'PR Head'), ('member', 'Core Member'), ('volunteer', 'Volunteer')], default='member', max_length=20)),
                ('profile_image', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('joined_at', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='core.society')),
            ],
            options={
                'ordering': ['order', 'role', 'name'],
            },
        ),
        
        # Create SocietyGallery model
        migrations.CreateModel(
            name='SocietyGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image_url', models.URLField()),
                ('caption', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('likes_count', models.IntegerField(default=0)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='core.society')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photos', to='core.event')),
            ],
            options={
                'verbose_name_plural': 'Society Galleries',
                'ordering': ['-uploaded_at'],
            },
        ),
        
        # Create SocietyAchievement model
        migrations.CreateModel(
            name='SocietyAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('achievement_date', models.DateField()),
                ('icon', models.CharField(default='🏆', max_length=50)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to='core.society')),
            ],
            options={
                'ordering': ['-achievement_date'],
            },
        ),
        
        # Create SocietyFAQ model
        migrations.CreateModel(
            name='SocietyFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('answer', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='core.society')),
            ],
            options={
                'verbose_name': 'Society FAQ',
                'verbose_name_plural': 'Society FAQs',
                'ordering': ['order'],
            },
        ),
    ]
