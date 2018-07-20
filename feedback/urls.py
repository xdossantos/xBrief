from django.conf.urls import url

from . import views

app_name='feedback'

urlpatterns = [
    url(r"^$", views.FeedbackList.as_view(), name="all"),
    url(r"new/$", views.CreateFeedback.as_view(), name="create"),
    url(r"by/(?P<username>[-\w]+)/$",views.UserFeedback.as_view(),name="for_user"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.FeedbackDetail.as_view(),name="single"),
    url(r"delete/(?P<pk>\d+)/$",views.DeleteFeedback.as_view(),name="delete"),
]
