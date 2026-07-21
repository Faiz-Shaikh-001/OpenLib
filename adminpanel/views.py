from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from maincontent.models import BorrowRecord, Book
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def admin_page(request):
    is_super = getattr(request.user, 'is_superuser', False)
    user_role = getattr(request.user, 'role', 'admin' if is_super else 'user')
    if user_role != "admin":
        return redirect('user-page')

    context = {
        'total_books': Book.objects.count(),
        'total_users': User.objects.count(),
        'issued_books': BorrowRecord.objects.filter(status='borrowed').count(),
        'overdue_borrows': BorrowRecord.objects.filter(status='overdue').count(),
    }
    return render(request, 'adminpanel/dashboard.html', context)
