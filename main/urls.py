from django.urls import path
from . views import *

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('candidate/<int:pk>', AdminCandidatePageView.as_view(), name='AdminCandidatePageView'),
    path('candidate/<int:pk>/report', CandidateReportPageView.as_view(), name='CandidateReportPageView'),
    path('media/uploads/<str:text>/<str:userid>/<str:file>', secureView, name='secure'),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),
]