from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from maincontent.models import Book, BorrowRecord


def check_role(request):
    """
    Django superusers are always administrators.

    Normal users use the application-level role stored
    on CustomUser.
    """
    if request.user.is_superuser:
        return "admin"

    return getattr(
        request.user,
        "role",
        "user",
    )


@login_required
def user_page(request):
    if check_role(request) != "user":
        return redirect("admin-page")

    query = request.GET.get(
        "search",
        "",
    ).strip()

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()

    return render(
        request,
        "userpage/user-page.html",
        {
            "books": books,
            "search_query": query,
        },
    )


@login_required
def user_profile(request):
    if check_role(request) != "user":
        raise PermissionDenied

    borrowed_records = BorrowRecord.objects.filter(
        user=request.user
    ).order_by("-borrow_date")

    return render(
        request,
        "userpage/profile.html",
        {
            "borrowed_records": borrowed_records,
        },
    )


@login_required
def book_detail(request, book_id):
    if check_role(request) != "user":
        raise PermissionDenied

    book = get_object_or_404(
        Book,
        id=book_id,
    )

    return render(
        request,
        "userpage/book-detail.html",
        {
            "book": book,
        },
    )


@login_required
def borrow_book(request, book_id):
    if check_role(request) != "user":
        raise PermissionDenied

    book = get_object_or_404(
        Book,
        id=book_id,
    )

    if book.available_copies < 1:
        messages.error(
            request,
            f"Sorry, '{book.title}' is currently out of stock.",
        )

        return redirect(
            "book-detail",
            book_id=book.id,
        )

    existing_borrow = BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        status="borrowed",
    ).first()

    if existing_borrow:
        messages.warning(
            request,
            f"You have already borrowed '{book.title}'.",
        )

        return redirect(
            "book-detail",
            book_id=book.id,
        )

    due_date = (
        timezone.now().date()
        + timedelta(days=14)
    )

    BorrowRecord.objects.create(
        user=request.user,
        book=book,
        due_date=due_date,
        status="borrowed",
    )

    book.available_copies -= 1
    book.save()

    messages.success(
        request,
        (
            f"Successfully borrowed '{book.title}'! "
            f"Due date: {due_date}."
        ),
    )

    return redirect(
        "book-detail",
        book_id=book.id,
    )


@login_required
def return_book(request, record_id):
    if check_role(request) != "user":
        raise PermissionDenied

    record = get_object_or_404(
        BorrowRecord,
        id=record_id,
        user=request.user,
    )

    if record.status == "returned":
        messages.error(
            request,
            "This book has already been returned.",
        )

        return redirect("user-profile")

    record.status = "returned"
    record.return_date = timezone.now().date()
    record.save()

    book = record.book

    book.available_copies += 1
    book.save()

    messages.success(
        request,
        f"Successfully returned '{book.title}'. Thank you!",
    )

    return redirect("user-profile")
