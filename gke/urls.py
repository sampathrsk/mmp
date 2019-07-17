from django.conf.urls import url
import views as v

urlpatterns = [
    url(r'^gke/$',v.gkeconfirm),
    url(r'^gkeredirect/$',v.gkeredirect),
    url(r'^gkeexecute/$',v.gkeexecute),
    url(r'^gketable/$',v.gketable),
    url(r'^gketerminate/cluster_name/$',v.gketerminate)
]