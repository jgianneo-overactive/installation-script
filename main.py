import os
import re
import yaml
import shutil


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


def replace_file_content(file, variable, value):
    text = file.read()
    newcontent = re.sub(variable, value, text)
    print(newcontent)
    file.write(newcontent)


def modify_yml_jar(jarname):
    unpackage_jar(jarname)
    choose = input("Write an option: 'qa', 'dev' or 'prod'. Nothing for default")
    sub = ""
    if choose == "qa" or choose == "QA":
        sub = "-qa"
        print("qa selected, opening application-qa.yml")
    if choose == "dev" or choose == "DEV":
        sub = "-dev"
        print("dev selected, opening application-dev.yml")
    if choose == "prod" or choose == "PROD":
        sub = "-prod"
    else:
        print("Opening application.yml by default")

    with open("BOOT-INF/classes/application" + sub + ".yml", 'r') as file:
        yml_file = yaml.safe_load(file)
    installer = open("installation.yml")

    for line in installer:
        if line.find(': ') > -1:
            print(line + " Valor actual: ")
            print(parse_int(get_element(yml_file, path_to_list(line))))
            answer = input()
            if len(answer) > 0:
                if "uy-edge-mobile_bins:" in line:
                    answer = like_list(answer)
                if "security_resource_enabled:" in line or "rest-config_restConnectors_0_apacheHttpClientDetails_enableHostNameVerifier:" in line:
                    answer = like_boolean(answer)
                change_element(yml_file, answer, path_to_list(line))
    with open("BOOT-INF/classes/application" + sub + ".yml", 'w') as new_file:
        yaml.dump(yml_file, new_file)
    print("Packing jar " + jarname)
    package_jar(jarname, ["BOOT-INF", "META-INF", "org"])


def path_to_list(line):
    newline = line[0:line.index(':')]
    return list(newline.split("_"))


def change_element(yml, value, path):
    first = parse_int(path[0])
    element = yml[first]
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
    return answer == 'true' or answer == 'TRUE' or answer == 'True'


def find_extension_files(type):
    extension = "." + type
    for file in os.listdir("."):
        if file.endswith(extension):
            return file


if __name__ == '__main__':
    name = "uy-edge-mobile-1.0"
    jarname = name + ".jar"
    modify_yml_jar(jarname)
    print("Moving jar " + jarname + " to etc/systemd/system")
    shutil.move(jarname, "etc/systemd/system")
    serverfile = find_extension_files("service")
    print("Service found: " + serverfile)
    if serverfile is not None:
        shutil.move(serverfile, "etc/systemd/system")
    #os.system("systemctl daemon-reload")
    #os.system("systemctl start uy-adapter-soft-token.service")