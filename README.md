# voteoff-django

# Setup
- Install Python(https://www.python.org/downloads/) Version 3.8.6 is recommended
- Install a virtual environment with `pip install pipenv`. This step is not necessary but is recommended so that dependencies are not installed globally on your system

## Running The VoteOff
- Clone the repository
- Download the local settings file [here](https://www.treysumida.com/media/portfolio/files/local_settings.py) and add it to the `voteoff-django/voteoff-project/voteOff` directory where the settings.py file is also located
- Change directories into the `voteoff-django` directory
- Run `pipenv shell` to start the virtual environment
- Change directories into the `voteoff-project` directory
- Run `pip install -r requirements.txt` to download the dependencies
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`
- Run `python manage.py collectstatic`
- Run `python manage.py runserver`
