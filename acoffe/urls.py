from django.urls import path, include

import acoffe.views as v

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'coffe-api', v.CoffeViewSet)
router.register(r'ingridient-api', v.IngridientViewSet)

urlpatterns = [
    path('', v.home_page, name='home_page'),
    # path('list/', v.list_coffe, name='list_coffe'),
    path('registration/', v.user_registration, name='regis'),
    path('login/', v.user_login, name='log in'),
    path('logout/', v.user_logout, name='log out'),



    # ListView
    path('list/', v.CoffeList.as_view(), name='list_coffe'),
    path('delete/<int:coffe_id>', v.CoffeDelete.as_view(), name='delete_coffe'),
    path('update/<int:coffe_id>', v.CoffeUpdate.as_view(), name='update_coffe'),
    path('create/', v.get_add_coffe, name='create_coffe'),
    # path('create/', v.CoffeCreate.as_view(), name='create_coffe'),

    path('list/<int:coffe_id>/', v.detail_coffe, name='detail_coffe'),

    # EMAIL
    path('contact/', v.contact_email, name='contact_email'),

    # API
    path('viewset/', include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)