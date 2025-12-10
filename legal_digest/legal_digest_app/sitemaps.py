from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Case


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['legal_digest_app:index', 'legal_digest_app:about', 'legal_digest_app:public_cases_list']

    def location(self, item):
        return reverse(item)


class CaseSitemap(Sitemap):
    """Sitemap for case pages."""
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # Only include non-draft cases in sitemap
        return Case.objects.exclude(status=Case.STATUS_DRAFT)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        # Use public_case_detail for publicly accessible URLs
        return reverse('legal_digest_app:public_case_detail', args=[item.slug])
