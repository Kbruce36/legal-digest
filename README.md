# Legal Digest

A professional platform for publishing and reading expert legal case summaries. This site allows a legal professional to share comprehensive case analysis and insights with the public.

## About

Legal Digest is a content publishing platform where a lawyer shares detailed case summaries, legal analysis, and court decision reviews. Visitors can browse, search, and read case summaries across various legal topics and jurisdictions.

## Features

### For Visitors (Public Access)
- **Browse Case Summaries** - Read comprehensive legal case analysis and court decisions
- **Advanced Search** - Find cases by keyword, court, jurisdiction, date range, and legal topics
- **Topic Categories** - Cases organized by tags for easy navigation by legal area
- **Free Access** - All published case summaries are freely available to read

### For Administrator (Lawyer Dashboard)
- **Content Management** - Create, edit, and publish case summaries
- **Rich Case Details** - Include citations, court info, parties, dates, and detailed analysis
- **Draft System** - Prepare content before publishing
- **Tagging & Organization** - Categorize cases for easy discovery
- **Status Tracking** - Manage case publication workflow

## SEO Features

The platform is optimized for search engines to help people discover your legal content:

- **Meta Tags** - Comprehensive meta tags for search engines and social media
- **Open Graph** - Proper OG tags for Facebook, LinkedIn, and other social platforms
- **Twitter Cards** - Twitter-specific meta tags for better social sharing
- **Sitemap** - Automatic XML sitemap generation at `/sitemap.xml`
- **Robots.txt** - Search engine crawler instructions at `/robots.txt`
- **Structured Data** - JSON-LD structured data for rich search results
- **Canonical URLs** - Prevent duplicate content issues
- **Responsive Design** - Mobile-friendly for better SEO rankings

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt` (if available)
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the server: `python manage.py runserver`

## Environment Variables

For production deployment, configure these environment variables:

```bash
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SITE_DOMAIN=yourdomain.com
SITE_PROTOCOL=https
```

## Usage

### For Visitors
1. Visit the homepage at `/` to learn about the site
2. Browse published case summaries (coming soon - public case list)
3. Use search and filters to find specific cases
4. Read detailed case analysis and legal insights

### For Administrator (Lawyer)
1. **Login** - Access the admin dashboard at `/login`
2. **Dashboard** - View your case overview and statistics
3. **Add Cases** - Click "New Case Summary" to create case summaries
4. **Manage Content** - Edit, update, or delete case summaries
5. **Publish** - Change status from "Draft" to "Open" or "Closed" to make cases visible
6. **Organize** - Use tags to categorize cases by legal topic

## Technologies

- Django 6.0
- SQLite (development) / PostgreSQL (production recommended)
- Bootstrap 5
- Python 3.x

## License

See LICENSE file for details.
