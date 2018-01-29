from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import rockworthy.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', rockworthy.views.index, name='index'),
    url(r'^db', rockworthy.views.db, name='db'),
    #url(r'^token', rockworthy.views.createToken, name='create-token'),
    url(r'^token', rockworthy.views.createToken, name='generate-token'),
    url(r'^chat/', rockworthy.views.chat, name='chat'),
    url(r'^user-logged-in/', rockworthy.views.user_logged_in, name='user-logged-in'),
    url(r'^user-chat-join/', rockworthy.views.user_chat_join, name='user-chat-join'),
    url(r'^user-chat-start/', rockworthy.views.user_chat_start, name='user-chat-start'),
    path('admin/', admin.site.urls),
]
