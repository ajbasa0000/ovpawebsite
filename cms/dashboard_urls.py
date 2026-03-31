from django.urls import path
from . import dashboard_views

urlpatterns = [
    path('', dashboard_views.dashboard_home, name='dashboard_home'),
    
    # Generic Module Management
    path('m/<str:model_name>/', dashboard_views.module_list, name='module_list'),
    path('m/<str:model_name>/add/', dashboard_views.module_edit, name='module_add'),
    path('m/<str:model_name>/edit/<int:pk>/', dashboard_views.module_edit, name='module_edit'),
    path('m/<str:model_name>/delete/<int:pk>/', dashboard_views.module_delete, name='module_delete'),
    
    # Super Admin: Recycle Bin
    path('recycle-bin/', dashboard_views.recycle_bin, name='recycle_bin'),
    path('recycle-bin/restore/<str:model_class>/<int:pk>/', dashboard_views.restore_item, name='restore_item'),
]
