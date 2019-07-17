from django.conf.urls import url
from eks import views as v

urlpatterns = [
    url(r'^eks/$',v.awseksconfirm),
    url(r'^table/$',v.table),
    url(r'^logs/$',v.logs),
    url(r'^jenkinslog/$',v.jenkinslog),
    url(r'^awseksexecute/$',v.awseksview),
    url(r'^stacklist/$',v.stacklist),
    url(r'^awseksredirect/$',v.awseksredirect),
    url(r'^terminate/cluster_name/$',v.awseksterminate),
    url(r'^gitcreds/$',v.git_creds)
]
