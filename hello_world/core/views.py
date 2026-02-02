from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import (
    Society, Event, Announcement, GlobalChatMessage, SocietyChatMessage,
    SocietyMember, SocietyGallery, SocietyAchievement, SocietyFAQ,
    AdminUser, AccessLog, AdminLoginRecord, DeveloperAdmin, AdminAccessLog, AdminCredentials
)
import json
import secrets
import user_agents
from django.http import HttpRequest
import hashlib
from django.contrib.auth.hashers import make_password, check_password

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_info(request):
    """Extract device type and name from user agent"""
    try:
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        ua = user_agents.parse(user_agent_string)
        
        # Determine device type
        if ua.is_mobile:
            device_type = 'mobile'
        elif ua.is_tablet:
            device_type = 'tablet'
        elif ua.is_pc or ua.is_bot == False:
            device_type = 'desktop'
        else:
            device_type = 'web'
        
        # Get device name (browser + OS)
        browser = ua.browser.family
        os = ua.os.family
        device_name = f"{browser} on {os}"
        
        return device_type, device_name
    except Exception as e:
        return 'unknown', 'Unknown Device'

def get_user_timezone(request):
    """Get user's timezone from request data or browser"""
    try:
        data = json.loads(request.body) if request.body else {}
        timezone_str = data.get('timezone', request.META.get('HTTP_X_TIMEZONE', 'UTC'))
        return timezone_str if timezone_str else 'UTC'
    except:
        return 'UTC'

def get_device_info(request):
    """Extract device information from User-Agent"""
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    ua = user_agents.parse(user_agent_string)
    
    return {
        'user_agent': user_agent_string,
        'browser': f"{ua.browser.family} {ua.browser.version_string}",
        'os': f"{ua.os.family} {ua.os.version_string}",
        'device': ua.device.family if ua.device.family else 'Unknown'
    }

def index(request):
    """Main homepage with all societies, events, and global chat"""
    try:
        societies = Society.objects.filter(is_active=True)
        upcoming_events = Event.objects.filter(event_date__gte=timezone.now())[:6]
        recent_announcements = Announcement.objects.filter(is_active=True)[:10]
        global_messages = GlobalChatMessage.objects.all()[:50]
        
        context = {
            'societies': societies,
            'upcoming_events': upcoming_events,
            'recent_announcements': recent_announcements,
            'global_messages': global_messages,
        }
    except Exception as e:
        # Migration not applied yet - show empty page
        context = {
            'societies': [],
            'upcoming_events': [],
            'recent_announcements': [],
            'global_messages': [],
            'migration_error': str(e),
        }
    return render(request, 'index.html', context)

def society_detail(request, society_id):
    """Advanced society page with all features"""
    society = get_object_or_404(Society, id=society_id)
    
    # Increment view count
    try:
        Society.objects.filter(id=society_id).update(views_count=society.views_count + 1)
    except:
        pass
    
    # Get all related data
    upcoming_events = society.events.filter(event_date__gte=timezone.now())[:6]
    past_events = society.events.filter(event_date__lt=timezone.now())[:6]
    announcements = society.announcements.filter(is_active=True)[:10]
    chat_messages = society.chat_messages.all()[:50]
    
    # New features data
    try:
        members = society.members.filter(is_active=True)
        leadership = members.exclude(role='member').exclude(role='volunteer')[:6]
        gallery = society.gallery.all()[:12]
        featured_gallery = society.gallery.filter(is_featured=True)[:4]
        achievements = society.achievements.all()[:10]
        faqs = society.faqs.all()[:10]
    except Exception:
        members = []
        leadership = []
        gallery = []
        featured_gallery = []
        achievements = []
        faqs = []
    
    # Stats
    stats = {
        'total_events': society.events.count(),
        'upcoming_events': len(upcoming_events) if upcoming_events else 0,
        'total_members': len(members) if members else 0,
        'gallery_count': len(gallery) if gallery else 0,
        'achievements_count': len(achievements) if achievements else 0,
    }
    
    # Similar societies
    try:
        similar_societies = Society.objects.filter(
            category=society.category, is_active=True
        ).exclude(id=society.id)[:4]
    except Exception:
        similar_societies = []
    
    context = {
        'society': society,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'announcements': announcements,
        'chat_messages': chat_messages,
        'members': members,
        'leadership': leadership,
        'gallery': gallery,
        'featured_gallery': featured_gallery,
        'achievements': achievements,
        'faqs': faqs,
        'stats': stats,
        'similar_societies': similar_societies,
    }
    return render(request, 'society_detail.html', context)

def all_events(request):
    """Page showing all upcoming events"""
    events = Event.objects.filter(event_date__gte=timezone.now())
    context = {'events': events}
    return render(request, 'all_events.html', context)

