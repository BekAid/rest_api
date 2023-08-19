from django.db.models import Avg, Count
from rest_framework import generics
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, DirectorCreateUpdateSerializer


# views.py

class DirectorList(generics.ListCreateAPIView):
    queryset = Director.objects.annotate(movies_count=Count('movie'))
    serializer_class = DirectorSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DirectorCreateUpdateSerializer
        return self.serializer_class

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# views.py

# views.py

class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return DirectorCreateUpdateSerializer
        return self.serializer_class


# views.py

class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer



# views.py

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


class MovieReviewList(generics.ListAPIView):
    queryset = Movie.objects.annotate(avg_rating=Avg('reviews__stars'))
    serializer_class = MovieSerializer



