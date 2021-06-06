from rest_framework import serializers
from rating.models import MovieRatings

class MovieRatingsSerializer(serializers.ModelSerializer):
    """
    The serialzers to serializer and Deserialzer
    MovieRatings object
    """
    class Meta:
        model = MovieRatings
        fields = '__all__'