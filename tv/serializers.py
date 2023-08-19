from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, generics
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ('id', 'name', 'movies_count')

    def get_movies_count(self, obj):
        return obj.movie_set.count()


# serializers.py

class DirectorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        exclude = ('id',)  # Исключаем поле 'id', если оно не должно изменяться


# serializers.py

# serializers.py

class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Review
        fields = ('id', 'text', 'stars', 'movie')



class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'duration', 'director', 'reviews', 'avg_rating')

    def get_avg_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.count() > 0:
            return sum(review.stars for review in reviews) / reviews.count()
        else:
            return 0



class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'duration', 'director')


# views.py

class DirectorList(generics.ListCreateAPIView):
    queryset = Director.objects.annotate(movies_count=Count('movie'))
    serializer_class = DirectorSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DirectorCreateUpdateSerializer
        return self.serializer_class


class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DirectorCreateUpdateSerializer
        return self.serializer_class


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MovieCreateUpdateSerializer
        return self.serializer_class


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MovieCreateUpdateSerializer
        return self.serializer_class


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        movie_id = self.kwargs.get('movie_id')
        movie = get_object_or_404(Movie, id=movie_id)
        serializer.save(movie=movie)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


class MovieReviewList(generics.ListAPIView):
    queryset = Movie.objects.annotate(avg_rating=Avg('reviews__stars'))
    serializer_class = MovieSerializer
