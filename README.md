# Wishlist API

REST API to manage customers and their wishlists.

## Technologies

- Python 3.8
- Flask (webserver)
- Flask ApiSpec (provides API documentation with OpenAPI and Swagger)
- Flask-JWT-Extended (handles authentication with JWT)
- alembic (handles database migrations)

## Installation
Pre-requisites: Docker, docker-compose and make.


```bash
git clone git@github.com:csmaniottojr/wishlist_api.git
cd wishlist_api/
cp .env.example .env # set value for blank enviroment variables
make build
```

## Usage

```bash
make up
```

- Access the live documentation: http://localhost:5000/swagger-ui
- Create an user account with endpoint `/auth/signup`
- Login to get an access token with endpoint `/auth/login`
- Click on the button "Authorize" and type "Bearer <YOUR_TOKEN>"
- All right, now you're authenticated and can access the others endpoints.

## Tests
```bash
make test
```


## License
[MIT](LICENSE)