#!/usr/bin/env python3

from argparse import ArgumentParser
import os
from tools import input_passphrase, execute_command, replace_in_file

# Arguments
parser = ArgumentParser(description='Create a server certificate.')
parser.add_argument('signing-ca-name', help='The signing CA name (ex. signing-ca-01)')
parser.add_argument('server-certificate-name', help='The server certificate name (ex. service.krumer.it)')
arguments = vars(parser.parse_args())

signing_ca_name = arguments['signing-ca-name']
server_certificate_name = arguments['server-certificate-name']

# Locations
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.getcwd()

# Information
print('Information')
print('=================')
print('')

organization_name = input('Organization Name (ex. Krumer): ')
common_name = input('Common Name (ex. service.krumer.it): ')

print('')
print('')

# Domain Components
print('Domain Components')
print('=================')
print('- Example: Domain Component 0 - it')
print('- Example: Domain Component 1 - krumer')
print('- Example: Domain Component 2 - service')
print('- Enter an empty line when you are finished')
print('')

domain_components = []
counter = 0

while True:
    domain_component = input('Domain Component {0}: '.format(counter))
    domain_component = domain_component.strip()
    counter += 1

    if(domain_component == ''):
        break

    domain_components.append(domain_component)


print('')
print('')

# Alternative Names
print('Alternative Names')
print('=================')
print('- Example: Alternative Name 0 - service.krumer.it')
print('- Example: Alternative Name 1 - *.service.krumer.it')
print('- Enter an empty line when you are finished')
print('')

alternative_names = []
counter = 0

while True:
    alternative_name = input('Alternative Name {0}: '.format(counter))
    alternative_name = alternative_name.strip()
    counter += 1

    if(alternative_name == ''):
        break

    alternative_names.append(alternative_name)


print('')
print('')

# Passphrases
print('Phassphrases')
print('=================')
print('')

sigining_ca_passphrase = input_passphrase('Signing CA passphrase')

print('')
print('')

# Confirmation
print('Confirmation')
print('=================')
print('Please check the following information bevor continue with the creation of the server certificate:')
print('')

print('- Organization Name: {0}'.format(organization_name))
print('- Common Name: {0}'.format(common_name))
print('- Domain Components: {0}'.format('.'.join(domain_components)))
print('- Alternative Names: {0}'.format(', '.join(alternative_names)))
print('')

response = input('Do you want to create the server certificate? [y,N] ')
print('')

if response != 'y' and response != 'Y':
    quit(-1)

# Generation
print('Generation')
print('=================')
print('')

execute_command('Create folders', 'mkdir -p server-certificates/{0}/configs server-certificates/{0}/private-keys server-certificates/{0}/certificates server-certificates/{0}/certificate-chains server-certificates/{0}/certificate-signing-requests'.format(signing_ca_name))

execute_command('Copy configuration template', 'cp {0}/templates/server-certificate.conf server-certificates/{1}/configs/{2}.conf'.format(script_dir, signing_ca_name, server_certificate_name))
replace_in_file('Replace organization name', 'server-certificates/{0}/configs/{1}.conf'.format(signing_ca_name, server_certificate_name), 'ORGANIZATION_NAME', organization_name)
replace_in_file('Replace common name', 'server-certificates/{0}/configs/{1}.conf'.format(signing_ca_name, server_certificate_name), 'COMMON_NAME', common_name)
replace_in_file('Replace domain components', 'server-certificates/{0}/configs/{1}.conf'.format(signing_ca_name, server_certificate_name), 'DOMAIN_COMPONENTS', '\n'.join(['{0}.domainComponent = "{1}"'.format(index, domain_component) for index, domain_component in enumerate(domain_components)]))
replace_in_file('Replace alternative names', 'server-certificates/{0}/configs/{1}.conf'.format(signing_ca_name, server_certificate_name), 'ALTERNATIVE_NAMES', ','.join(['DNS:' + alternative_name for alternative_name in alternative_names]))

execute_command('Generate private key and certificate signing request', 'openssl req -new -config server-certificates/{0}/configs/{1}.conf -out server-certificates/{0}/certificate-signing-requests/{1}.csr -keyout server-certificates/{0}/private-keys/{1}.key'.format(signing_ca_name, server_certificate_name))
execute_command('Generate and sign certificate', 'openssl ca -batch -config ca/{0}/{0}.conf -in server-certificates/{0}/certificate-signing-requests/{1}.csr -out server-certificates/{0}/certificates/{1}.crt -extensions server_ext -passin stdin'.format(signing_ca_name, server_certificate_name), stdin=sigining_ca_passphrase)
execute_command('Generate certificate chain', 'cat server-certificates/{0}/certificates/{1}.crt ca/{0}/certificate.crt > server-certificates/{0}/certificate-chains/{1}.pem'.format(signing_ca_name, server_certificate_name))
execute_command('Delete certificate signing request', 'rm -rf server-certificates/{0}/certificate-signing-requests/{1}.csr'.format(signing_ca_name, server_certificate_name))

print('')
