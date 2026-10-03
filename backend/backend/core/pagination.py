from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for Resource_Collection responses.

    - page_size = 20: default page size when no client page size is supplied (5.1).
    - page_size_query_param = 'page_size': lets clients override the page size (5.3);
      invalid values are ignored and the default is used (5.8).
    - max_page_size = 100: hard cap even when a larger value is requested (5.4).

    Every response carries ``count``, ``next``, and ``previous`` (5.5), with the
    next/previous links null on the last/first page respectively.

    Requirements: 5.1, 5.3, 5.4, 5.5, 5.8
    """

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
