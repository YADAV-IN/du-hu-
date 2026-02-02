from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Society(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('literary', 'Literary'),
        ('social', 'Social Service'),
        ('music', 'Music & Arts'),
        ('debate', 'Debate & MUN'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField()
    long_description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    banner_image = models.URLField(blank=True, null=True)
    logo_image = models.URLField(blank=True, null=True)
    color_theme = models.CharField(max_length=7, default='#00ff00')
    
    # Contact & Social
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Stats & Info
    founding_year = models.IntegerField(default=2020)
    member_count = models.IntegerField(default=0)
    president_name = models.CharField(max_length=100, blank=True, null=True)
    vice_president = models.CharField(max_length=100, blank=True, null=True)
    convenor_name = models.CharField(max_length=100, blank=True, null=True)
    faculty_advisor = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # Admin Control
    access_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_restricted = models.BooleanField(default=False)
    
    # Stats
    views_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Societies"
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def total_events(self):
        return self.events.count()
    
    @property
    def upcoming_events_count(self):
        return self.events.filter(event_date__gte=timezone.now()).count()

class Event(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('competition', 'Competition'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]
    
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=300)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    registration_link = models.URLField(blank=True, null=True)
    event_image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.title} - {self.society.name}"

class Announcement(models.Model):
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=300)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.society.name}"

class GlobalChatMessage(models.Model):
    DEVICE_CHOICES = [
        ('web', 'Web Browser'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('desktop', 'Desktop'),
        ('unknown', 'Unknown'),
    ]
    
    user_name = models.CharField(max_length=100)
    message = models.TextField()
    device_type = models.CharField(max_length=20, choices=DEVICE_CHOICES, default='unknown')
    device_name = models.CharField(max_length=200, blank=True, null=True)  # e.g., "Chrome on Windows"
    user_timezone = models.CharField(max_length=100, default='UTC')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user_name']),
        ]
    
    def __str__(self):
        return f"{self.user_name}: {self.message[:50]}"
    
    def get_formatted_time(self):
        """Return time in 12-hour format with AM/PM"""
        return self.created_at.strftime('%I:%M %p')
    
    def get_formatted_date(self):
        """Return date in readable format"""
        return self.created_at.strftime('%d %b %Y')

class SocietyChatMessage(models.Model):
    DEVICE_CHOICES = [
        ('web', 'Web Browser'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('desktop', 'Desktop'),
        ('unknown', 'Unknown'),
    ]
    
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='chat_messages')
    user_name = models.CharField(max_length=100)
    message = models.TextField()
    device_type = models.CharField(max_length=20, choices=DEVICE_CHOICES, default='unknown')
    device_name = models.CharField(max_length=200, blank=True, null=True)  # e.g., "Safari on iPhone"
    user_timezone = models.CharField(max_length=100, default='UTC')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['society', '-created_at']),
            models.Index(fields=['user_name']),
        ]
    
    def __str__(self):
        return f"{self.user_name} in {self.society.name}: {self.message[:50]}"
    
    def get_formatted_time(self):
        """Return time in 12-hour format with AM/PM"""
        return self.created_at.strftime('%I:%M %p')
    
    def get_formatted_date(self):
        """Return date in readable format"""
        return self.created_at.strftime('%d %b %Y')


class SocietyMember(models.Model):
    """Members of a society with roles"""
    ROLE_CHOICES = [
        ('president', 'President'),
        ('vice_president', 'Vice President'),
        ('secretary', 'Secretary'),
        ('convenor', 'Convenor'),
        ('treasurer', 'Treasurer'),
        ('tech_head', 'Tech Head'),
        ('creative_head', 'Creative Head'),
        ('pr_head', 'PR Head'),
        ('member', 'Core Member'),
        ('volunteer', 'Volunteer'),
    ]
    
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    profile_image = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    joined_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'role', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_role_display()} @ {self.society.name}"


class SocietyGallery(models.Model):
    """Photo gallery for societies"""
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='gallery')
    title = models.CharField(max_length=200)
    image_url = models.URLField()
    caption = models.TextField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    likes_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = "Society Galleries"
    
    def __str__(self):
        return f"{self.title} - {self.society.name}"


class SocietyAchievement(models.Model):
    """Achievements and awards"""
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    achievement_date = models.DateField()
    icon = models.CharField(max_length=50, default='🏆')
    
    class Meta:
        ordering = ['-achievement_date']
    
    def __str__(self):
        return f"{self.title} - {self.society.name}"


class SocietyFAQ(models.Model):
    """Frequently asked questions"""
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Society FAQ"
        verbose_name_plural = "Society FAQs"


