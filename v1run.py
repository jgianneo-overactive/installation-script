import os
import shutil


def openF():
    prop = open(r"C:\Users\javier.gianneo\Desktop\server-example\BOOT-INF\classes\application.properties", 'r+')
    content = prop.read()
    print(content)
    prop.close()


def unpackageJar(jarName):
    unpackageJar = 'jar xf ' + jarName
    os.system(unpackageJar)


def packageJar(jarName, list):
    packageJarPath = 'jar cf ' + jarName + ''
    for name in list:
        packageJarPath = packageJarPath + " " + name
    os.system(packageJarPath)


def readFromCommand(text):
    return input(text)


def runJar():
    os.system('java -jar awards-api-0.0.1-SNAPSHOT.jar')


def create_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


if __name__ == '__main__':
    create_folder("new folder")
    #unpackageJar("awards-api-0.0.1-SNAPSHOT.jar")
    #open()
    #folderList = ["BOOT-INF", "META-INF", "org"]
    #packageJar("awards-api-0.0.2-SNAPSHOT.jar", folderList)
