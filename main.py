import getpass
import os
import re
import sys
import yaml
import shutil
import base64


def unpackage_jar(jarname):
    unpackagejar = 'jar xf ' + jarname
    os.system(unpackagejar)


def package_jar(jarname, list):
    packagejarpath = 'jar cf ' + jarname + ''
    for name in list:
        packagejarpath = packagejarpath + " " + name
    os.system(packagejarpath)


def create_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    print("Created new folder: " + path)


def create_file(path, content):
    with open(path, 'w+') as f:
        f.write(content)


def copy_file(path, destination):
    shutil.copy(path, destination, follow_symlinks=True)
    print("Copying " + path + " to " + destination)


def change_file_name(path, new):
    os.rename(path, new)
    print("Created file: ")


def run_command(command):
    os.system(command)


def replace_file_content(file, variable, value):
    text = file.read()
    newcontent = re.sub(variable, value, text)
    print(newcontent)
    file.write(newcontent)


def modify_yml_jar(jarname, ymlconfigname):
    unpackage_jar(jarname)
    choose = input("Escribir una opcion: 'qa', 'dev' o 'prod'. Por defecto: application.yml ").lower()
    sub = ""
    if choose == "qa":
        sub = "-qa"
        print("qa seleleccionado, abriendo application-qa.yml")
    if choose == "dev":
        sub = "-dev"
        print("dev seleccionado, abriendo application-dev.yml")
    if choose == "prod":
        sub = "-prod"
        print("prod seleccionado, abriendo application-prod.yml")
    if sub == "":
        print("Abriendo application.yml por defecto")

    with open("BOOT-INF/classes/application" + sub + ".yml", 'r') as file:
        yml_file = yaml.safe_load(file)
    installer = open(ymlconfigname)

    for line in installer:
        if line.find(': ') > -1:
            print(yml_file)
            print(line + " Valor actual: ")
            print(parse_int(get_element(yml_file, path_to_list(line))))
            if get_type_line(line) == "password":
                passinput = getpass.getpass()
                if len(passinput) > 0:
                    answer = like_password(passinput)
            else:
                answer = input()
            if len(answer) > 0:
                if get_type_line(line) == "list":
                    answer = like_list(answer)
                if get_type_line(line) == "boolean":
                    answer = like_boolean(answer)
                change_element(yml_file, answer, path_to_list(line))
    with open("BOOT-INF/classes/application" + sub + ".yml", 'w') as new_file:
        yaml.dump(yml_file, new_file)
    print("Generando jar " + jarname)
    package_jar(jarname, ["BOOT-INF", "META-INF", "org"])


def get_type_line(line):
    return line[line.index('[')+1:line.index(']')]


def path_to_list(line):
    newline = line[0:line.index('[')]
    return list(newline.split("/"))


def change_element(yml, value, path):
    first = parse_int(path[0])
    element = yml.get(first)
    if element is None:
        yml[first] = None
    path.remove(path[0])
    if len(path) > 0:
        if type(element) is dict or type(element) is list:
            change_element(element, value, path)
    else:
        yml[first] = parse_int(value)


def get_element(yml, path):
    if len(path) > 0:
        element = path[0]
        new_path = path.copy()
        new_path.remove(element)
        if yml.get(parse_int(element)) is None:
            print("No es posible mostrar el valor")
        else:
            return get_element(yml[parse_int(element)], new_path)
    else:
        return yml


def like_list(answer):
    new = list(answer.split(" "))
    for strg in new:
        val = parse_int(strg)
        new.remove(strg)
        if type(val) is int:
            new.insert(0, val)
    return new


def parse_int(answer):
    if type(answer) is str:
        if re.match('^[0-9]+$', answer) is not None:
            return int(answer)
    return answer


def like_boolean(answer):
    return answer.lower() == 'true'


def like_password(answer):
    answer_bytes = answer.encode('ascii')
    a = base64.b64encode(answer_bytes)
    return "encoded:" + a.decode('ascii')


def find_extension_files(type):
    file_list = []
    extension = "." + type
    for file in os.listdir("."):
        if file.endswith(extension):
            file_list.insert(0, file)
    return file_list


if __name__ == '__main__':
    jarname = sys.argv[1]
    servicename = sys.argv[2]
    ymlconfigname = sys.argv[3]
    modify_yml_jar(jarname, ymlconfigname)
    print("Moviendo " + jarname + " a etc/systemd/system")
    #shutil.move(jarname, "etc/systemd/system")
    if os.path.exists(servicename):
        print("Moviendo " + servicename + " a etc/systemd/system")
        shutil.move(servicename, "etc/systemd/system")
    else:
        print("No encontrado servicio con el nombre: " + servicename)
