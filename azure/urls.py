from django.conf.urls import url
from azure import views as v

urlpatterns = [
    url(r'^aks/$',v.home),
    url(r'^ftable/$',v.ftable),
    url(r'^baseaks/$',v.data_view),
    url(r'^temp_details/$', v.temp_details),
    url(r'^terminate/cluster_name/$',v.azureaksterminate),
    url(r'^aksinfo/$', v.redirect),
    url(r'^gitcreds/$',v.git_creds)
]


