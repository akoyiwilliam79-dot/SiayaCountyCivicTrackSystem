# Deployment Guide

This document explains how to deploy the Civic System Django project to a production environment.

---

## 1. Prepare the Project

Before deploying:

- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Ensure all migrations are applied

```bash id="dep4"
python manage.py makemigrations
python manage.py migrate