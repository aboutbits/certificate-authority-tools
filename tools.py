import getpass
import os
import subprocess

def input_passphrase(description):
    passphrase = getpass.getpass(description + ': ')
    passphrase_confirmation = getpass.getpass(description + ' Confirmation: ')

    if passphrase != passphrase_confirmation:
        print()
        print('Passphrases do not match. Please retry!')
        print()
        quit(-1)

    return passphrase

def execute_command(task, command, cwd=None, stdin=None):
    print('- ' + task)

    process = subprocess.Popen(command, shell=True, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.communicate(input=(stdin.encode() if stdin != None else None))[0]

    if process.returncode != 0:
        print()
        print('Execution faild: "' + task)
        print()
        print(output[0].decode("utf-8"))
        quit(-1)

def replace_in_file(task, file, search, replace):
    print('- ' + task)

    if not os.path.exists(file):
        print()
        print('Execution faild: "' + task)
        print()
        print('File {0} does not exist.'.format(file))
        quit(-1)

    try:
        f = open(file, 'r')
        data = f.read()
        f.close()

        data = data.replace(search, replace)

        f = open(file, 'w')
        f.write(data)
        f.close()
    except Exception as e:
        print()
        print('Execution faild: "' + task)
        print()
        print(e)
        quit(-1)
