# hangman
Final CodeAcademy task

``` bash
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=yourusername -e POSTGRES_DB=yourdatabasename -p 5432:5432 -d postgres
```
To start app
``` bash
docker-compose up --build --force-recreate --no-deps
```
To stop pres Ctrl+C and comand
``` bash
docker-compose down
```
