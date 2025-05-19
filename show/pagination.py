from rest_framework.pagination import PageNumberPagination


class EventSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 20


class EventSessionSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = "page_size"
    max_page_size = 20
