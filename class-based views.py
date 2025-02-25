from django.views.generic import DetailView
from .models import Library, Book

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add books related to this library
        context['books'] = self.object.books.all()  # Assuming a ManyToMany or ForeignKey relationship
        return context