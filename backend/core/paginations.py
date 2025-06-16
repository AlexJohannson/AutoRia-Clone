from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PagePagination(PageNumberPagination):
    page_size = 6
    max_page_size = 10
    page_size_query_param = 'size'

    def paginate_queryset(self, queryset, request, view=None):
        if not queryset.ordered:
            queryset = queryset.order_by('id')
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'prev': bool(self.get_previous_link()),
            'next': bool(self.get_next_link()),
            'data': data
        })


