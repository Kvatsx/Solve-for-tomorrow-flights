# Methodology used to design the application.

We have followed the [The Twelve Factors](https://12factor.net/) design to make this production based application.

## [I. Codebase](https://12factor.net/codebase)

We have hosted source code (both CLI and API) on Github for version control and different deployments if needed in the future.

## [II. Dependencies](https://12factor.net/dependencies)

We have used **pipfile** to explicitly declare and isolate dependencies.~~~~

## [III. Config](https://12factor.net/config)

We have stored the config file in Environment files (.flaskenv, .env etc).

## [IV. Backing services](https://12factor.net/backing-services)

We have used only single backing service, mongoDB database on cloud. (Both for local and production environment.)

## [V. Build, release, run](https://12factor.net/build-release-run)

We have used Heroku platform which is a Platform as a Service (PaaS). This it helps us to keep the build, release and run seperately.

## [VI. Processes](https://12factor.net/processes)

Processes (Flask and Node server) running are stateless, persistent data is being stored only on mongoDB database (on cloud).

## [VII. Port binding](https://12factor.net/port-binding)

We are providing api endpoints using Flask server.

## [VIII. Concurrency](https://12factor.net/concurrency)

Procfile is being used to run multiple process type. (Currently we have only 1)

## [IX. Disposability](https://12factor.net/disposability)

Heroku is taking care for fast startup and graceful shutdown.

## [X. Dev/prod parity](https://12factor.net/dev-prod-parity)

No disparity between development and production environment - thanks to environment files.

## [XI. Logs](https://12factor.net/logs)

`heroku logs` are only currently being only used to monitor the behavior.

## [XII. Admin processes](https://12factor.net/admin-processes)

This is not available in our application yet.
