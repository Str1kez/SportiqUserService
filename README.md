# User Microservice for Sportiq Project

This microservice is responsible for registering and authenticating users, as well as for working on JWT. DB for Blacklist and KDS is defined here.

![Microservice Architecture](assets/diagram-dark.png#gh-dark-mode-only)
![Microservice Architecture](assets/diagram.png#gh-light-mode-only)

## Related Sportiq services

- [API Gateway](https://github.com/Str1kez/SportiqAPIGateway)
- [Event Service](https://github.com/Str1kez/SportiqEventService)
- [Subscription Service](https://github.com/Str1kez/SportiqSubscriptionService)
- [Frontend App](https://github.com/Str1kez/SportiqReactApp)

## Documentation

OpenAPI - https://str1kez.github.io/SportiqUserService

## KDS and JWT Blacklist

Build Docker-image with cronjob on updating secret key for signing JWT (every 15 min by default):

```commanline
make build-kds
```

It improves user security. Generation of secret key is based on openssl.

## Microservice

Bcrypt was used as a password hashing function with 12 rounds. It reduces the chances to hack password via table methods. \
HMAC-SHA-256 was used to generate the JWT signature. \
UUID v6 is the primary key in user table, which increases the efficiency of caching operations.

### Startup

1. Create `.env` file and fill it:
   ```commandline
   make env
   ```
2. Run migrations:
   ```commandline
   make upgrade head
   ```
3. Create Docker-image:
   ```commandline
   make build
   ```
4. Run the microservice:
   ```commandline
   make up
   ```

`make down` - to stop
