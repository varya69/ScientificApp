from django.urls import path
# from django.conf.urls import url
from user import views, loginviews

urlpatterns = [
    # path('^user/', views.userApi),
    path('', views.get_sellers, name='seller'),
    # path('^user/([0-9]+)$', views.userApi),
    path('seller/', views.create_seller),
    path('user/', loginviews.create_user),
    path('seller-login/', loginviews.sellerLogin),
    path('user-login/', loginviews.userLogin),
    path('seller/', views.get_sellers),
    path('seller/<int:seller_id>/', views.update_seller),
    path('seller/<int:seller_id>/', views.delete_seller),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('add-product/<int:id>', views.add_product, name='add-product'),
    path('product-list/<int:id>', views.product_list, name='product-list'),
    path('products/<int:id>', views.delete_product, name='delete_product'),
    path('product/<int:id>', views.get_product, name='get_product'),
    path('update_product/<int:id>', views.update_product, name='update_product'),
    path('all-products/', views.all_products, name='all_products'),
    path('products/', loginviews.search, name='search'),
    path('cart/', loginviews.addProductToCart, name='cart'),
    path('get_cart/<int:user_id>', loginviews.get_cartList, name='get_cart'),
    path('delete-cart/<int:cartId>', loginviews.delete_cart, name='delete-cart'),
    # path('', views.userApi, name='user'),
    # path('seller/([0-9]+)$', views.seller_api),
]
