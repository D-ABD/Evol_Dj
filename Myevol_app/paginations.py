from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

class MyEvolPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    
    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "meta": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer", "example": 52},
                        "total_pages": {"type": "integer", "example": 6},
                        "current_page": {"type": "integer", "example": 2},
                        "next": {"type": "string", "nullable": True, "example": "https://api.myevol.app/api/badges/?page=3"},
                        "previous": {"type": "string", "nullable": True, "example": "https://api.myevol.app/api/badges/?page=1"},
                        "page_size": {"type": "integer", "example": 10},
                    }
                },
                "results": {
                    "type": "array",
                    "items": {"type": "object"},
                },
            },
        }
    )
    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'meta': {
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'page_size': self.get_page_size(self.request),
            },
            'results': data
        })
