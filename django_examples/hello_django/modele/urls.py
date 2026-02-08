from django.urls import path
from . import views
urlpatterns = [
    path('instructor/<int:id>/', views.instructor_detail, name='instructor_detail'),
    path("department/create", views.department_create, name='department_create'),
]