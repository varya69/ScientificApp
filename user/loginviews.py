"""
This code is for a web application that allows sellers to sell products and buyers to purchase them. This particular file contains several functions which carry out different tasks.

The following libraries are imported:
- `APIView` from `rest_framework.views`
- `require_GET` from `django.views.decorators.http`
- `Response` from `rest_framework.response`
- `status` from `rest_framework`
- `filters` from `rest_framework`
- `Q` from `django.db.models`
- `csrf_exempt` from `django.views.decorators.csrf`
- `Http404`, `JsonResponse` from `django.http`
- models (Cart, Product, User, Seller) from `user`
- `json` 
- `TokenObtainPairView` from `rest_framework_simplejwt.views`
- `IsAuthenticated` from `rest_framework.permissions`
- `CustomTokenObtainPairSerializer`, `ProductSerializer` from `user.serializers`

The first three functions (sellerLogin, userLogin, search) take care of authentication and searching for products. The fourth function (create_user) creates a new user. The next two functions (get_users, update_user) retrieve and update the details of all users respectively. The final function (addProductToCart) adds a product to the cart of a particular buyer.

All the functions use the `JsonResponse()` method to return the response in JSON format. The `csrf_exempt` decorator has been used to disable CSRF protection so that POST requests can be made without including a CSRF token in the request header.
"""

from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from django.views.decorators.http import require_GET
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse
from user import models
from user.models import Cart, Product, User, Seller
import json
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from user.serializers import CustomTokenObtainPairSerializer, ProductSerializer

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]

#     def login(self, request, format=None):
#         content = {'message': 'This is a protected endpoint.'}
#         return Response(content)


@csrf_exempt
def sellerLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data\n")
        print(data)
        seller = Seller.objects.filter(SellerEmail=data['SellerEmail'], password=data['password']).first()
        if seller is not None:
            # create a session to keep the user logged in
            # request.session['seller_id'] = seller.id
            return JsonResponse({'message': 'Login successful', 'SellerName': seller.SellerName, 'SellerId': seller.SellerId})
        else:
            return JsonResponse({'error': 'Invalid login credentials'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

@csrf_exempt
def userLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data\n")
        print(data)
        user = User.objects.filter(UserEmail=data['UserEmail'], password=data['password']).first()
        print("\nuser:", user)
        if user is not None:
            # create a session to keep the user logged in
            # request.session['seller_id'] = seller.id
            return JsonResponse({'message': 'Login successful', 'UserName': user.UserName, 'UserId': user.UserId})
        else:
            return JsonResponse({'error': 'Invalid login credentials'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})



@require_GET
def search(request):
    if request.method == 'GET':
        search_term = request.GET.get('search')
        products = Product.objects.filter(
            Q(ProductName__icontains=search_term) | Q(Description__icontains=search_term)
        )
        results = []
        for product in products:
            result = {
                "id": product.id,
                "ProductName": product.ProductName,
                "Description": product.Description,
                "Category": product.Category,
                "Price": product.Price,
                "quantity": product.quantity,
                "image": product.image.url if product.image else None
                }
            results.append(result)

        return JsonResponse({ 'results': results })

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User(
            UserName=data['UserName'],
            UserEmail=data['UserEmail'],
            mobileNo=data['mobileNo'],
            password=data['password'],
        )
        user.save()
        return JsonResponse({'message': 'User created successfully', 'UserName': user.UserName, 'UserId': user.UserId})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
@csrf_exempt
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_list = []
        for user in users:
            user_dict = {
                'UserId': user.UserId,
                'UserName': user.UserName,
                'UserEmail': user.UserEmail,
                'mobileNo': user.mobileNo,
                'password': user.password,
            }
            users_list.append(user_dict)
        return JsonResponse(users_list, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'})

@csrf_exempt
def update_user(request, user_id):
    try:
        user = User.objects.get(UserId=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")

    if request.method == 'PUT':
        data = json.loads(request.body)
        user.UserName = data.get('SellerName', user.UserName)
        user.UserEmail = data.get('SellerEmail', user.UserEmail)
        user.mobileNo = data.get('mobileNo', user.mobileNo)
        user.password = data.get('password', user.password)
        user.save()
        return JsonResponse({'message': 'User updated successfully'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'})
    
@csrf_exempt
def addProductToCart(request):
    if request.method == 'POST':
        product_data = json.loads(request.body)
        # product_data = request.POST.copy()
        # product_id = product_data.pop('productId', None) # Remove 'productId' from product_data
        # user_id = product_data.pop('userId', None) # Remove 'userId' from product_data
        print(product_data)
        # Assuming you have a User model for user authentication and authorization
        # user = User.objects.get(UserId=user_id)
        # if 'image' in product_data:
        #     image = product_data['image']
        #     fs = FileSystemStorage()
        #     filename = fs.save(image.name, image)
        #     uploaded_file_url = fs.url(filename)
        # Create a new Cart object with the extracted data
        cart = Cart(
            ProductName=product_data['ProductName'],
            Description=product_data['Description'],
            Category=product_data['Category'],
            Price=product_data['Price'],
            image=product_data['image'], # Get image from request's FILES data
            quantity=product_data['quantity'],
            user_id=product_data['userId'], # Save productId field with the extracted userId
            productId=product_data['productId'] # Save productId field with the extracted product_id
            # user_id=user_id
        )
        cart.save()

        # Return success response
        response_data = {'message': 'Product added to cart successfully'}
        return JsonResponse(response_data, status=200)

    # Return error response for unsupported request method
    response_data = {'error': 'Invalid request method'}
    return JsonResponse(response_data, status=400)

@csrf_exempt
def get_cartList(request, user_id):
    if request.method == 'GET':
        carts = Cart.objects.filter(user_id=user_id)
        # products = Product.objects.all()
        cart_list = []
        for cart in carts:
            cart_dict = {
                "id": cart.id,
                "ProductName": cart.ProductName,
                "Description": cart.Description,
                "Category": cart.Category,
                "Price": cart.Price,
                "quantity": cart.quantity,
                "image": cart.image if cart.image else None,
                "user_id": cart.user_id,
                "productId" : cart.productId
            }
            cart_list.append(cart_dict)
        return JsonResponse(cart_list, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'})
    
@csrf_exempt
def delete_cart(request, cartId):
    try:
        cart = Cart.objects.get(pk=cartId)
        print(cart)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist")

    if request.method == 'DELETE':
        cart.delete()
        return JsonResponse({'message': 'Remove item from Cart successfully'})
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'})
            