@csrf_exempt
@require_POST
@csrf_exempt
def send_global_message(request):
    """Handle global chat messages with device tracking"""
    try:
        data = json.loads(request.body)
        user_name = data.get('user_name', 'Anonymous')
        message = data.get('message', '')
        user_timezone = data.get('timezone', 'UTC')
        
        if message.strip():
            # Get device information
            device_type, device_name = get_device_info(request)
            ip_address = get_client_ip(request)
            
            chat_msg = GlobalChatMessage.objects.create(
                user_name=user_name,
                message=message,
                device_type=device_type,
                device_name=device_name,
                user_timezone=user_timezone or 'UTC',
                ip_address=ip_address
            )
            return JsonResponse({
                'status': 'success',
                'message': {
                    'user_name': chat_msg.user_name,
                    'message': chat_msg.message,
                    'device_type': chat_msg.device_type,
                    'timezone': chat_msg.user_timezone,
                    'created_at': chat_msg.created_at.strftime('%I:%M %p'),
                    'created_date': chat_msg.created_at.strftime('%d %b %Y')
                }
            })
        return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_POST
@csrf_exempt
@require_POST
def send_society_message(request, society_id):
    """Handle society-specific chat messages with device tracking"""
    try:
        society = get_object_or_404(Society, id=society_id)
        data = json.loads(request.body)
        user_name = data.get('user_name', 'Anonymous')
        message = data.get('message', '')
        user_timezone = data.get('timezone', 'UTC')
        
        if message.strip():
            # Get device information
            device_type, device_name = get_device_info(request)
            ip_address = get_client_ip(request)
            
            chat_msg = SocietyChatMessage.objects.create(
                society=society,
                user_name=user_name,
                message=message,
                device_type=device_type,
                device_name=device_name,
                user_timezone=user_timezone or 'UTC',
                ip_address=ip_address
            )
            return JsonResponse({
                'status': 'success',
                'message': {
                    'user_name': chat_msg.user_name,
                    'message': chat_msg.message,
                    'device_type': chat_msg.device_type,
                    'timezone': chat_msg.user_timezone,
                    'created_at': chat_msg.created_at.strftime('%I:%M %p'),
                    'created_date': chat_msg.created_at.strftime('%d %b %Y')
                }
            })
        return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@csrf_exempt
def get_global_messages(request):
    """API endpoint to fetch latest global messages with device & timezone info"""
    messages = GlobalChatMessage.objects.all()[:50]
    data = [{
        'user_name': msg.user_name,
        'message': msg.message,
        'device_type': msg.device_type,
        'device_name': msg.device_name,
        'timezone': msg.user_timezone,
        'created_at': msg.created_at.strftime('%I:%M %p'),
        'created_date': msg.created_at.strftime('%d %b %Y'),
        'timestamp': msg.created_at.isoformat()
    } for msg in messages]
    return JsonResponse({'messages': data})

@csrf_exempt
def get_society_messages(request, society_id):
    """API endpoint to fetch latest society messages with device & timezone info"""
    society = get_object_or_404(Society, id=society_id)
    messages = society.chat_messages.all()[:50]
    data = [{
        'user_name': msg.user_name,
        'message': msg.message,
        'device_type': msg.device_type,
        'device_name': msg.device_name,
        'timezone': msg.user_timezone,
        'created_at': msg.created_at.strftime('%I:%M %p'),
        'created_date': msg.created_at.strftime('%d %b %Y'),
        'timestamp': msg.created_at.isoformat()
    } for msg in messages]
    return JsonResponse({'messages': data})
    } for msg in messages]
    return JsonResponse({'messages': data})

# ===== ADMIN PANEL VIEWS =====

