#!/bin/bash

function django_secret() { python -c "from secrets import token_urlsafe;print(f'SECRET_KEY={token_urlsafe(64)}')"; }
echo "DEBUG=True" > .env
django_secret >> .env
