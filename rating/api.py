from django.http.response import JsonResponse
from rating import serializers
from rest_framework.views import APIView
from rating.models import User, MovieRatings
from rating.serializers import MovieRatingsSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from functools import reduce
from django.db.models import Q

# Create you APIs Logic here

class MovieDetails(APIView):
    """
    API View for Post Show listing
    """
    def get(self, request, version):
        try:
            authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
            serializer_class = MovieRatingsSerializer
            instance = MovieRatings.objects.all()
            if request.GET.get('sorted_by'):
                sorted_by = request.GET['sorted_by']
                if sorted_by == 'name' or sorted_by == '-name':
                    instance = instance.order_by(sorted_by)
                if sorted_by == 'rating' or sorted_by == '-rating':
                    instance = instance.order_by(sorted_by)
                if sorted_by == 'release_date' or sorted_by == '-release_date':
                    instance = instance.order_by(sorted_by)
                if sorted_by == 'duration' or sorted_by == '-duration':
                    instance = instance.order_by(sorted_by)
            # Search movie by name
            if request.GET.get('search_by_name'):
                search_items = request.GET['search_by_name'].split(' ')
                search_items = list(filter(None, search_items))
                if search_items:
                    instance = instance.filter(reduce(lambda x, y: x & y, [Q(name__icontains=word) for word in search_items]))
                    if not instance:
                        instance = instance.filter(reduce(lambda x, y: x | y, [Q(name__icontains=word) for word in search_items]))
            
            serializer = MovieRatingsSerializer(instance, many= True)
            return JsonResponse({"status": 200,
                        "message": "Successfully Retrieved Movie Details",
                        "data": serializer.data})

        except Exception as e:
            print(e)
            return JsonResponse({"status": 500,
                            "message": "Something went wrong please try after sometime.",
                            "data": {}})

