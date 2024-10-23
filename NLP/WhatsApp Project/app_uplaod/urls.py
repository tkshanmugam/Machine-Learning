from django.conf.urls import url
from app_uplaod import views
from django.urls import path

app_name = 'app_upload'

urlpatterns = [
    path('', views.FileUploadView.as_view(), name = 'image_upload'),
    #path('whats', views.WhatsappAnalaysis.as_view(), name = 'whats'),
    path('result', views.finalresult.as_view(), name= 'result'),
    path('success', views.Success.as_view(), name = 'success'),
    path('fail',views.Failure.as_view(),name='fail'),
    path('filenot',views.FileNotfound.as_view(), name='filenot'),
    path('aboutus',views.AboutUs.as_view(), name='aboutus')
]
