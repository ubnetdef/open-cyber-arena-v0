from django.urls import path

from arena.pods import views


app_name = 'pods'

urlpatterns = [
    path('', views.PodListView.as_view()),
    path('vms/<int:pk>/', views.VirtualMachineDetailView.as_view()),
    path('vms/<int:pk>/credentials/', views.VirtualMachineCredentialsView.as_view()),
    path('vms/<int:pk>/power/<state>/', views.VirtualMachinePowerView.as_view()),
]
