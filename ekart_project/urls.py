"""clg_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ekart_app import views
from ekart_project import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

admin.site.site_header = "Ekart's Admin Page"
admin.site.site_title = "EkartAdmin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('signup',views.signup),
    path('login',views.login),
    path('newuser',views.newusr),
    path('loguser',views.logusr),
    path('logout',views.logout),
    path('srch',views.srch),
    path('productpg',views.productpg, name='productpg'),
    path('buyd',views.buydirect),
    path('items',views.QuantityChange),
    path('buy',views.buyfrmcrt, name='buyconfirm'),
    path('buypg',views.buypg),
    path('delcrt',views.delcart),
    path('delItm',views.delitem),
    path('cart',views.usercart),
    path('newreview',views.user_review),
    # path('chngrev',views.chngreview),
    path('delrev',views.delreview),
    path('userpg',views.user_page, name='userpage'),
    # path('userpage',views.userpage),
    path('deladdr',views.deladdr),
    path('addaddr',views.addaddr),
    path('chngDetail',views.changeUserDetails),
    path('aboutus',views.aboutus),
    path('catpg',views.catpg),
    path('typepg',views.typpg),
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

