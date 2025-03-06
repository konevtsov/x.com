# Auth microservice
- [Database schema](https://drawsql.app/teams/xcom-1/diagrams/x-auth-service)

This service is responsible for user registration. 
Technologies such as:
- FastAPI
- SQLAlchmemy
- JWT
- Uvicorn

![image](https://github.com/user-attachments/assets/2e0c5ac6-c914-4261-ac92-2855ec2fa996)

# Getting started


### 1. Token issuance
Create directory for private and public key
```shell
mkdir src/certs && cd crs/certs
```
Generate an RSA private key, of size 2048
```shell
openssl genrsa -out jwt-private.pem 2048
```
Extract the public key from the kay pair, which can be used in a certificate
```shell
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
