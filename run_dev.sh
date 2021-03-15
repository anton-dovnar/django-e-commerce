#!/usr/bin/env bash
DJANGO_SETTINGS_MODULE=config.settings.dev \
SECRET_KEY='' \
DATABASE_HOST=postgres \
REDIS_HOST=redis \
CACHE_HOST=cache \
docker-compose up
