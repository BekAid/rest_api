from django.db.models import Count, Avg
from rest_framework import serializers, generics
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ('id', 'name', 'movies_count')

    def get_movies_count(self, obj):
        return obj.movie_set.count()


class DirectorList(generics.ListAPIView):
    queryset = Director.objects.annotate(movies_count=Count('movie'))
    serializer_class = DirectorSerializer


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'stars')


class MovieSerializer(serializers.ModelSerializer):
    director_name = serializers.ReadOnlyField(source='director.name')
    reviews = ReviewSerializer(many=True)
    avg_rating = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        return ReviewSerializer(reviews, many=True).data

    def get_avg_rating(self, obj):
        return obj.reviews.aggregate(Avg('stars'))['stars__avg']

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'duration','director', 'director_name', 'reviews', 'avg_rating')



