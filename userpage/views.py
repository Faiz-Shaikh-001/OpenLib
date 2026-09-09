from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from maincontent.models import Book, BorrowRecord


def check_role(request):
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

    books = Book.objects.select_related(
        "category"
    ).all()

    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(isbn__icontains=query)
            | Q(category__name__icontains=query)
        )

    books = books.order_by(
        "title",
    )

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

    borrowed_records = (
        BorrowRecord.objects
        .filter(user=request.user)
        .select_related("book")
        .order_by("-borrow_date")
    )

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
        Book.objects.select_related("category"),
        id=book_id,
    )

    active_borrow = BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        status="borrowed",
    ).first()

    return render(
        request,
        "userpage/book-detail.html",
        {
            "book": book,
            "active_borrow": active_borrow,
        },
    )


@login_required
@require_POST
def borrow_book(request, book_id):
    if check_role(request) != "user":
        raise PermissionDenied

    try:
        with transaction.atomic():
            existing_borrow = BorrowRecord.objects.filter(
                user=request.user,
                book_id=book_id,
                status="borrowed",
            ).exists()

            if existing_borrow:
                messages.warning(
                    request,
                    "You have already borrowed this book.",
                )

                return redirect(
                    "book-detail",
                    book_id=book_id,
                )

            # Conditional UPDATE prevents stock from dropping below zero.
            updated_rows = Book.objects.filter(
                id=book_id,
                available_copies__gt=0,
            ).update(
                available_copies=F("available_copies") - 1
            )

            if updated_rows == 0:
                if not Book.objects.filter(id=book_id).exists():
                    messages.error(
                        request,
                        "The requested book does not exist.",
                    )

                    return redirect("user-page")

                messages.error(
                    request,
                    "This book is currently unavailable.",
                )

                return redirect(
                    "book-detail",
                    book_id=book_id,
                )

            due_date = (
                timezone.now().date()
                + timedelta(days=14)
            )

            BorrowRecord.objects.create(
                user=request.user,
                book_id=book_id,
                due_date=due_date,
                status="borrowed",
            )

    except IntegrityError:
        # Protects against simultaneous duplicate borrow attempts.
        messages.warning(
            request,
            "You already have an active borrow for this book.",
        )

        return redirect(
            "book-detail",
            book_id=book_id,
        )

    book = Book.objects.get(
        id=book_id,
    )

    messages.success(
        request,
        (
            f"Successfully borrowed '{book.title}'. "
            f"Due date: {due_date}."
        ),
    )

    return redirect(
        "book-detail",
        book_id=book_id,
    )


@login_required
@require_POST
def return_book(request, record_id):
    if check_role(request) != "user":
        raise PermissionDenied

    with transaction.atomic():
        record = get_object_or_404(
            BorrowRecord.objects.select_for_update(),
            id=record_id,
            user=request.user,
        )

        if record.status == "returned":
            messages.warning(
                request,
                "This book has already been returned.",
            )

            return redirect(
                "user-profile",
            )

        record.status = "returned"
        record.return_date = timezone.now().date()

        record.save(
            update_fields=[
                "status",
                "return_date",
            ]
        )

        Book.objects.filter(
            id=record.book_id,
        ).update(
            available_copies=F("available_copies") + 1
        )

        book_title = record.book.title

    messages.success(
        request,
        f"Successfully returned '{book_title}'.",
    )

    return redirect(
        "user-profile",
    )
