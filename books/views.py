from rest_framework import generics, filters
from .models import Book
from .serializers import BookSerializer

class BookListAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        max_price = self.request.query_params.get('max_price')
        search = self.request.query_params.get('search')

        if category and category != 'All':
            queryset = queryset.filter(category__iexact=category)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | models.Q(author__icontains=search)
            )

        return queryset