Certificate Authority Tools
===========================

This project is a wrapper around some OpenSSL commands. It should represent a tool, that helps you set up a root certificate authority with multiple signing certificate authorities. These certificate authorities can be used to generate and sign server certificates.

This is very useful if you want to have valid SSL certificates for your local development. You can simply serve your projects locally with the generated server certificates. In addition, you have to add the certificate of the root certificate authority to your machine aside the other already existing root certificates, so that the server certificates can be validated and trusted. 

## Requirements

- Python 3
- OpenSSL

## Setup

1. Clone the repository somewhere on your machine (ex. ~/Code/Certificate-Authority-Tools)
2. Create a folder where you want to generate all the keys and certificates (ex. ~/Certificates)
3. Go to the new folder where you want to generate all the keys and certificates and execute the following commands (ex. ~/Certificates)

## Root CA

Execute the following command to generate a root CA:

```bash
python3 ~/Code/Certificate-Authority-Tools/create-root-ca.py root-ca
```

## Signing CA

Execute the following command to generate a signing CA:

```bash
python3 ~/Code/Certificate-Authority-Tools/create-signing-ca.py root-ca signing-ca-01
```

## Server Certificate

Execute the following command to generate a server certificate:

```bash
python3 ~/Code/Certificate-Authority-Tools/create-server-certificate.py signing-ca-01 www.krumer.it
```