def admin_login(request):
    """Admin login page"""
    if request.user.is_authenticated and (request.user.is_superuser or hasattr(request.user, 'adminuser')):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user and (user.is_superuser or hasattr(user, 'adminuser')):
            login(request, user)
            
            # Record login in AdminLoginRecord
            device_info = get_device_info(request)
            ip_address = get_client_ip(request)
            
            AdminLoginRecord.objects.create(
                admin_user=username,
                ip_address=ip_address,
                device_info=device_info['user_agent'],
                browser=device_info['browser'],
                operating_system=device_info['os'],
                session_id=request.session.session_key,
                is_successful=True
            )
            
            return redirect('admin_dashboard')
        else:
            # Record failed login attempt
            ip_address = get_client_ip(request)
            device_info = get_device_info(request)
            
            try:
                AdminLoginRecord.objects.create(
                    admin_user=username or 'Unknown',
                    ip_address=ip_address,
                    device_info=device_info['user_agent'],
                    browser=device_info['browser'],
                    operating_system=device_info['os'],
                    is_successful=False
                )
            except:
                pass
            
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or not admin'})
    
    return render(request, 'admin_login.html')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    """Admin control panel dashboard"""
    if not (request.user.is_superuser or hasattr(request.user, 'adminuser')):
        return redirect('admin_login')
    
    admin_user = getattr(request.user, 'adminuser', None)
    
    if admin_user and admin_user.is_super_admin:
        societies = Society.objects.all()
    elif admin_user:
        societies = admin_user.societies.all()
    else:
        societies = Society.objects.all()
    
    context = {
        'societies': societies,
        'total_societies': Society.objects.count(),
        'total_events': Event.objects.count(),
        'total_messages': GlobalChatMessage.objects.count(),
        'is_super_admin': admin_user.is_super_admin if admin_user else request.user.is_superuser,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required(login_url='admin_login')
def manage_society(request, society_id):
    """Manage individual society"""
    if not (request.user.is_superuser or hasattr(request.user, 'adminuser')):
        return redirect('admin_login')
    
    society = get_object_or_404(Society, id=society_id)
    admin_user = getattr(request.user, 'adminuser', None)
    
    # Check permission
    if admin_user and not admin_user.is_super_admin and society not in admin_user.societies.all():
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        society.name = request.POST.get('name', society.name)
        society.description = request.POST.get('description', society.description)
        society.is_restricted = request.POST.get('is_restricted') == 'on'
        society.member_count = int(request.POST.get('member_count', society.member_count))
        
        if request.POST.get('regenerate_code'):
            society.access_code = secrets.token_urlsafe(12)[:20]
        
        society.save()
        return redirect('admin_dashboard')
    
    access_logs = AccessLog.objects.filter(society=society)[:20]
    context = {
        'society': society,
        'access_logs': access_logs,
    }
    return render(request, 'manage_society.html', context)

def verify_access_code(request, society_id):
    """Verify society access code"""
    if request.method == 'POST':
        code = request.POST.get('code')
        society = get_object_or_404(Society, id=society_id)
        
        if society.access_code == code:
            request.session[f'society_{society_id}_access'] = True
            AccessLog.objects.create(
                society=society,
                user_identifier=request.META.get('REMOTE_ADDR', 'unknown'),
                access_code_used=code
            )
            return redirect('society_detail', society_id=society_id)
        else:
            return render(request, 'verify_code.html', {'error': 'Invalid access code', 'society_id': society_id})
    
    society = get_object_or_404(Society, id=society_id)
    return render(request, 'verify_code.html', {'society': society})

def admin_logout(request):
    """Admin logout"""
    logout(request)
    return redirect('home')
@login_required(login_url='admin_login')
def admin_login_records(request):
    """View all admin login records"""
    if not (request.user.is_superuser or hasattr(request.user, 'adminuser')):
        return redirect('admin_login')
    
    # Get all login records
    records = AdminLoginRecord.objects.all()[:200]
    
    # Statistics
    total_logins = AdminLoginRecord.objects.filter(is_successful=True).count()
    failed_logins = AdminLoginRecord.objects.filter(is_successful=False).count()
    unique_admins = AdminLoginRecord.objects.filter(is_successful=True).values('admin_user').distinct().count()
    today_logins = AdminLoginRecord.objects.filter(
        login_date=timezone.now().date(),
        is_successful=True
    ).count()
    
    # Get logins by admin
    logins_by_admin = AdminLoginRecord.objects.filter(is_successful=True).values('admin_user').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'records': records,
        'total_logins': total_logins,
        'failed_logins': failed_logins,
        'unique_admins': unique_admins,
        'today_logins': today_logins,
        'logins_by_admin': logins_by_admin,
    }
    return render(request, 'admin_login_records.html', context)

# ===== DEVELOPER ADMIN VIEWS =====

def developer_login(request):
    """Developer admin login page"""
    if request.user.is_authenticated and hasattr(request.user, 'developeradmin'):
        return redirect('developer_dashboard')
    
    if request.method == 'POST':
        developer_id = request.POST.get('developer_id')
        master_key = request.POST.get('master_key')
        
        try:
            dev_admin = DeveloperAdmin.objects.get(developer_id=developer_id, is_active=True)
            if check_password(master_key, dev_admin.master_key):
                login(request, dev_admin.user)
                
                # Record login
                ip_address = get_client_ip(request)
                AdminAccessLog.objects.create(
                    developer=dev_admin,
                    action="Developer Login",
                    resource_type="System",
                    ip_address=ip_address,
                    changes_made=json.dumps({'login': 'successful'})
                )
                
                return redirect('developer_dashboard')
            else:
                error = 'Invalid master key'
        except DeveloperAdmin.DoesNotExist:
            error = 'Developer ID not found'
        
        return render(request, 'developer_login.html', {'error': error})
    
    return render(request, 'developer_login.html')

