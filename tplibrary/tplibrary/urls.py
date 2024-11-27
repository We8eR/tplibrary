# tplibrary/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from impotrttp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtp/', views.addtp, name='addtp'),
    path('admin/', admin.site.urls),
    path('data/', views.data, name='data'),
    # Управление пользователями
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    # Управление справочниками
    path('dictionaries/', views.dictionaries, name='dictionaries'),
    path('dictionaries/role/add/', views.add_role, name='add_role'),
    path('dictionaries/role/delete/<int:role_id>/', views.delete_role, name='delete_role'),
    path('dictionaries/workshop/add/', views.add_workshop, name='add_workshop'),
    path('dictionaries/workshop/delete/<int:workshop_id>/', views.delete_workshop, name='delete_workshop'),
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html', next_page='index'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
