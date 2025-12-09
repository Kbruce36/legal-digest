from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Case, Tag


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    cases = Case.objects.all()
    stats = {
        "open": cases.filter(status=Case.STATUS_OPEN).count(),
        "closed": cases.filter(status=Case.STATUS_CLOSED).count(),
        "draft": cases.filter(status=Case.STATUS_DRAFT).count(),
        "tags": Tag.objects.count(),
    }
    recent_cases = cases.order_by("-decision_date", "-created_at")[:6]
    activity_items = cases.order_by("-updated_at")[:6]

    context = {
        "stats": stats,
        "recent_cases": recent_cases,
        "activity_items": activity_items,
    }
    return render(request, 'dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
