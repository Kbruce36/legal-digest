from django.conf import settings


def seo_context(request):  # noqa: ARG001
    """Add SEO-related context variables to all templates."""
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'AI and Human Rights Hub'),
        'SITE_DOMAIN': getattr(settings, 'SITE_DOMAIN', 'localhost:8000'),
        'SITE_PROTOCOL': getattr(settings, 'SITE_PROTOCOL', 'http'),
        'site_name': 'AI and Human Rights Hub',
        'site_description': 'Documenting how artificial intelligence impacts human rights worldwide',
        'site_keywords': 'AI human rights, artificial intelligence, algorithmic bias, surveillance, freedom of expression, child safety, AI ethics',
    }
