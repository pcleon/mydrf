from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from common.utils import MyResponse


class MyPageNumberPagination(PageNumberPagination):
    page_size = 2  # 默认每页显示的多少条记录
    page_query_param = 'page'  # 默认查询参数名为 page
    page_size_query_param = 'limit'  # 前台控制每页显示的最大条数
    max_page_size = 10  # 后台控制显示的最大记录条数

    @MyResponse
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            ('results', data)
        ]))