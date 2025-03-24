from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Video, Contact, Profile, Room
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    videos = Video.objects.all()[:3]  # Get latest 3 videos
    return render(request, 'core/home.html', {'videos': videos})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact = Contact.objects.create(
            name=name,
            surname=surname,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        # Send email notification
        send_mail(
            f'New Contact Form Submission: {subject}',
            f'Name: {name} {surname}\nEmail: {email}\nPhone: {phone}\nMessage: {message}',
            email,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        
        messages.success(request, '¡Su mensaje ha sido enviado exitosamente!')
        return redirect('contact')
    
    return render(request, 'core/contact.html')

@login_required
def room_list(request):
    rooms = Room.objects.all().order_by('date', 'time')
    return render(request, 'core/room_list.html', {'rooms': rooms})

@staff_member_required
def create_room(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        meeting_link = request.POST.get('meeting_link')
        
        room = Room.objects.create(
            title=title,
            date=date,
            time=time,
            meeting_link=meeting_link,
            created_by=request.user
        )
        
        messages.success(request, 'Sala creada exitosamente!')
        return redirect('room_list')
    
    return redirect('room_list')

@staff_member_required
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Sala eliminada exitosamente!')
    return redirect('room_list')

@staff_member_required
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.title = request.POST.get('title')
        room.date = request.POST.get('date')
        room.time = request.POST.get('time')
        room.meeting_link = request.POST.get('meeting_link')
        room.save()
        messages.success(request, 'Sala actualizada exitosamente!')
    return redirect('room_list')

@login_required
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'core/video_list.html', {'videos': videos})

@login_required
def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'core/video_detail.html', {'video': video})

@staff_member_required
def video_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        url = request.POST.get('url')
        summary = request.POST.get('summary')
        
        video = Video.objects.create(
            title=title,
            url=url,
            summary=summary
        )
        
        messages.success(request, 'Video agregado exitosamente!')
        return redirect('video_list')
    
    return redirect('video_list')

@staff_member_required
def video_edit(request, pk):
    video = get_object_or_404(Video, pk=pk)
    
    if request.method == 'POST':
        video.title = request.POST.get('title')
        video.url = request.POST.get('url')
        video.summary = request.POST.get('summary')
        video.save()
        
        messages.success(request, 'Video actualizado exitosamente!')
        return redirect('video_list')
    
    return redirect('video_list')

@staff_member_required
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video eliminado exitosamente!')
    
    return redirect('video_list')

@login_required
def profile(request):
    # Ensure profile exists
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user = request.user
        
        if 'update_profile' in request.POST:
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            messages.success(request, '¡Perfil actualizado exitosamente!')
        
        elif 'update_picture' in request.POST and request.FILES.get('profile_picture'):
            user.profile.profile_picture = request.FILES['profile_picture']
            user.profile.save()
            messages.success(request, '¡Foto de perfil actualizada exitosamente!')
        
        elif 'change_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            if user.check_password(current_password):
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, '¡Contraseña actualizada exitosamente!')
                    return redirect('login')
                else:
                    messages.error(request, 'Las nuevas contraseñas no coinciden.')
            else:
                messages.error(request, 'La contraseña actual es incorrecta.')
        
        elif 'create_user' in request.POST and request.user.is_staff:
            new_username = request.POST.get('new_username')
            new_email = request.POST.get('new_email')
            new_password = request.POST.get('new_password')
            new_is_staff = request.POST.get('new_is_staff') == 'on'
            
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'El nombre de usuario ya existe.')
            elif User.objects.filter(email=new_email).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
            else:
                new_user = User.objects.create_user(
                    username=new_username,
                    email=new_email,
                    password=new_password,
                    is_staff=new_is_staff
                )
                messages.success(request, f'Usuario {new_username} creado exitosamente')
        
        elif 'toggle_staff' in request.POST and request.user.is_staff:
            user_id = request.POST.get('user_id')
            target_user = User.objects.get(id=user_id)
            target_user.is_staff = not target_user.is_staff
            target_user.save()
            messages.success(request, f'Estado de staff actualizado para {target_user.username}')
        
        elif 'delete_user' in request.POST and request.user.is_staff:
            user_id = request.POST.get('user_id')
            if int(user_id) != request.user.id:
                User.objects.get(id=user_id).delete()
                messages.success(request, 'Usuario eliminado exitosamente')
            else:
                messages.error(request, 'No puedes eliminar tu propio usuario')
        
        return redirect('profile')
    
    context = {
        'user': request.user,
        'users': User.objects.all() if request.user.is_staff else None
    }
    return render(request, 'core/profile.html', context)
