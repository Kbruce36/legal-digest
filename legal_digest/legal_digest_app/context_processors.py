from django.conf import settings


def seo_context(request):  # noqa: ARG001
    """Add SEO-related context variables to all templates."""
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Legal Digest'),
        'SITE_DOMAIN': getattr(settings, 'SITE_DOMAIN', 'localhost:8000'),
        'SITE_PROTOCOL': getattr(settings, 'SITE_PROTOCOL', 'http'),
    }
