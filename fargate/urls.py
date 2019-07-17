from django.conf.urls import url
from fargate import views as v

urlpatterns = [
    url(r'^fg/$',v.awsfgconfirm),
    url(r'^fgtable/$',v.table),
    url(r'^awsfgexecute/$',v.awsfgview),
    url(r'^awsfgredirect/$',v.awsfgredirect),
    url(r'^fgterminate/cluster_name/$',v.awsfgterminate)
]
