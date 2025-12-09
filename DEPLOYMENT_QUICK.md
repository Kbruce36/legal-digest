# Quick Deployment Checklist

## Before You Start
- [ ] Code is working locally
- [ ] GitHub account created
- [ ] Render account created (https://render.com)

## Step 1: Push to GitHub (5 minutes)
```bash
cd legal_digest
git init
git add .
git commit -m "Ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/legal-digest.git
git push -u origin main
```

## Step 2: Render - Create Database (2 minutes)
1. Render Dashboard → New + → PostgreSQL
2. Name: `legal-digest-db`
3. Plan: Free
4. Create Database
5. **COPY the Internal Database URL!**

## Step 3: Render - Create Web Service (5 minutes)
1. Render Dashboard → New + → Web Service
2. Connect GitHub repository: `legal-digest`
3. Settings:
   - Name: `legal-digest`
   - Root Directory: `legal_digest`
   - Build Command: `chmod +x build.sh && ./build.sh`
   - Start Command: `gunicorn legal_digest.wsgi:application`
   - Plan: Free

## Step 4: Add Environment Variables
```
DJANGO_SECRET_KEY=generate-at-djecrety.ir
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app.onrender.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
DATABASE_URL=paste-from-step-2
SITE_DOMAIN=your-app.onrender.com
SITE_PROTOCOL=https
PYTHON_VERSION=3.11.0
```

## Step 5: Deploy & Wait (10 minutes)
- Click "Create Web Service"
- Wait for build to complete
- Check for errors in logs

## Step 6: Create Admin User (2 minutes)
1. Go to your service → Shell tab
2. Run:
```bash
cd legal_digest
python manage.py createsuperuser
```

## Done! 🎉
- Visit: `https://your-app.onrender.com`
- Admin: `https://your-app.onrender.com/admin`

## Need Help?
See DEPLOYMENT.md for detailed instructions!
