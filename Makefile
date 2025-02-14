install_deps:
	pip install -r requirements.txt
run:
	python app.py
flask:
	flask --app app run
flask_watch:
	flask --app app.py --debug run
flask_ssl:
	flask --app app run --cert=adhoc
flask_ssl_watch:
	flask --app app --debug run --cert=adhoc