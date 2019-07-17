from django.conf.urls import url
from infrasetup import views as v

urlpatterns = [
      url(r'^form/$', v.awsview), # Notice the URL has been named
      url(r'^clustertable/$',v.clustertable),
      url(r'^terminate/clustername/$',v.clusterterminate),
      url(r'^ajax/VpcLaunch/$', v.VpcLaunch), # Notice the URL has been named
      url(r'^ajax/clusternamecheck/$', v.clusternamecheck),
      url(r'^ajax/masterasgnamecheck/$', v.masterasgnamecheck),
      url(r'^ajax/slaveasgnamecheck/$', v.slaveasgnamecheck),
      url(r'^form1/$', v.infoview), # Notice the URL has been named
      url(r'^guestbook/$', v.guestbook),    
      url(r'^select/$', v.select),
]
