from django.shortcuts import render
from rest_framework import status,serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product
from django.http import HttpResponse

def index(request):
    return HttpResponse('haproxy check')

params=['id','amount','price','date', 'title', 'unit']
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = params

@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
def ProductView(request):
    if request.method == 'GET':
        products = Product.objects.all()#выбор всех объектов
        serializer = ProductSerializer(products, many=True)#Serializer для вывода всех объектов
        return Response({"resourses" : serializer.data,
                         "total_count": Product.objects.all().count()},#вывод количества
                        status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)#Serializer для создания объекта
        if serializer.is_valid():#проверка JSON объекта
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'UPDATE':
        data={}#создание словаря обновляемых полей
        for each in request.POST:#добавление данных полей из параметра запроса
            if each in params:
                data[each] = request.POST.get(each)
            else:
                return Response('', status=status.HTTP_400_BAD_REQUEST)#поле не существует
        if not('id' in data):
            return Response('', status=status.HTTP_400_BAD_REQUEST)#отсутсвует id
        if Product.objects.filter(id=request.POST.get('id')).count():
            product=Product.objects.filter(id=data['id'])[0]#выбор объекта по id
            serializer = ProductSerializer(product,
                                           data=request.data,
                                           partial=True)#Serializer для обновления объекта
            if serializer.is_valid():
                serializer.save()
                return Response('', status=status.HTTP_202_ACCEPTED)
        return Response('', status=status.HTTP_400_BAD_REQUEST)#id не найден

    elif request.method == 'DELETE':
        params0=['id']
        for each in request.POST:
            if each in params0:
                pass
            else:
                return Response('', status=status.HTTP_400_BAD_REQUEST)#параметр отличный от id
        if request.POST.get('id')==None:
            return Response('', status=status.HTTP_400_BAD_REQUEST)#отсутсвует id
        if Product.objects.filter(id=request.POST.get('id')).count():
            Product.objects.filter(id=request.data['id']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('', status=status.HTTP_400_BAD_REQUEST)#id не найден

@api_view(['GET'])
def Cost(request):
    if request.method == 'GET':
        total_cost=0#объявление общей стоимости
        for each in Product.objects.all():
            total_cost+=each.price#добавление цены каждого объекта
        return Response({"total_cost": total_cost}, status=status.HTTP_200_OK)