@login_required(login_url='developer_login')
def developer_dashboard(request):
    """Developer master dashboard"""
    if not hasattr(request.user, 'developeradmin'):
        return redirect('developer_login')
    
    developer = request.user.developeradmin
    
    # Get all statistics
    total_admins = AdminUser.objects.filter(created_by=developer).count()
    active_admins = AdminUser.objects.filter(created_by=developer, is_active=True).count()
    total_societies = Society.objects.count()
    total_events = Event.objects.count()
    today_logins = AdminLoginRecord.objects.filter(login_date=timezone.now().date()).count()
    
    # Get all admins managed by this developer
    all_admins = AdminUser.objects.filter(created_by=developer).select_related('user')
    
    # Recent access logs
    recent_logs = AdminAccessLog.objects.filter(developer=developer)[:20]
    
    # Admin by role
    admins_by_role = AdminUser.objects.filter(created_by=developer).values('role').annotate(count=Count('id'))
    
    context = {
        'developer': developer,
        'total_admins': total_admins,
        'active_admins': active_admins,
        'total_societies': total_societies,
        'total_events': total_events,
        'today_logins': today_logins,
        'all_admins': all_admins,
        'recent_logs': recent_logs,
        'admins_by_role': admins_by_role,
    }
    return render(request, 'developer_dashboard.html', context)

@login_required(login_url='developer_login')
def create_admin(request):
    """Create new admin user"""
    if not hasattr(request.user, 'developeradmin'):
        return redirect('developer_login')
    
    developer = request.user.developeradmin
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        admin_role = request.POST.get('role', 'limited_admin')
        
        # Generate temporary password
        temp_password = secrets.token_urlsafe(12)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=temp_password
        )
        
        # Create admin
        admin = AdminUser.objects.create(
            user=user,
            role=admin_role,
            created_by=developer,
            is_active=True
        )
        
        # Update permissions based on role
        admin.update_permissions_from_role()
        admin.save()
        
        # Create credentials
        AdminCredentials.objects.create(
            admin_user=admin,
            temporary_password=temp_password,
            password_changed=False
        )
        
        # Log action
        ip_address = get_client_ip(request)
        AdminAccessLog.objects.create(
            developer=developer,
            action=f"Created Admin: {username}",
            resource_type="Admin",
            resource_id=admin.id,
            ip_address=ip_address,
            changes_made=json.dumps({'role': admin_role, 'username': username})
        )
        
        return render(request, 'admin_created.html', {
            'admin': admin,
            'temp_password': temp_password,
            'username': username
        })
    
    context = {
        'roles': AdminUser.ADMIN_ROLES
    }
    return render(request, 'create_admin.html', context)

@login_required(login_url='developer_login')
def manage_admin(request, admin_id):
    """Manage individual admin"""
    if not hasattr(request.user, 'developeradmin'):
        return redirect('developer_login')
    
    developer = request.user.developeradmin
    admin = get_object_or_404(AdminUser, id=admin_id, created_by=developer)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_role':
            new_role = request.POST.get('role')
            admin.role = new_role
            admin.update_permissions_from_role()
            admin.save()
            
            ip_address = get_client_ip(request)
            AdminAccessLog.objects.create(
                developer=developer,
                action=f"Updated Admin Role: {admin.user.username}",
                resource_type="Admin",
                resource_id=admin.id,
                ip_address=ip_address,
                changes_made=json.dumps({'new_role': new_role})
            )
        
        elif action == 'deactivate':
            admin.is_active = False
            admin.save()
            admin.user.is_active = False
            admin.user.save()
            
            ip_address = get_client_ip(request)
            AdminAccessLog.objects.create(
                developer=developer,
                action=f"Deactivated Admin: {admin.user.username}",
                resource_type="Admin",
                resource_id=admin.id,
                ip_address=ip_address
            )
        
        elif action == 'assign_societies':
            society_ids = request.POST.getlist('societies')
            admin.societies.set(society_ids)
            
            ip_address = get_client_ip(request)
            AdminAccessLog.objects.create(
                developer=developer,
                action=f"Updated Admin Societies: {admin.user.username}",
                resource_type="Admin",
                resource_id=admin.id,
                ip_address=ip_address,
                changes_made=json.dumps({'societies_count': len(society_ids)})
            )
        
        return redirect('manage_admin', admin_id=admin_id)
    
    context = {
        'admin': admin,
        'roles': AdminUser.ADMIN_ROLES,
        'all_societies': Society.objects.all(),
        'assigned_societies': admin.societies.all()
    }
    return render(request, 'manage_admin.html', context)

@login_required(login_url='developer_login')
def developer_logout(request):
    """Developer logout"""
    developer = request.user.developeradmin if hasattr(request.user, 'developeradmin') else None
    
    if developer:
        ip_address = get_client_ip(request)
        AdminAccessLog.objects.create(
            developer=developer,
            action="Developer Logout",
            resource_type="System",
            ip_address=ip_address
        )
    
    logout(request)
    return redirect('home')
