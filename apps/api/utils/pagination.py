from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size_query_param = "size"
    page_size = 6
    max_page_size = 6
    page_query_param = "page"
