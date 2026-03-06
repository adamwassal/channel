#!/usr/bin/env bash
set -e

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
  python3 manage.py createsuperuser --noinput || true
fi

exec gunicorn coding_with_adam.wsgi:application --bind 0.0.0.0:${PORT:-8000}
