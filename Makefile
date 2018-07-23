SCSS = {{ project_name }}/static/scss
STATIC = {{ project_name }}/static

.PHONY: collectstatics compile-scss compile-scss-debug isort isort-check run install test celery

collectstatics: compile-scss
	./manage.py collectstatic --noinput

compile-scss:
	sassc $(SCSS)/main.scss $(STATIC)/css/main.css -s compressed

compile-scss-debug:
	sassc $(SCSS)/main.scss $(STATIC)/css/main.css --sourcemap

watch-scss:
	watchmedo shell-command --patterns=*.scss --recursive --command="make compile-scss-debug" $(SCSS)

flake:
	flake8 . --exclude=*/migrations --max-line-length=80

isort:
	isort */*.py

isort-check:
	isort -c */*.py

run:
	python manage.py runserver 0.0.0.0:8000

install:
	pip install -r requirements/dev.txt

test:
	@coverage run --source=. manage.py test -v2 --settings=wheelapp.settings.test

celery:
	export C_FORCE_ROOT=true && celery -A wheelapp worker -l DEBUG --autoreload

start-services:
	/etc/init.d/postgresql start && \
		/etc/init.d/redis-server start && \
		/etc/init.d/rabbitmq-server start
