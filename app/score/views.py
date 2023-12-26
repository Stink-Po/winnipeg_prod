from django.shortcuts import render, redirect, get_object_or_404
from .models import DiscountCode, generate_discount_code
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .forms import SearchForm
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
def create_new_code(request):
    user = CustomUser.objects.filter(pk=request.user.id).first()
    code = generate_discount_code()
    new_discount_code = DiscountCode.objects.create(code=code, user=user)
    new_discount_code.save()
    user.discount_codes.add(new_discount_code)
    user.score -= 100
    user.save()
    return redirect("accounts:dashboard")


@login_required
def user_discount_code(request):
    form = SearchForm()
    all_user_codes = DiscountCode.objects.filter(user=request.user).all()
    return render(request, "score/user_discount_codes.html", {
        "discount_codes": all_user_codes,
        "search_form": form,
    })


@user_passes_test(is_admin)
def search_discount_code(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            code = DiscountCode.objects.filter(code=query).first()
            if code:
                return render(request, "score/search_code_results.html", {"code": code})

    return render(request, "score/search_code_results.html", {"code": None})


@user_passes_test(is_admin)
def flag_code_to_used(request, code_id):
    current_code = get_object_or_404(DiscountCode, pk=code_id)
    if current_code:
        current_code.used = True
        current_code.save()

    return redirect("accounts:dashboard")


def how_score_work(request):
    return render(request, "score/how_score_works.html")
