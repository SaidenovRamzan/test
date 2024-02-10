from .book import (
    AddBookView, BookView,
    BookCreateView, BookDetailView, BookUpdateView,
    BookDeleteView, AddGenreView, 
)
from .compostion import (
    SearchCompositionView, CompositionCreateView, CompositionDetailView,
    CompositionUpdateView, CompositionDeleteView, HomeView, ListOfCompositionsView,
    CompositionAdminListView
)
from .comment import add_comment
from .favorite import favorite_unfavor, delete_from_favorite
from .create_all_in_one import AllInOneView
