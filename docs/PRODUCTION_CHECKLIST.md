# KAVAN v6.0 — Production Deployment Checklist

Verify each of the following items before deploying the application to production.

---

## 1. Automated Checklist

Always run the automated verification script on the target host before starting production services:

```bash
bash backend/deployment/scripts/check_production_ready.sh
```

Ensure the script outputs `PRODUCTION READINESS STATUS: PASSED` with zero critical failures.

---

## 2. Manual Verification List

- [ ] **SSL/TLS Certificates**: Let's Encrypt or private commercial SSL certificates configured inside Nginx `/etc/nginx/ssl/` pointing to port 443.
- [ ] **Secrets & Keys**: Secret Key changed from default settings template, storing high entropy values.
- [ ] **Database Backups**: Cron job established calling `backup_database.sh` daily with backups transferred to offsite secure cold storage (e.g. S3).
- [ ] **Systemd Daemons**: Verify `kavan-api.service`, `kavan-celery.service`, and `kavan-beat.service` are registered and running without crashes.
- [ ] **Monitoring & Alerts**: Check health endpoint `/health/` returns `healthy` status and system indicators are within spec.
- [ ] **Firewall**: Limit database port 5432 and Redis port 6379 to local interface or trusted network interfaces only (never expose database to public internet).
- [ ] **Storage Quotas**: Verify logs directory has rotating configurations and disk space checks are active.
