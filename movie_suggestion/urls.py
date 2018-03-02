from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import logout

urlpatterns = [
                path('', include('suggestions.urls')),
                path('login/', auth_views.login, name='login'),
                path('logout/', logout, {'next_page': '/login/'}, name='logout'),
                path('admin/', admin.site.urls),
                path('suggestions/', include('suggestions.urls')),
                path('register/', CreateView.as_view(template_name='registration/register.html', form_class=UserCreationForm, success_url='/suggestions/'), name='register'),
             ]
