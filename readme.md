# TrackIt API
[![CI](https://github.com/ghostfaccee/TrackIt-API/actions/workflows/ci.yml/badge.svg)](https://github.com/ghostfaccee/TrackIt-API/actions/workflows/ci.yml)
[![Docker Image CI](https://github.com/ghostfaccee/TrackIt-API/actions/workflows/docker.yml/badge.svg)](https://github.com/ghostfaccee/TrackIt-API/actions/workflows/docker.yml)

API for tracking habits. Written in FastAPI with asynchronous database operations. REST-like approach.

[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white)](#)
[![Pytest](https://img.shields.io/badge/Pytest-fff?logo=pytest&logoColor=000)](#)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](#)
[![Redis](https://img.shields.io/badge/Redis-%23DD0031.svg?logo=redis&logoColor=white)](#)
[![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white)](#)

## Installation and launch (Ubuntu)
```
git clone https://github.com/ghostfaccee/TrackIt-API.git
cd TrackIt-API
docker compose up --build -d
```

### Applying new migrations
```
docker compose exec api alembic upgrade head
```

### Stop container
```
docker compose down
```

### Change in the project (for developers)
If you decide to add changes to the tables yourself or add new ones, create your own migration using alembic inside the docker container
```
docker compose exec api alembic revision --autogenerate -m "describe your changes"
docker compose exec api alembic upgrade head
```

**You can view the environment variables in the .env.example file.**

**To get logs in file format, use:**
    
    docker compose logs > logs.txt

## License
MIT. You can find it in the root of the project.
