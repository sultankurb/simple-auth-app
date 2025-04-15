# This prject is for deep learninng Authinticate


___
## Description
 - This service solve problem with managing users

___


## Table of content
 - [Installation](#installation)
___


## Installation
### Requirments that you neeed
* git
* docker
* docker compose

## First step is clone repository
```shell
git clone https://github.com/sultankurb/simple-auth-app.git
```

## Second step is 
Create certificate that neew for authinticate
```shell
mkdir certificates/ && cd certificate/ && openssl genrsa -out private-key.pem 2048 && openssl rsa -in private-key.pem -outform PEM -pubout -out public-key.pem
```

## And Last Step is run this project
```shell
docker compose up -d
```
