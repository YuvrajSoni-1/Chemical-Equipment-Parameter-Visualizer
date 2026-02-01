from django.urls import path
from .views import UploadView, HistoryView, AnalysisView, ReportView, APIRootView

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('history/', HistoryView.as_view(), name='history'),
    path('analysis/<int:id>/', AnalysisView.as_view(), name='analysis'),
    path('report/<int:id>/', ReportView.as_view(), name='report'),
]
