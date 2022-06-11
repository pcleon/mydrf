from rest_framework.views import APIView
from .models import BookInfo
from .serializers import BookModelSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView, get_object_or_404

# 定义类 继承APIView 多Book的操作
class BookListAPIView(APIView):
    '''
        View获取数据方式:
            GET：
                request.GET
            POST:
                request.POST
                request.body
        APIView获取数据方式：
            GET:
                request.query_params
            POST:
                request.data
    '''

    def get(self, request):
        # 请求字段 request.query_params
        books = BookInfo.objects.all()
        serializer = BookModelSerializer(instance=books, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        # 请求字段 request.data
        data = request.data
        serializer = BookModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 定义类 继承APIView 单Book的操作
class BookOneAPIView(APIView):
    def get(self, request, id):
        book = BookInfo.objects.get(id=id)
        serializer = BookModelSerializer(instance=book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        data = request.data
        book = BookInfo.objects.get(id=id)
        serializer = BookModelSerializer(instance=book, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        BookInfo.objects.get(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 二级视图 SecondAPIView
'''
特点: 
    1.继承自APIView，为列表视图和详情视图添加了常用的行为和属性
    2.可以和一个或者多个mixin类配合使用   
    mixin: 为了扩展功能，封装请求方法

属性：
    queryset
    serializer_class
    lookup_url_kwarg
方法：
    get_queryset()
    get_serialize()
    get_object() 根据id自动获得单个对象  id字段必须命名为pk
'''


# 多个元素操作
class BookListSecondAPIView(GenericAPIView):
    # 1.提供公共的属性
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer
    lookup_url_kwarg = 'id'  # 改变get_object()字段的名称

    def get(self, request):
        # 请求字段 request.query_params
        # books = self.queryset
        books = self.get_queryset()
        # serializer = BookModelSerializer(instance=books,many=True)
        serializer = self.serializer_class(instance=books, many=True)
        # serializer = self.get_serializer(instance=books,many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        # 请求字段 request.data
        data = request.data
        serializer = BookModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 单个元素操作
class BookOneSecondAPIView(GenericAPIView):
    # 1.提供公共的属性
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer
    lookup_url_kwarg = 'id'  # 改变get_object()字段的名称

    def get(self, request, id):
        book = self.get_object()
        serializer = BookModelSerializer(instance=book)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id):
        data = request.data
        book = self.get_object()
        serializer = BookModelSerializer(instance=book, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
Mixin
1.用于提供基本视图行为（列表视图、详情试图）的操作
2.配合二级试图使用

类名称              方法            功能
ListModelMixin      list           查询所有
CreateModelMixin    create         创建一个
RetrieveModelMixin  retrieve       查询一个
UpdateModelMixin    update         更新一个
DestroyModelMixin   destroy        删除一个  
'''
from rest_framework import mixins


# Mixin和GenericAPIView,实现列表视图
class BookListMixinSecondAPIView(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    # 1.提供公共的属性
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BookOneMixinSecondAPIView(GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin):
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer
    lookup_url_kwarg = 'id'  # 改变get_object()字段的名称

    def get(self, request, id):
        return self.retrieve(request)

    def put(self, request, id):
        return self.update(request)

    def delete(self, request, id):
        return self.destroy(request)


'''
三级视图 --通用的视图
特点：
    无大量的自定义行为，可以使用三级视图来解决

三级视图：
类名称               父类               方法       功能
CreateAPIView       二级视图，Mixin     post       创建一个对象
ListAPIView         ...                get        查询所有数据
RetrieveAPIView     ...                get        查询单个数据
DestroyAPIView      ...                delete      删除一个对象
UpdateAPIView       ...                put/potch      更新一个对象
'''
# 三级视图实现列表和详情
from rest_framework import generics


class BookListThirdAPIView(generics.ListAPIView, generics.CreateAPIView):
    # 1.提供公共的属性
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer


class BookOneThirdAPIView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer
    lookup_url_kwarg = 'id'  # 改变get_object()字段的名称


'''
视图集
    特点：
    1.将一组相关的操作，放在一个类中进行完成
    2.不提供get，post方法，使用retrieve，create方法来替代
    3.可以将标准的请求方式和mixin的方法做映射

常见的视图集
类名称                          父类                        作用
ViewSet                   APIView/ViewSetMixin             可以做路由映射
GenericViewSet          GenericAPIView/ViewSetMixin        可以做路由映射，可以使用三个属性三个方法
ModeViewSet             GenericAPIView/5个Mixin类           三个属性三个方法和所有的增删改查
ReadOnlyModelViewSet    GenericAPIView/2个获取Mixin类       可以获取单个和所有数据
'''

# ViewSet   获取所有和单个数据
from rest_framework import viewsets


class BookViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = BookInfo.objects.all()
        serializer = BookModelSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = BookInfo.objects.all()
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookModelSerializer(instance=book)
        return Response(serializer.data)


# 使用 ReadOnlyModelViewSet获取所有和单个数据
class BookReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer


# 使用ModeViewSet 完成所以功能
class BookModeViewSet(viewsets.ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer
