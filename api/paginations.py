from rest_framework.pagination import LimitOffsetPagination


class LimitResultsPagination(LimitOffsetPagination):
    max_limit = 100
