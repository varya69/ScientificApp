from rest_framework.views import APIView
from django.views.decorators.http import require_GET
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse
from user import models
from user.models import Product, User, Seller
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
def login(request):
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
                "image": product.image.url if product.image else None
                }
            results.append(result)

        return JsonResponse({ 'results': results })

# def search(self, request):
#         if request.method == 'GET':
#             queryset = Product.objects.all()
#             serializer_class = ProductSerializer
#             filter_backends = [filters.SearchFilter]
#             search_fields = ['name', 'description', 'category']
#             return Response(filter_backends.data)
#         else:
#              pass

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth import authenticate, login

# class LoginView(APIView):
#     def login(self, request, format=None):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return Response({'detail': 'Authentication successful.'})
#         else:
#             return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
