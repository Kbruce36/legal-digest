from django import forms
from .models import Case, Tag


class CaseForm(forms.ModelForm):
    """Form for creating and editing cases."""
    
    class Meta:
        model = Case
        fields = [
            'title', 'citation', 'court', 'jurisdiction', 'docket_number',
            'decision_date', 'parties', 'status', 'summary_short', 
            'summary_long', 'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter case title',
                'required': True
            }),
            'citation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 123 F.3d 456'
            }),
            'court': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Supreme Court'
            }),
            'jurisdiction': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Federal, State'
            }),
            'docket_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2024-CV-12345'
            }),
            'decision_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'parties': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of parties involved'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'summary_short': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Concise summary (1-2 sentences)'
            }),
            'summary_long': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Full case summary'
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'summary_short': 'Short Summary',
            'summary_long': 'Full Summary',
        }


class CaseFilterForm(forms.Form):
    """Form for filtering cases on dashboard."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search case titles or citations',
            'id': 'searchInput'
        })
    )
    
    court = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Court name',
            'id': 'courtSelect'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + Case.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'statusSelect'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'dateFrom'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'dateTo'
        })
    )
    
    tag = forms.ModelChoiceField(
        required=False,
        queryset=Tag.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        empty_label='All Tags'
    )
