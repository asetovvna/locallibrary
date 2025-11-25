from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime

from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm


# --- Функция обновления срока возврата ---
@permission_required("catalog.can_mark_returned")
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data["renewal_date"]
            book_inst.save()
            return HttpResponseRedirect(reverse("all-borrowed"))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    return render(
        request,
        "catalog/book_renew_librarian.html",
        {"form": form, "bookinst": book_inst},
    )


# locallibrary/catalog/views.py (в самый конец)

from django.contrib.auth.mixins import PermissionRequiredMixin


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = "__all__"
    permission_required = "catalog.can_mark_returned"  # или создайте новое разрешение
    # login_url = '/login/'   # если нужно переопределить


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    permission_required = "catalog.can_mark_returned"


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("authors")
    permission_required = "catalog.can_mark_returned"


# --- Остальные CBVs ---
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    ordering = ["last_name"]  # чтобы убрать предупреждение


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = "catalog.can_mark_returned"
    template_name = "catalog/bookinstance_list_borrowed_all.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")


# --- Простые функции ---
def index(request):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": Book.objects.count(),
        "num_instances": BookInstance.objects.count(),
        "num_instances_available": BookInstance.objects.filter(
            status__exact="a"
        ).count(),
        "num_authors": Author.objects.count(),
        "num_visits": request.session["num_visits"],
    }
    return render(
        request, "index.html", context
    )  # ← скорее всего, шаблон "index.html", а не "base_generic.html"
