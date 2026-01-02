from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    max_page_size = 100
    
    def get_paginated_response(self, data):
        message={
            "status":200,
            'message': 'Paginated data',
            'total_pages': self.page.paginator.num_pages,
            'total_Count': self.page.paginator.count,
            # 'current_page': self.page.number,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'data': data
        }
        return Response(message)