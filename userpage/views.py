from datetime import timedelta
from maincontent.models import BorrowRecord
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from maincontent.models import Book
from django.contrib import messages
from django.utils import timezone
from django.db.models.query_utils import Q


@login_required
def user_page(request):
    if check_role(request) != "user":
        return redirect('admin-page')
    query = request.GET.get('search', '').strip()
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'userpage/user-page.html', {
        'books': books,
        'search_query': query,
    })


@login_required
def user_profile(request):
    if check_role(request) != "user":
        raise PermissionDenied
    
    borrowed_records = BorrowRecord.objects.filter(user=request.user).order_by('-borrow_date')
    return render(request, 'userpage/profile.html', {'borrowed_records': borrowed_records})


@login_required
def book_detail(request, book_id):
    if check_role(request) != "user":
        raise PermissionDenied
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'userpage/book-detail.html', {'book': book})


def check_role(request):
    is_super = getattr(request.user, 'is_superuser', False)
    user_role = getattr(request.user, 'role', 'admin' if is_super else 'user')
    return user_role


@login_required
def borrow_book(request, book_id):
    if check_role(request) != "user":
        raise PermissionDenied()
    
    book = get_object_or_404(Book, id=book_id)

    if book.available_copies < 1:
        messages.error(request, f"Sorry, '{book.title}' is currently out of stock.")
        return redirect('book-detail', book_id=book.id)
    
    existing_borrow = BorrowRecord.objects.filter(user=request.user, book=book, status='borrowed').first()

    if existing_borrow:
        messages.warning(request, f"You have already borrowed '{book.title}'.")
        return redirect('book-detail', book_id=book.id)

    due_date = timezone.now().date() + timedelta(days=14)
    BorrowRecord.objects.create(
        user=request.user,
        book=book,
        due_date=due_date,
        status='borrowed'
    )
    book.available_copies -= 1
    book.save()

    messages.success(request, f"Successfully borrowed '{book.title}'! Due date: {due_date}.")
    return redirect('book-detail', book_id=book.id)


@login_required
def return_book(request, record_id):
    if check_role(request) != 'user':
        raise PermissionDenied
    
    record = get_object_or_404(BorrowRecord, id=record_id, user=request.user)

    if record.status == 'returned':
        messages.error(request, "This book has already been returned.")
        return redirect('user-profile')
    
    record.status = 'returned'
    record.return_date = timezone.now().date()
    record.save()

    book = record.book
    book.available_copies += 1
    book.save()

    messages.success(request, f"Successfully returned '{book.title}'. Thank you!")

    return redirect('user-profile')

