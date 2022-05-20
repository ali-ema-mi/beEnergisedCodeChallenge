# beEnergised

beEnergised Pricing System (A sub-system of CSMS)

1- Prepare server: (Ubuntu 18.04 and up)

    sudo apt update
    sudo apt upgrade

2- Install docker:

    sudo apt install docker.io

3- Install docker compose:

    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

4- Define bellow environment variables in .env file:

    # Django
    GUNICORN_PORT=8000
    ALLOWED_HOSTS=*
    DEBUG=0
    SECRET_KEY=django-insecure-l8(o4x($x=t=%nr(^%lb9j169^v(ol@=m@!s72c1g&u-$$zy4p
    ROOT_PASSWORD=123
    SERVICE_PORT=8000

5- Start containers:

    docker-compose up -d

6- If prefer some initial dummy data, run:

    docker-compose exec web python manage.py init

or 

    docker exec be_energised python manage.py init


7- Navigate to control panel through:

    http://[server ip]:8000/

Note: service port can be changed via SERVICE_PORT in .env. (restarting container needed)

8- For running test:

    docker-compose exec web python manage.py test

or 

    docker exec be_energised python manage.py test

9- For API documentation and testing tools, navigate to:

    http://[server ip]:8000/api/

10- Sample command line example for testing API:

    curl -X POST -H "Content-Type: application/json" -d "{\"rate\": {\"energy\": 0.3, \"time\": 2, \"transaction\": 1}, \"cdr\": {\"meterStart\": 1204307, \"timestampStart\": \"2021-04-05T10:04:00Z\", \"meterStop\": 1215230, \"timestampStop\": \"2021-04-05T11:27:00Z\"}}" http://[server ip]:8000/api/invoice/ 

Returned response:

    {"overall":7.04,"components":{"energy":3.277,"time":2.767,"transaction":1.0}}