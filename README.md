# Sports League
Below link contains details about how to create a django postgres project using Docker
https://docs.docker.com/samples/django/

# How to run
docker-compose up

# How to access Graphql API
Locally connect to http://0.0.0.0:8000/graphql/

# How to access postgres
docker-compose exec db psql -U postgres

# How to stop
docker-compose down

# How to create new app
sudo docker-compose run web django-admin startapp tennis
