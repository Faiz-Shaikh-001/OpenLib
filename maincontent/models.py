from django.conf import settings
from django.db import models
from django.db.models import Q


class EmailSubscription(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=200,
    )

    author = models.CharField(
        max_length=150,
    )

    isbn = models.CharField(
        max_length=13,
        unique=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    total_copies = models.PositiveIntegerField(
        default=1,
    )

    available_copies = models.PositiveIntegerField(
        default=1,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.title} by {self.author}"


class BorrowRecord(models.Model):
    STATUS_CHOICES = (
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrow_records",
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrow_records",
    )

    borrow_date = models.DateField(
        auto_now_add=True,
    )

    due_date = models.DateField()

    return_date = models.DateField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="borrowed",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                condition=Q(status="borrowed"),
                name="unique_active_borrow_per_user_book",
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.book.title} ({self.status})"
        )