class AdminUser(models.Model):
    """Admin users with role-based permissions"""
    ADMIN_ROLES = [
        ('super_admin', 'Super Admin - All Access'),
        ('societies_admin', 'Societies Admin - Manage Societies'),
        ('events_admin', 'Events Admin - Manage Events'),
        ('chat_admin', 'Chat Admin - Moderate Chat'),
        ('reports_admin', 'Reports Admin - View Reports'),
        ('limited_admin', 'Limited Admin - Specific Societies'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    societies = models.ManyToManyField(Society, related_name='admin_users', blank=True)
    role = models.CharField(max_length=20, choices=ADMIN_ROLES, default='limited_admin')
    is_super_admin = models.BooleanField(default=False)
    created_by = models.ForeignKey('DeveloperAdmin', on_delete=models.SET_NULL, null=True, blank=True, related_name='admins_created')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Permission levels
    can_manage_societies = models.BooleanField(default=False)
    can_manage_events = models.BooleanField(default=False)
    can_manage_admins = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    can_moderate_chat = models.BooleanField(default=False)
    can_delete_content = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def update_permissions_from_role(self):
        """Auto-update permissions based on role"""
        if self.role == 'super_admin':
            self.can_manage_societies = True
            self.can_manage_events = True
            self.can_manage_admins = True
            self.can_view_reports = True
            self.can_moderate_chat = True
            self.can_delete_content = True
        elif self.role == 'societies_admin':
            self.can_manage_societies = True
            self.can_view_reports = True
        elif self.role == 'events_admin':
            self.can_manage_events = True
            self.can_view_reports = True
        elif self.role == 'chat_admin':
            self.can_moderate_chat = True
            self.can_delete_content = True
        elif self.role == 'reports_admin':
            self.can_view_reports = True
        else:  # limited_admin
            self.can_manage_societies = False
            self.can_manage_events = False
            self.can_manage_admins = False
            self.can_delete_content = False


class DeveloperAdmin(models.Model):
    """Master developer account with full control"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    developer_id = models.CharField(max_length=50, unique=True)
    master_key = models.CharField(max_length=100)  # Master password hash
    organization_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Full control permissions
    can_create_admins = models.BooleanField(default=True)
    can_delete_admins = models.BooleanField(default=True)
    can_modify_permissions = models.BooleanField(default=True)
    can_view_all_logs = models.BooleanField(default=True)
    can_manage_all_societies = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Developer Admin"
        verbose_name_plural = "Developer Admins"
    
    def __str__(self):
        return f"Developer: {self.developer_id} ({self.user.username})"
    
    def get_admins_count(self):
        return AdminUser.objects.filter(created_by=self).count()
    
    def get_total_societies(self):
        return Society.objects.count()


class AdminAccessLog(models.Model):
    """Track admin panel access and actions"""
    admin_user = models.ForeignKey(AdminUser, on_delete=models.CASCADE, related_name='access_logs', null=True, blank=True)
    developer = models.ForeignKey(DeveloperAdmin, on_delete=models.CASCADE, related_name='access_logs', null=True, blank=True)
    action = models.CharField(max_length=200)  # e.g., "Created event", "Deleted society"
    resource_type = models.CharField(max_length=50)  # e.g., "Society", "Event", "Admin"
    resource_id = models.IntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    changes_made = models.TextField(blank=True)  # JSON of changes
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Admin Access Log"
        verbose_name_plural = "Admin Access Logs"
    
    def __str__(self):
        actor = self.admin_user.user.username if self.admin_user else self.developer.developer_id
        return f"{actor} - {self.action} - {self.timestamp}"


class AdminCredentials(models.Model):
    """Store admin credentials and access tokens"""
    admin_user = models.OneToOneField(AdminUser, on_delete=models.CASCADE, related_name='credentials')
    temporary_password = models.CharField(max_length=100, blank=True)
    password_changed = models.BooleanField(default=False)
    password_changed_at = models.DateTimeField(null=True, blank=True)
    api_token = models.CharField(max_length=100, unique=True, blank=True)
    token_created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Credentials for {self.admin_user.user.username}"



class AccessLog(models.Model):
    """Log of who accessed what society"""
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='access_logs')
    user_identifier = models.CharField(max_length=100)  # IP or session
    access_code_used = models.CharField(max_length=20)
    accessed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_identifier} accessed {self.society.name}"
    
    class Meta:
        ordering = ['-accessed_at']


class AdminLoginRecord(models.Model):
    """Track admin logins with device info, timestamp, etc."""
    admin_user = models.CharField(max_length=100)  # Username
    login_time = models.DateTimeField(auto_now_add=True)
    login_date = models.DateField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    device_info = models.CharField(max_length=500, blank=True)  # User-Agent / Device IMEI equivalent
    browser = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    is_successful = models.BooleanField(default=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-login_time']
        verbose_name = "Admin Login Record"
        verbose_name_plural = "Admin Login Records"
    
    def __str__(self):
        return f"{self.admin_user} - {self.login_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def get_duration(self):
        if self.logout_time:
            delta = self.logout_time - self.login_time
            self.duration_minutes = int(delta.total_seconds() / 60)
            self.save()
            return f"{self.duration_minutes} mins"
        return "Active"


class GlobalChatMessage(models.Model):
    """Global chat messages"""
    user_name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user_name}: {self.message[:50]}"
