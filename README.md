# AItiv8 - Challenge 2 - SmartCities
## Agricultural Planning

RUN (Estamos a usar Python 3.10)

python -m venv venv                 (or python3.10 -m venv venv if more than one distribution of python)
. venv/Scrypts/activate             (or . venv/bin/activate on Linux)
pip install -r requirements
python manage.py makemigrations
python manage.py migrate
./manage.py runserver

ENDPOINTS

http://127.0.0.1:8000/crop_type
http://127.0.0.1:8000/optimized_planning