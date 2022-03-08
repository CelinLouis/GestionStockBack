from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class PaginationLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 5


class PaginationPageNumberPagination(PageNumberPagination):
    page_size = 10