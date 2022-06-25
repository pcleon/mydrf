from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
    page_size = 2  # 默认每页显示的多少条记录
    page_query_param = 'page'  # 默认查询参数名为 page
    page_size_query_param = 'size'  # 前台控制每页显示的最大条数
    max_page_size = 10  # 后台控制显示的最大记录条数