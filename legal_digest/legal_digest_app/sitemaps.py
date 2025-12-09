from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Case


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['legal_digest_app:index']

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

    def location(self, item):  # Changed back to 'item' for consistency
        return reverse('legal_digest_app:case_detail', args=[item.slug])
