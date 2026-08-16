from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dash_board_view, name='dash_board_view'),
    path('tasks/create/', views.create_task_view, name='create_task'),
    path('tasks/<int:task_id>/submit/', views.submit_task_view, name='submit_task'),
    path('tasks/<int:task_id>/verify/', views.verify_task_view, name='verify_task'),
    path('logout/', views.logout_view, name='logout'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
