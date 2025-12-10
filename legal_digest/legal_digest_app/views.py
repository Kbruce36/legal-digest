from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CaseFilterForm, CaseForm
from .models import Case, Tag


def index(request):
    # Get count of published cases for homepage
    published_count = Case.objects.exclude(status=Case.STATUS_DRAFT).count()
    recent_cases = Case.objects.exclude(status=Case.STATUS_DRAFT).order_by('-created_at')[:3]
    
    context = {
        'published_count': published_count,
        'recent_cases': recent_cases,
    }
    return render(request, 'index.html', context)


def about(request):
    """About page describing the AI and Human Rights Hub mission."""
    published_count = Case.objects.exclude(status=Case.STATUS_DRAFT).count()
    context = {
        'published_count': published_count,
    }
    return render(request, 'about.html', context)


def public_cases_list(request):
    """Public page showing all published case summaries."""
    # Only show non-draft cases to the public
    cases = Case.objects.exclude(status=Case.STATUS_DRAFT).order_by('-decision_date', '-created_at')
    
    # Apply search/filter if provided
    search = request.GET.get('search', '')
    court = request.GET.get('court', '')
    tag_id = request.GET.get('tag', '')
    
    if search:
        cases = cases.filter(
            Q(title__icontains=search) |
            Q(citation__icontains=search) |
            Q(court__icontains=search) |
            Q(parties__icontains=search)
        )
    
    if court:
        cases = cases.filter(court__icontains=court)
    
    if tag_id:
        cases = cases.filter(tags__id=tag_id)
    
    # Pagination
    paginator = Paginator(cases, 12)  # 12 cases per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all tags and courts for filters
    all_tags = Tag.objects.all()
    all_courts = Case.objects.exclude(court='').exclude(status=Case.STATUS_DRAFT).values_list('court', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'all_tags': all_tags,
        'all_courts': all_courts,
        'search': search,
        'selected_court': court,
        'selected_tag': tag_id,
    }
    return render(request, 'public_cases_list.html', context)


def public_case_detail(request, slug):
    """Public page showing a single case summary."""
    # Only allow viewing non-draft cases
    case = get_object_or_404(Case.objects.exclude(status=Case.STATUS_DRAFT), slug=slug)
    
    # Get related cases (same tags)
    related_cases = Case.objects.exclude(status=Case.STATUS_DRAFT).exclude(id=case.id).filter(
        tags__in=case.tags.all()
    ).distinct()[:3]
    
    context = {
        'case': case,
        'related_cases': related_cases,
    }
    return render(request, 'public_case_detail.html', context)


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
                Q(parties__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()
        
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


@login_required
def tag_list(request):
    """List all tags with case counts."""
    tags = Tag.objects.all().order_by('name')
    tag_stats = []
    for tag in tags:
        tag_stats.append({
            'tag': tag,
            'case_count': tag.cases.count(),
            'published_count': tag.cases.exclude(status=Case.STATUS_DRAFT).count()
        })
    
    context = {
        'tag_stats': tag_stats,
    }
    return render(request, 'tag_list.html', context)


@login_required
def tag_create(request):
    """Create a new tag."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            if Tag.objects.filter(name__iexact=name).exists():
                messages.error(request, f'Tag "{name}" already exists.')
            else:
                Tag.objects.create(name=name)
                messages.success(request, f'Tag "{name}" created successfully.')
                return redirect('legal_digest_app:tag_list')
        else:
            messages.error(request, 'Tag name cannot be empty.')
    
    return render(request, 'tag_form.html')


@login_required
def tag_edit(request, slug):
    """Edit an existing tag."""
    tag = get_object_or_404(Tag, slug=slug)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            if Tag.objects.filter(name__iexact=name).exclude(id=tag.id).exists():
                messages.error(request, f'Tag "{name}" already exists.')
            else:
                tag.name = name
                tag.slug = ''  # Reset slug to regenerate from new name
                tag.save()
                messages.success(request, 'Tag updated successfully.')
                return redirect('legal_digest_app:tag_list')
        else:
            messages.error(request, 'Tag name cannot be empty.')
    
    context = {'tag': tag}
    return render(request, 'tag_form.html', context)


@login_required
def tag_delete(request, slug):
    """Delete a tag."""
    tag = get_object_or_404(Tag, slug=slug)
    
    if request.method == 'POST':
        tag_name = tag.name
        tag.delete()
        messages.success(request, f'Tag "{tag_name}" deleted successfully.')
        return redirect('legal_digest_app:tag_list')
    
    context = {
        'tag': tag,
        'case_count': tag.cases.count()
    }
    return render(request, 'tag_confirm_delete.html', context)
