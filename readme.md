Certificates
============

## Requirements

- Python 3
- OpenSSL

## Setup

1. Clone the repository somewhere on your machine (ex. ~/Code/Certificate-Authority-Tools)
2. Create a folder where you want to generate all the keys and certificates (ex. ~/Certificates)
3. Go to the new folder where you want to generate all the keys and certificates and execute the following commands.

## Root CA

Execute the following command to generate a root CA:

```bash
python3 /path/to/script/create-root-ca.py root-ca
```

## Signing CA

Execute the following command to generate a signing CA:

```bash
python3 /path/to/script/create-signing-ca.py root-ca signing-ca-01
```

## Server Certificate

Execute the following command to generate a server certificate:

```bash
python3 /path/to/script/create-server-certificate.py signing-ca-01 www.krumer.it
```
