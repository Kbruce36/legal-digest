# Deploying Legal Digest to Render

This guide will walk you through deploying your Legal Digest application to Render.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com - it's free)
3. Your code committed to a GitHub repository

## Step 1: Prepare Your GitHub Repository

### 1.1 Initialize Git (if not already done)
```bash
cd legal_digest
git init
```

### 1.2 Add all files to Git
```bash
git add .
```

### 1.3 Commit your changes
```bash
git commit -m "Initial commit - Ready for deployment"
```

### 1.4 Create a new repository on GitHub
1. Go to https://github.com
2. Click the "+" icon in the top right
3. Click "New repository"
4. Name it: `legal-digest`
5. Keep it Public or Private (your choice)
6. Don't initialize with README (you already have one)
7. Click "Create repository"

### 1.5 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/legal-digest.git
git branch -M main
git push -u origin main
```

## Step 2: Create a Render Account

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email
4. Verify your email if required

## Step 3: Create a PostgreSQL Database on Render

1. From your Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Configure the database:
   - **Name**: `legal-digest-db`
   - **Database**: `legal_digest_db` (auto-generated)
   - **User**: `legal_digest_user` (auto-generated)
   - **Region**: Choose closest to your users
   - **Plan**: Free (for MVP)
4. Click "Create Database"
5. **IMPORTANT**: Copy the "Internal Database URL" - you'll need this!
   - It looks like: `postgresql://user:password@host/database`

## Step 4: Create a Web Service on Render

### 4.1 Create New Web Service
1. From Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository:
   - Click "Connect account" if needed
   - Find and select your `legal-digest` repository
   - Click "Connect"

### 4.2 Configure the Web Service
Fill in the following settings:

**Basic Settings:**
- **Name**: `legal-digest`
- **Region**: Same as your database
- **Branch**: `main` (or `development` if you want)
- **Root Directory**: `legal_digest` (the inner folder with manage.py)
- **Runtime**: Python 3
- **Build Command**: `chmod +x build.sh && ./build.sh`
- **Start Command**: `gunicorn legal_digest.wsgi:application`

**Plan:**
- Select "Free" (for MVP testing)

### 4.3 Add Environment Variables
Click "Advanced" then add these environment variables:

```
DJANGO_SECRET_KEY=your-random-secret-key-here-make-it-long-and-random
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app-name.onrender.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
DATABASE_URL=paste-the-internal-database-url-from-step-3
SITE_DOMAIN=your-app-name.onrender.com
SITE_PROTOCOL=https
PYTHON_VERSION=3.11.0
```

**Important Notes:**
- Replace `your-app-name` with your actual Render app name
- Replace `your-random-secret-key-here-make-it-long-and-random` with a long random string
  - You can generate one at https://djecrety.ir/
- Use the DATABASE_URL you copied in Step 3

### 4.4 Deploy
1. Click "Create Web Service"
2. Render will start building and deploying your app
3. This will take 5-10 minutes for the first deployment
4. Watch the logs for any errors

## Step 5: Create Superuser (Admin Account)

Once deployment is successful:

### 5.1 Access Render Shell
1. Go to your web service dashboard on Render
2. Click the "Shell" tab on the left
3. This opens a terminal connected to your live server

### 5.2 Create Superuser
In the Render shell, run:
```bash
cd legal_digest
python manage.py createsuperuser
```

Follow the prompts:
- Username: (choose your username)
- Email: (your email)
- Password: (choose a strong password)
- Password (again): (confirm password)

## Step 6: Access Your Live Site

Your site should now be live at:
- **Public site**: `https://your-app-name.onrender.com/`
- **Admin panel**: `https://your-app-name.onrender.com/admin/`

### First Steps:
1. Visit the admin panel
2. Login with your superuser credentials
3. Start adding case summaries!

## Step 7: Test Your Deployment

1. **Homepage**: Visit your site URL - should show the new homepage
2. **Login**: Go to `/login` and test login
3. **Dashboard**: After login, check the dashboard
4. **Add Case**: Try creating a test case summary
5. **Sitemap**: Visit `/sitemap.xml` - should work
6. **Robots**: Visit `/robots.txt` - should work

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Verify `build.sh` has correct permissions

### Database Connection Errors
- Double-check DATABASE_URL environment variable
- Ensure database is in same region as web service
- Verify database is running (green status in Render)

### Static Files Not Loading
- Check that STATIC_ROOT is set correctly
- Verify WhiteNoise is in MIDDLEWARE
- Run `python manage.py collectstatic` in shell if needed

### 500 Server Errors
- Set `DJANGO_DEBUG=True` temporarily to see error details
- Check Render logs (Logs tab)
- Verify all environment variables are set
- **Remember to set DEBUG=False after fixing!**

## Updating Your Site

Whenever you make changes:

1. Commit changes to Git:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

2. Render will automatically detect the push and redeploy
3. Wait for the build to complete (~2-5 minutes)

## Free Tier Limitations

Render's free tier has these limits:
- Database: 1GB storage, shared CPU
- Web Service: Spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month of runtime

For production with consistent traffic, upgrade to paid tier ($7/month for web service).

## Next Steps After Deployment

1. **Add Content**: Log in and create case summaries
2. **Custom Domain**: (Optional) Add your own domain in Render settings
3. **Monitor**: Check Render dashboard for performance and errors
4. **Backup**: Render backups your database, but export important data regularly
5. **SEO**: Submit your sitemap to Google Search Console
6. **Share**: Your lawyer can now start publishing case summaries!

## Support

If you encounter issues:
- Check Render's documentation: https://render.com/docs
- Review deployment logs in Render dashboard
- Check Django logs in Render Shell: `tail -f /var/log/render.log`

## Security Checklist

- ✅ DEBUG set to False
- ✅ SECRET_KEY is random and secret
- ✅ ALLOWED_HOSTS configured
- ✅ CSRF_TRUSTED_ORIGINS configured
- ✅ HTTPS enabled (automatic on Render)
- ✅ Security headers enabled
- ✅ Strong password for admin account

---

**Congratulations! Your Legal Digest platform is now live! 🎉**
