from django.conf.urls import patterns, include, url
from django.contrib import admin
from cms_users_put import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', login, {'template_name': 'registration/login.html'}),
    url(r'^logout', logout, {'next_page': '/'}),
    url(r'^$', views.barra, name='Inicio'),
    url(r'(.+)', views.pag, name='Pagina'),
    url(r'.*', views.error, name='Error'),
)
