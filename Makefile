shell:
	python manage.py shell

run:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate: migrations
	python manage.py migrate

su:
	python manage.py createsuperuser

.PHONY: shell