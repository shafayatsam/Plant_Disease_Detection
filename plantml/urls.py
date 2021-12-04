from django.urls import path, re_path
from django.urls.resolvers import URLPattern

from .views import (AllDiseaseView, 
                    PredictionView, 
                    DiseaseInfoView, 
                    HomePageView, 
                    PredicPageView, 
                    DiseaseDetailView, 
                    ReviewListView, 
                    ReviewCreateView)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('upload', PredictionView.as_view(), name='upload'),
    path('info/<disease>', PredicPageView.as_view(), name='disease_info'),
    path('info/', DiseaseInfoView.as_view(), name='disease_info'),
    path('list_disease/', AllDiseaseView.as_view(), name='all_diseases'),
    path('disease/<int:pk>/', DiseaseDetailView.as_view(), name='disease_detail'),
    path('review-list', ReviewListView.as_view(), name='review_list'),
    path('review', ReviewCreateView.as_view(), name='review')
]