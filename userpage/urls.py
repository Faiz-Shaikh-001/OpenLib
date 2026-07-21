from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user_page, name='user-page'),  # Define a name for the user_page URL
    path('user/profile/', views.user_profile, name='user-profile'),
    path('user/book/<int:book_id>/', views.book_detail, name='book-detail'),
    path('user/book/<int:book_id>/borrow/', views.borrow_book, name='borrow-book'),
    path('user/book/<int:record_id>/return/', views.return_book, name='return-book'),
]
