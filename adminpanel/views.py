from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from maincontent.models import Book, BorrowRecord


User = get_user_model()


def is_admin(user):
    return user.is_superuser or getattr(user, "role", "user") == "admin"


@login_required
def admin_page(request):
    if not is_admin(request.user):
        raise PermissionDenied(
            "You do not have permission to access the admin dashboard."
        )

    context = {
        "total_books": Book.objects.count(),
        "total_users": User.objects.count(),
        "issued_books": BorrowRecord.objects.filter(
            status="borrowed"
        ).count(),
        "overdue_borrows": BorrowRecord.objects.filter(
            status="overdue"
        ).count(),
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context,
    )
