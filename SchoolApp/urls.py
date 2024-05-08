from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include
from SchoolApp import admin
from .views import*


router = DefaultRouter()
router.register('students', StudentViewSet)
router.register('parents', ParentViewSet)
router.register('teachers', TeacherViewSet)
router.register('cls', ClsViewSet)

urlpatterns = [

    path('', include(router.urls)),
    path('login/', UserLoginViewSet.as_view(), name='student login'),
    path('register/', RegistrationView.as_view(), name='register'),
]