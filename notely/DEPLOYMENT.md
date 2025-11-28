# Deployment Guide for Render

This guide will help you deploy the Notely application to Render with PostgreSQL database.

## Why PostgreSQL for Production?

SQLite is not suitable for production on Render because:
- Render's filesystem is ephemeral (gets wiped on each deployment)
- Data stored in SQLite will be lost when the service restarts
- PostgreSQL provides persistent storage and better performance

## Prerequisites

- A Render account (https://render.com)
- Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Step 1: Create a PostgreSQL Database on Render

1. **Log in to Render Dashboard**
   - Go to https://dashboard.render.com

2. **Create New PostgreSQL Database**
   - Click "New +" button
   - Select "PostgreSQL"
   - Fill in the details:
     - **Name**: `notely-db` (or your preferred name)
     - **Database**: `notely` (will be created automatically)
     - **User**: `notely` (will be created automatically)
     - **Region**: Choose the same region as your web service
     - **Plan**: Free (for testing) or paid plan
   - Click "Create Database"

3. **Copy the Internal Database URL**
   - Once created, go to your database dashboard
   - Find "Internal Database URL" (starts with `postgres://`)
   - Copy this URL - you'll need it in Step 2

## Step 2: Create a Web Service on Render

1. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your Git repository

2. **Configure the Web Service**
   - **Name**: `notely` (or your preferred name)
   - **Region**: Same as your database
   - **Branch**: `main` (or your default branch)
   - **Build Command**: Leave as default or use:
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```
     gunicorn notely.wsgi:application
     ```

3. **Add Environment Variables**
   Click "Advanced" and add these environment variables:

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | Paste the Internal Database URL from Step 1 |
   | `SECRET_KEY` | Generate a secure random key (use https://djecrety.ir/) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | Your Render URL (e.g., `your-app.onrender.com`) |

4. **Create the Web Service**
   - Click "Create Web Service"
   - Render will start building and deploying your app

## Step 3: Run Database Migrations

After your web service is deployed:

1. **Go to your Web Service dashboard**
2. **Click on "Shell" tab**
3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

## Step 4: Verify Deployment

1. Visit your application URL: `https://your-app.onrender.com`
2. Try creating a note
3. Restart your web service from the dashboard
4. Verify that your notes are still there (they should persist!)

## Environment Variables Reference

### Required Variables

- **DATABASE_URL**: PostgreSQL connection string from Render database
  - Format: `postgres://user:password@host:port/database`
  - Provided automatically by Render when you create a database

- **SECRET_KEY**: Django secret key for cryptographic signing
  - Generate a secure key: https://djecrety.ir/
  - Never commit this to version control

- **DEBUG**: Set to `False` in production
  - Default: `True` (development mode)

- **ALLOWED_HOSTS**: Comma-separated list of allowed domains
  - Example: `your-app.onrender.com,www.your-domain.com`
  - Default includes: `localhost,127.0.0.1,note-ai-nmdr.onrender.com`

### Optional Variables

- **CSRF_TRUSTED_ORIGINS**: If you have custom domains
  - Already configured in settings.py for Render

## Troubleshooting

### Issue: "Invalid HTTP_HOST header"
**Solution**: Add your domain to `ALLOWED_HOSTS` environment variable

### Issue: "CSRF verification failed"
**Solution**: Ensure your domain is in `CSRF_TRUSTED_ORIGINS` in settings.py

### Issue: "Database connection error"
**Solution**:
- Verify `DATABASE_URL` environment variable is set correctly
- Ensure your database and web service are in the same region
- Use "Internal Database URL" not "External Database URL"

### Issue: "Notes disappear after deployment"
**Solution**: You're likely still using SQLite. Verify:
- PostgreSQL database is created
- `DATABASE_URL` environment variable is set
- Run migrations after setting up PostgreSQL

### Issue: "Static files not loading"
**Solution**:
- Run `python manage.py collectstatic` in build script
- WhiteNoise is already configured in settings.py

## Build Script (build.sh)

Your current build script should contain:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic --no-input
```

## Local Development vs Production

The application automatically detects the environment:

- **Local Development**: Uses SQLite (no DATABASE_URL environment variable)
- **Production**: Uses PostgreSQL (DATABASE_URL is set by Render)

You can develop locally with SQLite and deploy to production with PostgreSQL without changing any code!

## Cost Considerations

### Free Tier
- PostgreSQL: 1GB storage, 97 hours/month uptime
- Web Service: 750 hours/month
- Both services spin down after 15 minutes of inactivity

### Paid Plans
- PostgreSQL: Starting at $7/month (always on, more storage)
- Web Service: Starting at $7/month (always on, better performance)

## Security Best Practices

1. **Never commit secrets to Git**
   - Use environment variables for sensitive data
   - Add `.env` files to `.gitignore`

2. **Use strong SECRET_KEY**
   - Generate a unique key for production
   - Keep it different from development

3. **Set DEBUG=False in production**
   - Prevents sensitive information leakage
   - Better error handling

4. **Keep dependencies updated**
   - Regularly update requirements.txt
   - Monitor for security vulnerabilities

## Backup Your Database

Render provides automatic daily backups for paid PostgreSQL plans. For free tier:

1. Use Render's manual backup feature
2. Or export data periodically:
   ```bash
   python manage.py dumpdata > backup.json
   ```

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL on Render](https://render.com/docs/databases)

## Support

For issues specific to:
- **Notely Application**: Open an issue in the repository
- **Render Platform**: Contact Render support or check their docs
