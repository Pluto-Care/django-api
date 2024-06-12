# Only to be used in development environment

apps := users users_sessions users_totp logs users_forgot_password users_app_tokens organizations roles \
patients appointments calls

.PHONY: all

venv:
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

resetdb:
	rm -f ./db/db.sqlite3
	rm -f ./db/logs.sqlite3
	find . -type d -name migrations -prune -not -path "./.venv/*" -exec rm -rf {} \;
	.venv/bin/python manage.py makemigrations $(apps)
	.venv/bin/python manage.py migrate
	.venv/bin/python manage.py migrate logs --database=logs_db
	.venv/bin/python manage.py setup_base_roles

resetkeys:
	tar -czf ./keys/backup_$(shell date +%Y%m%d-%H%M.%S).tar.gz ./keys/*
	rm -f ./keys/*.bin
	.venv/bin/python manage.py generate_users_totp_key

superuser:
	.venv/bin/python manage.py createsuperuser

getready: venv resetdb resetkeys

run:
	.venv/bin/python manage.py runserver 0.0.0.0:8000

ngrok:
	ngrok http --domain=decent-annually-roughy.ngrok-free.app http://localhost:8000

su:
	.venv/bin/python manage.py createsuperuser

org:
	.venv/bin/python manage.py add_organization