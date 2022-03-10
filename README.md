# Digikala CDN Task

This is a simple system to pull incident reports from monitoring systems

### Client APIs

- Login
- Get incident reports and filter

### Admin abilities

- All client abilities
- Create custom report

## Note

- Incident reports are pulled by celery beat and in the multi threading system
- Application is Dockerize and you can use it easily 

## How to start

### Install

pull the git repository

```bash
https://github.com/RasoulRostami/Incident-report.git
cd incident_report
cp incident_report/.env-example incident_report/.env
```

Create custom `.env` file for environment variables. you can copy `env-example` and file you own values

**Note**: Database Information between `docker-compose.yml` (db section)  and `.env` file must have same value
**Recommendation**: You can don't modify the values for develop level

Run docker-compose

```
docker-compose up --build
```

### develop

You can study swagger documents to understand APIs, See request body and response boy
swagger URL: ` localhoust:api-docs/`

### tests

After developing, you can see test coverage with below commands

```
docker exec -it cdn_backend coverage run manage.py test
docker exec -it cdn_backend coverage html
```

After above command HTML repost will be created in `./htmlcov/index.html` and you can analysis tests
If you encounter with permission denied error while opening HTML files, run below command

```
sudo chown -R $USER:$USER .
```

Now tests cover **%96** of project

## Recommendation

Remaining features:

- Create `Dockerfile` and `docker-compose.yml` Product version
- `IncidentReport` have dynamic body
- Use Elastic Search for pulling incident report (less request to `RDBMS` and have more functionality)
- Use `Socket` for serving incident-report inside of `RESTful` 

