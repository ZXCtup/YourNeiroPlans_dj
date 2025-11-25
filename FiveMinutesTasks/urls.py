from django.urls import path

from .views import (
    About,
    IndexPage,
    PlanListView,
    PlanCreateView,
    PlanDetailView,
    UserProfileView,
    UserPlansView,
    
)

urlpatterns = [
    path('', IndexPage.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('plans/', PlanListView.as_view(), name='allplans'),
    path('plans/create/', PlanCreateView.as_view(), name='plan-create'),
    path('plans/<slug:slug>/', PlanDetailView.as_view(), name='plan-detail'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('user/<str:username>/plans/', UserPlansView.as_view(), name='user-plans'),
    
]