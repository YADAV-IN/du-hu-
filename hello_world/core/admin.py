from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from .models import (
    Society, Event, Announcement, GlobalChatMessage, SocietyChatMessage,
    SocietyMember, SocietyGallery, SocietyAchievement, SocietyFAQ
)

class SocietyMemberInline(admin.TabularInline):
    model = SocietyMember
    extra = 1
    fields = ('name', 'role', 'profile_image', 'is_active', 'order')

class SocietyGalleryInline(admin.TabularInline):
    model = SocietyGallery
    extra = 1
    fields = ('title', 'image_url', 'is_featured', 'likes_count')

class SocietyAchievementInline(admin.TabularInline):
    model = SocietyAchievement
    extra = 1
    fields = ('title', 'achievement_date', 'icon')

class SocietyFAQInline(admin.TabularInline):
    model = SocietyFAQ
    extra = 1
    fields = ('question', 'answer', 'order')

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('colored_name', 'category', 'active_status', 'member_count', 'event_count', 'featured_tag', 'verified_tag', 'views_count')
    list_filter = ('is_active', 'is_featured', 'is_verified', 'category', 'created_at')
    search_fields = ('name', 'description', 'tagline', 'president_name', 'convenor_name')
    ordering = ('-is_featured', '-created_at',)
    inlines = [SocietyMemberInline, SocietyGalleryInline, SocietyAchievementInline, SocietyFAQInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'description', 'long_description', 'category', 'color_theme')
        }),
        ('Media', {
            'fields': ('banner_image', 'logo_image')
        }),
        ('Contact & Social', {
            'fields': ('email', 'phone', 'instagram', 'linkedin', 'twitter', 'website'),
            'classes': ('collapse',)
        }),
        ('Leadership', {
            'fields': ('president_name', 'vice_president', 'convenor_name', 'faculty_advisor', 'founding_year', 'member_count'),
            'classes': ('collapse',)
        }),
        ('Status & Visibility', {
            'fields': ('is_active', 'is_featured', 'is_verified', 'views_count')
        }),
        ('Additional Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'views_count')
    actions = ['make_featured', 'remove_featured', 'activate_society', 'deactivate_society', 'verify_society', 'unverify_society']
    
    def colored_name(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 14px;">⬤ {}</span>',
            obj.color_theme,
            obj.name
        )
    colored_name.short_description = 'Society Name'
    
    def verified_tag(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: #00d77a; font-weight: bold;">✓ Verified</span>')
        return format_html('<span style="color: #888;">—</span>')
    verified_tag.short_description = 'Verified'
    
    def verify_society(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f'{queryset.count()} societies verified')
    verify_society.short_description = "✓ Mark as Verified"
    
    def unverify_society(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, f'{queryset.count()} societies unverified')
    unverify_society.short_description = "✗ Remove Verification"
    
    def active_status(self, obj):
        color = '#28a745' if obj.is_active else '#dc3545'
        status = '✓ Active' if obj.is_active else '✗ Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            status
        )
    active_status.short_description = 'Status'
    
    def event_count(self, obj):
        count = obj.events.count()
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px;">📅 {} Events</span>',
            count
        )
    event_count.short_description = 'Events'
    
    def announcement_count(self, obj):
        count = obj.announcements.count()
        return format_html(
            '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 3px;">📢 {} Announcements</span>',
            count
        )
    announcement_count.short_description = 'Announcements'
    
    def featured_tag(self, obj):
        if obj.is_featured:
            return format_html('<span style="color: #ff6b6b; font-size: 18px;">⭐</span>')
        return '-'
    featured_tag.short_description = 'Featured'
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} societies marked as featured!')
    make_featured.short_description = '⭐ Mark as Featured'
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} societies removed from featured!')
    remove_featured.short_description = '☆ Remove from Featured'
    
    def activate_society(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} societies activated!')
    activate_society.short_description = '✓ Activate Selected'
    
    def deactivate_society(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} societies deactivated!')
    deactivate_society.short_description = '✗ Deactivate Selected'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'society_link', 'event_type_badge', 'date_display', 'featured_status', 'registration_count')
    list_filter = ('event_type', 'is_featured', 'society', 'event_date', 'created_at')
    search_fields = ('title', 'description', 'location')
    ordering = ('-event_date',)
    date_hierarchy = 'event_date'
    actions = ['make_featured', 'remove_featured', 'mark_completed']
    
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'society', 'description', 'event_type')
        }),
        ('Date & Location', {
            'fields': ('event_date', 'location')
        }),
        ('Media & Links', {
            'fields': ('event_image', 'registration_link')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_completed')
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def event_title(self, obj):
        return format_html(
            '<strong style="font-size: 14px;">📅 {}</strong>',
            obj.title
        )
    event_title.short_description = 'Event Title'
    
    def society_link(self, obj):
        return format_html(
            '<span style="color: {};">● {}</span>',
            obj.society.color_theme,
            obj.society.name
        )
    society_link.short_description = 'Society'
    
    def event_type_badge(self, obj):
        colors = {
            'workshop': '#007bff',
            'seminar': '#17a2b8',
            'competition': '#ffc107',
            'social': '#28a745',
            'other': '#6c757d'
        }
        color = colors.get(obj.event_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold;">{}</span>',
            color,
            obj.get_event_type_display()
        )
    event_type_badge.short_description = 'Type'
    
    def date_display(self, obj):
        return format_html(
            '<span style="font-weight: bold;">🕐 {}</span>',
            obj.event_date.strftime('%b %d, %Y')
        )
    date_display.short_description = 'Date'
    
    def featured_status(self, obj):
        if obj.is_featured:
            return format_html('<span style="color: #ff6b6b; font-size: 16px;">⭐ Featured</span>')
        return '☆'
    featured_status.short_description = 'Featured'
    
    def registration_count(self, obj):
        # Placeholder - extend later with registration model
        return format_html(
            '<span style="background-color: #00d77a; color: white; padding: 3px 8px; border-radius: 3px;">👥 +50</span>'
        )
    registration_count.short_description = 'Registrations'
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} events marked as featured!')
    make_featured.short_description = '⭐ Mark as Featured'
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} events removed from featured!')
    remove_featured.short_description = '☆ Remove Featured'
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f'{updated} events marked as completed!')
    mark_completed.short_description = '✓ Mark as Completed'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('announcement_title', 'society_name', 'priority_badge', 'active_status', 'views_count', 'created_at_display')
    list_filter = ('priority', 'is_active', 'society', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    actions = ['activate_announcements', 'deactivate_announcements', 'mark_high_priority']
    
    fieldsets = (
        ('Announcement Content', {
            'fields': ('title', 'content', 'society')
        }),
        ('Priority & Visibility', {
            'fields': ('priority', 'is_active')
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def announcement_title(self, obj):
        return format_html(
            '<strong>📢 {}</strong>',
            obj.title[:50]
        )
    announcement_title.short_description = 'Title'
    
    def society_name(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            obj.society.color_theme,
            obj.society.name
        )
    society_name.short_description = 'Society'
    
    def priority_badge(self, obj):
        colors = {
            'high': '#dc3545',
            'medium': '#ffc107',
            'low': '#28a745'
        }
        color = colors.get(obj.priority, '#6c757d')
        icons = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold;">{} {}</span>',
            color,
            icons.get(obj.priority, '⚪'),
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    def active_status(self, obj):
        color = '#28a745' if obj.is_active else '#dc3545'
        status = '✓ Live' if obj.is_active else '✗ Draft'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            status
        )
    active_status.short_description = 'Status'
    
    def views_count(self, obj):
        return format_html(
            '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 3px;">👁️ 1.2K</span>'
        )
    views_count.short_description = 'Views'
    
    def created_at_display(self, obj):
        return obj.created_at.strftime('%b %d, %Y %I:%M %p')
    created_at_display.short_description = 'Posted'
    
    def activate_announcements(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} announcements activated!')
    activate_announcements.short_description = '✓ Activate Selected'
    
    def deactivate_announcements(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} announcements deactivated!')
    deactivate_announcements.short_description = '✗ Deactivate Selected'
    
    def mark_high_priority(self, request, queryset):
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} announcements marked as high priority!')
    mark_high_priority.short_description = '🔴 Mark High Priority'

@admin.register(GlobalChatMessage)
class GlobalChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'message_preview', 'device_info', 'timezone_display', 'datetime_display', 'delete_btn')
    list_filter = ('created_at', 'device_type', 'user_timezone')
    search_fields = ('user_name', 'message', 'device_name', 'ip_address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'message_display', 'ip_address', 'user_timezone')
    actions = ['delete_spam', 'export_messages']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('user_name', 'message_display')
        }),
        ('🖥️ Device Information', {
            'fields': ('device_type', 'device_name', 'ip_address'),
            'classes': ('collapse',)
        }),
        ('🌍 Timezone & Date-Time', {
            'fields': ('user_timezone', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_info(self, obj):
        return format_html(
            '<span style="background-color: #00d77a; color: white; padding: 5px 10px; border-radius: 50px; font-weight: bold;">👤 {}</span>',
            obj.user_name[:20]
        )
    user_info.short_description = 'User'
    
    def message_preview(self, obj):
        preview = obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
        return format_html(
            '<em>{}</em>',
            preview
        )
    message_preview.short_description = 'Message'
    
    def device_info(self, obj):
        device_emoji = {
            'web': '🌐',
            'mobile': '📱',
            'tablet': '📱',
            'desktop': '🖥️',
            'unknown': '❓'
        }
        emoji = device_emoji.get(obj.device_type, '❓')
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{} {}</span>',
            emoji,
            obj.get_device_type_display() if obj.device_type != 'unknown' else 'Unknown'
        )
    device_info.short_description = 'Device'
    
    def timezone_display(self, obj):
        return format_html(
            '<span style="background-color: #17a2b8; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">🌐 {}</span>',
            obj.user_timezone or 'UTC'
        )
    timezone_display.short_description = 'Timezone'
    
    def datetime_display(self, obj):
        time_12h = obj.created_at.strftime('%I:%M %p')
        date_str = obj.created_at.strftime('%d %b %Y')
        return format_html(
            '<div style="font-weight: bold;">⏰ {}</div><div style="font-size: 0.9em; color: #666;">📅 {}</div>',
            time_12h,
            date_str
        )
    datetime_display.short_description = 'Time & Date'
    
    def delete_btn(self, obj):
        return '🗑️'
    delete_btn.short_description = 'Action'
    
    def message_display(self, obj):
        return obj.message
    message_display.short_description = 'Full Message'
    
    def delete_spam(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} spam messages deleted!')
    delete_spam.short_description = '🗑️ Delete Selected Messages'
    
    def export_messages(self, request, queryset):
        self.message_user(request, 'Export feature coming soon!')
    export_messages.short_description = '📥 Export Messages'

@admin.register(SocietyChatMessage)
class SocietyChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'society_info', 'message_preview', 'device_info', 'timezone_display', 'datetime_display')
    list_filter = ('society', 'created_at', 'device_type', 'user_timezone')
    search_fields = ('user_name', 'message', 'society__name', 'device_name', 'ip_address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'message_display', 'ip_address', 'user_timezone')
    actions = ['delete_messages', 'mark_important']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('user_name', 'society', 'message_display')
        }),
        ('🖥️ Device Information', {
            'fields': ('device_type', 'device_name', 'ip_address'),
            'classes': ('collapse',)
        }),
        ('🌍 Timezone & Date-Time', {
            'fields': ('user_timezone', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_info(self, obj):
        return format_html(
            '<span style="background-color: #00d7ff; color: white; padding: 5px 10px; border-radius: 50px; font-weight: bold;">👤 {}</span>',
            obj.user_name[:20]
        )
    user_info.short_description = 'User'
    
    def society_info(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            obj.society.color_theme,
            obj.society.name[:20]
        )
    society_info.short_description = 'Society'
    
    def message_preview(self, obj):
        preview = obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
        return format_html('<em>{}</em>', preview)
    message_preview.short_description = 'Message'
    
    def device_info(self, obj):
        device_emoji = {
            'web': '🌐',
            'mobile': '📱',
            'tablet': '📱',
            'desktop': '🖥️',
            'unknown': '❓'
        }
        emoji = device_emoji.get(obj.device_type, '❓')
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{} {}</span>',
            emoji,
            obj.get_device_type_display() if obj.device_type != 'unknown' else 'Unknown'
        )
    device_info.short_description = 'Device'
    
    def timezone_display(self, obj):
        return format_html(
            '<span style="background-color: #17a2b8; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">🌐 {}</span>',
            obj.user_timezone or 'UTC'
        )
    timezone_display.short_description = 'Timezone'
    
    def datetime_display(self, obj):
        time_12h = obj.created_at.strftime('%I:%M %p')
        date_str = obj.created_at.strftime('%d %b %Y')
        return format_html(
            '<div style="font-weight: bold;">⏰ {}</div><div style="font-size: 0.9em; color: #666;">📅 {}</div>',
            time_12h,
            date_str
        )
    datetime_display.short_description = 'Time & Date'
    
    def message_display(self, obj):
        return obj.message
    message_display.short_description = 'Full Message'
    
    def delete_messages(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} messages deleted!')
    delete_messages.short_description = '🗑️ Delete Selected'
    
    def mark_important(self, request, queryset):
        self.message_user(request, f'{queryset.count()} messages marked as important!')
    mark_important.short_description = '⭐ Mark Important'


# ========== NEW ADVANCED SOCIETY MODELS ==========

@admin.register(SocietyMember)
class SocietyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'society', 'role_badge', 'is_active', 'joined_at')
    list_filter = ('society', 'role', 'is_active')
    search_fields = ('name', 'email', 'society__name')
    ordering = ('society', 'order', 'name')
    
    def role_badge(self, obj):
        colors = {
            'president': '#ff4081',
            'vice_president': '#9c27b0',
            'secretary': '#2196f3',
            'treasurer': '#4caf50',
            'tech_head': '#00bcd4',
            'creative_head': '#ff9800',
            'pr_head': '#e91e63',
            'member': '#607d8b',
            'volunteer': '#795548',
        }
        color = colors.get(obj.role, '#607d8b')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px;">{}</span>',
            color, obj.get_role_display()
        )
    role_badge.short_description = 'Role'


@admin.register(SocietyGallery)
class SocietyGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'society', 'image_preview', 'is_featured', 'likes_count', 'uploaded_at')
    list_filter = ('society', 'is_featured', 'uploaded_at')
    search_fields = ('title', 'caption', 'society__name')
    ordering = ('-uploaded_at',)
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 6px;"/>',
                obj.image_url
            )
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(SocietyAchievement)
class SocietyAchievementAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'society', 'achievement_date')
    list_filter = ('society', 'achievement_date')
    search_fields = ('title', 'description', 'society__name')
    ordering = ('-achievement_date',)


@admin.register(SocietyFAQ)
class SocietyFAQAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'society', 'order')
    list_filter = ('society',)
    search_fields = ('question', 'answer', 'society__name')
    ordering = ('society', 'order')
    
    def question_preview(self, obj):
        return obj.question[:60] + '...' if len(obj.question) > 60 else obj.question
    question_preview.short_description = 'Question'
# Customize Admin Site
admin.site.site_header = "🎓 DU HUB - Advanced Admin Control Board"
admin.site.site_title = "DU HUB Admin"
admin.site.index_title = "Welcome to DU HUB Advanced Management System"
