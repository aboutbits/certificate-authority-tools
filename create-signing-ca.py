#!/usr/bin/env python3

from argparse import ArgumentParser
import os
from tools import input_passphrase, execute_command, replace_in_file

# Arguments
parser = ArgumentParser(description='Create a signing certificate authority.')
parser.add_argument('root-ca-name', help='The root CA name (ex. root-ca)')
parser.add_argument('signing-ca-name', help='The signing CA name (ex. signing-ca-01)')
arguments = vars(parser.parse_args())

root_ca_name = arguments['root-ca-name']
signing_ca_name = arguments['signing-ca-name']

# Locations
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.getcwd()

# Information
print('Information')
print('=================')
print('')

organization_name = input('Organization Name (ex. Krumer): ')
common_name = input('Common Name (ex. Krumer Signing CA 01): ')

print('')
print('')

# Domain Components
print('Domain Components')
print('=================')
print('- Example: Domain Component 0 - it')
print('- Example: Domain Component 1 - krumer')
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

# Passphrases
print('Phassphrases')
print('=================')
print('')

root_ca_passphrase = input_passphrase('Root CA passphrase')
signing_ca_passphrase = input_passphrase('Signing CA passphrase')

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
print('')

response = input('Do you want to create the root certificate authority? [y,N] ')
print('')

if response != 'y' and response != 'Y':
    quit(-1)

# Generation
print('Generation')
print('=================')
print('')

execute_command('Create folders', 'mkdir -p ca/{0} ca/{0}/archive ca/{0}/db'.format(signing_ca_name))

execute_command('Create database structure (index.db)', 'cp /dev/null ca/{0}/db/index.db'.format(signing_ca_name))
execute_command('Create database structure (index.db.attr)', 'cp /dev/null ca/{0}/db/index.db.attr'.format(signing_ca_name))
execute_command('Create database structure (crt.srl)', 'echo 01 > ca/{0}/db/crt.srl'.format(signing_ca_name))
execute_command('Create database structure (crl.srl)', 'echo 01 > ca/{0}/db/crl.srl'.format(signing_ca_name))

execute_command('Copy configuration template', 'cp {0}/templates/signing-ca.conf ca/{1}/{1}.conf'.format(script_dir, signing_ca_name))
replace_in_file('Replace signing ca name', 'ca/{0}/{0}.conf'.format(signing_ca_name), 'SIGNING_CA_NAME', signing_ca_name)
replace_in_file('Replace organization name', 'ca/{0}/{0}.conf'.format(signing_ca_name), 'ORGANIZATION_NAME', organization_name)
replace_in_file('Replace common name', 'ca/{0}/{0}.conf'.format(signing_ca_name), 'COMMON_NAME', common_name)
replace_in_file('Replace domain components', 'ca/{0}/{0}.conf'.format(signing_ca_name), 'DOMAIN_COMPONENTS', '\n'.join(['{0}.domainComponent = "{1}"'.format(index, domain_component) for index, domain_component in enumerate(domain_components)]))

execute_command('Generate private key and certificate signing request', 'openssl req -new -config ca/{0}/{0}.conf -out ca/{0}/certificate-signing-request.csr -keyout ca/{0}/private-key.key -passout stdin'.format(signing_ca_name, signing_ca_passphrase), stdin=signing_ca_passphrase)
execute_command('Generate and sign certificate', 'openssl ca -batch -config ca/{0}/{0}.conf -in ca/{1}/certificate-signing-request.csr -out ca/{1}/certificate.crt -extensions signing_ca_ext -passin stdin'.format(root_ca_name, signing_ca_name), stdin=root_ca_passphrase)
execute_command('Delete certificate signing request', 'rm -rf ca/{0}/certificate-signing-request.csr'.format(signing_ca_name))

print('')
