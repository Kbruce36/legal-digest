# Generated migration for AI and Human Rights Hub tags

from django.db import migrations


def create_initial_tags(apps, schema_editor):
    """Create initial AI and human rights tags."""
    Tag = apps.get_model('legal_digest_app', 'Tag')
    
    tags = [
        'AI Surveillance',
        'Algorithmic Bias',
        'Freedom of Expression',
        'Child Safety',
        'AI in Public Services',
        'Privacy Rights',
        'Facial Recognition',
        'Predictive Policing',
        'Content Moderation',
        'Automated Decision-Making',
        'Data Protection',
        'Discrimination',
        'Healthcare AI',
        'Employment AI',
        'Education AI',
        'Criminal Justice',
        'Social Media',
        'Transparency',
        'Accountability',
        'AI Governance',
    ]
    
    for tag_name in tags:
        # Use get_or_create with slug to handle duplicates properly
        from django.utils.text import slugify
        slug = slugify(tag_name)
        Tag.objects.get_or_create(slug=slug, defaults={'name': tag_name})


def reverse_tags(apps, schema_editor):
    """Remove initial tags if migration is reversed."""
    Tag = apps.get_model('legal_digest_app', 'Tag')
    
    tags = [
        'AI Surveillance',
        'Algorithmic Bias',
        'Freedom of Expression',
        'Child Safety',
        'AI in Public Services',
        'Privacy Rights',
        'Facial Recognition',
        'Predictive Policing',
        'Content Moderation',
        'Automated Decision-Making',
        'Data Protection',
        'Discrimination',
        'Healthcare AI',
        'Employment AI',
        'Education AI',
        'Criminal Justice',
        'Social Media',
        'Transparency',
        'Accountability',
        'AI Governance',
    ]
    
    Tag.objects.filter(name__in=tags).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('legal_digest_app', '0002_tag_case_tags'),
    ]

    operations = [
        migrations.RunPython(create_initial_tags, reverse_tags),
    ]
