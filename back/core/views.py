from django.db import connection
from django.http import HttpResponse
from django.views.generic import View


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            one = cursor.fetchone()[0]
            if one != 1:  # pragma: no cover
                raise Exception("Not healthy")
        return HttpResponse("ok")
