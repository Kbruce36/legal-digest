from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CaseFilterForm, CaseForm
from .models import Case, Tag


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    # Start with all cases
    cases = Case.objects.all()
    
    # Apply filters if provided
    filter_form = CaseFilterForm(request.GET or None)
    
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        if search:
            cases = cases.filter(
                Q(title__icontains=search) |
                Q(citation__icontains=search) |
                Q(docket_number__icontains=search) |
                Q(parties__icontains=search)
            )
        
        court = filter_form.cleaned_data.get('court')
        if court:
            cases = cases.filter(court__icontains=court)
        
        status = filter_form.cleaned_data.get('status')
        if status:
            cases = cases.filter(status=status)
        
        date_from = filter_form.cleaned_data.get('date_from')
        if date_from:
            cases = cases.filter(decision_date__gte=date_from)
        
        date_to = filter_form.cleaned_data.get('date_to')
        if date_to:
            cases = cases.filter(decision_date__lte=date_to)
        
        tag = filter_form.cleaned_data.get('tag')
        if tag:
            cases = cases.filter(tags=tag)
    
    # Calculate stats
    stats = {
        "open": cases.filter(status=Case.STATUS_OPEN).count(),
        "closed": cases.filter(status=Case.STATUS_CLOSED).count(),
        "draft": cases.filter(status=Case.STATUS_DRAFT).count(),
        "tags": Tag.objects.count(),
    }
    
    recent_cases = cases.order_by("-decision_date", "-created_at")[:6]
    activity_items = cases.order_by("-updated_at")[:6]
    
    # Get all unique courts for filter dropdown
    all_courts = Case.objects.exclude(court='').values_list('court', flat=True).distinct()

    context = {
        "stats": stats,
        "recent_cases": recent_cases,
        "activity_items": activity_items,
        "filter_form": filter_form,
        "all_courts": all_courts,
    }
    return render(request, 'dashboard.html', context)


@login_required
def case_create(request):
    """Create a new case."""
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save()
            messages.success(request, f'Case "{case.title}" created successfully!')
            return redirect('legal_digest_app:case_detail', slug=case.slug)
    else:
        form = CaseForm()
    
    return render(request, 'case_form.html', {
        'form': form,
        'title': 'Create New Case',
        'button_text': 'Create Case'
    })


@login_required
def case_detail(request, slug):
    """Display case details."""
    case = get_object_or_404(Case, slug=slug)
    return render(request, 'case_detail.html', {'case': case})


@login_required
def case_edit(request, slug):
    """Edit an existing case."""
    case = get_object_or_404(Case, slug=slug)
    
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            case = form.save()
            messages.success(request, f'Case "{case.title}" updated successfully!')
            return redirect('legal_digest_app:case_detail', slug=case.slug)
    else:
        form = CaseForm(instance=case)
    
    return render(request, 'case_form.html', {
        'form': form,
        'case': case,
        'title': f'Edit Case: {case.title}',
        'button_text': 'Update Case'
    })


@login_required
def case_delete(request, slug):
    """Delete a case."""
    case = get_object_or_404(Case, slug=slug)
    
    if request.method == 'POST':
        title = case.title
        case.delete()
        messages.success(request, f'Case "{title}" deleted successfully!')
        return redirect('legal_digest_app:dashboard')
    
    return render(request, 'case_confirm_delete.html', {'case': case})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
