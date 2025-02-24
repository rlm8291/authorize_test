install_deps:
	pip install -r requirements.txt
run:
	python app.py
flask:
	flask --app app run --port=1313
flask_watch:
	flask --app app.py --debug run --port=1313
flask_ssl:
	flask --app app run --cert=adhoc --port=1313
flask_ssl_watch:
	flask --app app --debug run --cert=adhoc --port=1313