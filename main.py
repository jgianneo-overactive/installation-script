import os
import re
import yaml
import shutil


def unpackage_jar(jarName):
    unpackageJar = 'jar xf ' + jarName
    os.system(unpackageJar)


def package_jar(jarName, list):
    packageJarPath = 'jar cf ' + jarName + ''
    for name in list:
        packageJarPath = packageJarPath + " " + name
    os.system(packageJarPath)


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
    print("Changed file: " + new)


def run_command(command):
    os.system(command)


def path_to_list(line):
    newline = line[0:line.index(':')]
    return list(newline.split("."))


def change_element(yml, value, path):
    first = path[0]
    element = yml[first]
    path.remove(first)
    if len(path) > 0 and (type(element) is dict or type(element) is list):
        change_element(element, value, path)
    else:
        yml[first] = value

def replace_file_content(file, variable, value):
    text = file.read()
    newContent = re.sub(variable, value, text)
    print(newContent)
    file.write(newContent)

def yml_edit():
    unpackage_jar("uy-edge-mobile-1.0.jar")
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
            print(line)
            answer = input()
            if len(answer) > 0:
                change_element(yml_file, answer, path_to_list(line))

    with open("BOOT-INF/classes/application" + sub + ".yml", 'w') as new_file:
        yaml.dump(yml_file, new_file)
    package_jar("uy-edge-mobile-1.2.jar", ["BOOT-INF", "META-INF", "org"])


if __name__ == '__main__':
    create_folder("datos/uy-adapter-soft-token")
    create_folder("datos/uy-adapter-soft-token/archive")
    create_folder("datos/uy-adapter-soft-token/conf")
    create_folder("datos/uy-adapter-soft-token/current")
    create_folder("datos/uy-adapter-soft-token/install_guide")
    create_folder("datos/uy-adapter-soft-token/latest")
    copy_file("datos/uyisamadapter/server.jks", "datos/uy-adapter-soft-token/archive")
    copy_file("datos/uyisamadapter/application-ext.properties", "datos/uy-adapter-soft-token/conf")
    copy_file("datos/uyisamadapter/server.jks", "datos/uy-adapter-soft-token/conf")
    copy_file("datos/uyisamadapter/server-public.cer", "datos/uy-adapter-soft-token/install_guide")
    copy_file("datos/uyisamadapter/client.jks", "datos/uy-adapter-soft-token/install_guide")
    copy_file("datos/uyisamadapter/client-public.cer", "datos/uy-adapter-soft-token/install_guide")
    copy_file("datos/uyisamadapter/creaJKS.txt", "datos/uy-adapter-soft-token/install_guide")
    copy_file("datos/uyisamadapter/encrypt.sh", "datos/uy-adapter-soft-token/install_guide")
    copy_file("datos/uyisamadapter/install.sh", "datos/uy-adapter-soft-token/install_guide")
    copy_file("datos/uyisamadapter/isamserver.cer", "datos/uy-adapter-soft-token/install_guide")
    copy_file("datos/uyisamadapter/jasypt-1.9.3.jar", "datos/uy-adapter-soft-token/install_guide")
    copy_file("datos/uyisamadapter/soft-token.conf", "datos/uy-adapter-soft-token/install_guide")

    create_file("datos/uy-adapter-soft-token/conf/application-ext.properties",
    '''logging.maxfilesizemb=30
    ldap.url=ldaps://uydcpan01.bancocomercial.com.uy:3269/
    ldap.domain=bancocomercial.com.uy
    jwt.keyID=4ea611a3-e078-4e99-b30d-f65d673b042a
    jwt.
    privateKey=MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDBuYhJRHEKJ4dRiybpxNnkb8NxtH1NLed+DoNtCSmgtN
    IAmDlB25GS7/Tk7d5Tj4pRA3gXNw3MeYkNCtZ8Z2mSE
    /f4L9fV1s1+4LQKd47LUZfDTyhOHfxtyFb28ZfR6GVrB0cFC8xiNWFkJArJx74gZG7dDrpfdwMbySDQmXZ5eqjlF3YFITb5pqbjvZl5Ck
    4qRDhCVEkXnqWLZpCQgQy0nz0rg4XYikgmLfkiGuQ44yH495UxBDXBdFxNTy0i9MnG6Ytjf5dkzxldqTYBVxpZbPvaMfJflknbmeEAuw3
    ArzWO/KSxNGMCP/0riGf+ri4n55I2j+xR5MbAFyGs8YmjAgMBAAECggEBAKtgr6Fpa7r49yv7NySNIdmFydf4PPUfC
    /CndDrsZSgnbrRZ9iU90g20O+ieShWQIWPD9uRKrulaBxVDpjWN4oX5JmAoKv+gtFBvBrdPx0I031ZH27cnrd2M4uo5Ff77YWUKnhhntJ
    qY8Jx/ig+xpY
    /QaYcj9Vpo1ZYqGt6PNJEHmG2BKU27gwjJp5MRmIpbT0CgOmjZ2mGwHzTyKoc3LlYEVK8c2jBuS4GilcivzKjHUtKGmbIcfSXZfjOGQkO
    6fwgQWC
    /qEg8o9L0l95AuaqWbLu7nz8bns8frGZb7iHolJBQmFXtKbGg9KABlCyMLuCYDSZEtidNVBITYZNCUBOECgYEA61b8FXlKziMc7OlNUMq
    T/I6HYl0mGl7vs2iAajTvlwkvq1/1DgwmvqoQPN/3OE/JR/mnJdsXJ9mFqTMfBHOIugIaLDk2zCxq+TOYxc1WsLEOX2OHq55J8U4Jo
    /b64DfinvP4+N2/4jESGdkTPeKFvBt368GKb10Q/UCiukJyxVMCgYEA0rtLA0t6NabXuJauj
    /4kLrwTMK7RyUWbj+PiFd9uThjAvwapHm0xJIl2xMCujVbU7TpJTYXOrbvjkn0v33L3LcUarqFthuAesjHZoSGRGh7SW53QgfAXkFqYZ6
    pWzaS3RyRhlkfpO92O1ahw/Uz30heeaISqTX1ldyPGb/yX0HECgYArJSxcB3umZRuVd4Q8LpeI8txxNSCaLxOE8cCxN
    /lA2GdL5PC5XZLw257Uej8JrN76+hMhxpPtM1zk00F5gHDtoRsJRof8UJxgCYyVnvqotB0tccLavM9TlPoBfHMsDjLW72WSwpy+LD7kTD
    7R1qir/uEycK4fkpFdzK7ItQvzjwKBgAJeqtRJqAEsdCaWQzZJVFzWLp0QijlqN
    /qhRGyci6ADNT+wsnwuHCxeA2DpDc13GYPlcOeXRqC7iS6fi8dGgrMYEVm
    /ZPzsTkwQtXLTbs9NY242Ux7y9UDhU+9ugfVkEc+SACrxehT7Q9zxPPwMPok1TMm+HDAs5dQ2KcgenhJxAoGATpIBTsKPKBmoHmJfKWcm
    rHQ8BB9xo0NUYX3mlWArgqFdoZfnBfUp1esAM88L0mW7iuGmqopkfCkAOd5j8DDdiD0MRZPTzYAmxeK+bTzjMIG5+uaxKxT6ly1tfGdTY
    +Tt58LTuuV0V+e87xudPlbEM3euAzUshm0ZRpKaY4cH/YQ=
    jwt.publicKey=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwbmISURxCieHUYsm6cTZ5G
    /DcbR9TS3nfg6DbQkpoLTSAJg5QduRku/05O3eU4+KUQN4FzcNzHmJDQrWfGdpkhP3+C
    /X1dbNfuC0CneOy1GXw08oTh38bchW9vGX0ehlawdHBQvMYjVhZCQKyce+IGRu3Q66X3cDG8kg0Jl2eXqo5Rd2BSE2+aam472ZeQpOKkQ
    4QlRJF56li2aQkIEMtJ89K4OF2IpIJi35IhrkOOMh+PeVMQQ1wXRcTU8tIvTJxumLY3+XZM8ZXak2AVcaWWz72jHyX5ZJ25nhALsNwK81
    jvyksTRjAj/9K4hn/q4uJ+eSNo/sUeTGwBchrPGJowIDAQAB
    nazca.host.name=https://<SERVER_ADAPTER_NAZCA>:<PORT_ADAPTER_NAZCA>
    jks.algorithm=JKS
    jks.password=
    jks.store=''')

    create_file("datos/uy-adapter-soft-token/conf/logback-spring.xml",
    '''<?xml version="1.0" encoding="UTF-8"?>
    <!--
    logging props
    Properties set in /datos/uy-adapter-soft-token/conf/application-ext.properties file
    logging.config=/datos/uy-adapter-soft-token/conf/logback-spring.xml
    logging.file=/var/log/uy-adapter-soft-token.log
    logging.maxfilesizemb=30
    -->
    <configuration>
     <conversionRule conversionWord="clr" converterClass="org.springframework.boot.logging.logback.
    ColorConverter" />
     <conversionRule conversionWord="wex" converterClass="org.springframework.boot.logging.logback.
    WhitespaceThrowableProxyConverter" />
     <conversionRule conversionWord="wEx" converterClass="org.springframework.boot.logging.logback.
    ExtendedWhitespaceThrowableProxyConverter" />
     <property name="CONSOLE_LOG_PATTERN" value="${CONSOLE_LOG_PATTERN:-%clr(%d{yyyy-MM-dd HH:mm:ss.SSS})
    {faint} %clr(${LOG_LEVEL_PATTERN:-%5p}) %clr(${PID:- }){magenta} %clr(---){faint} %clr([%15.15t]){faint} 
    %clr(%-40.40logger{39}){cyan} %clr(:){faint} %m%n${LOG_EXCEPTION_CONVERSION_WORD:-%wEx}}"/>
     <property name="FILE_LOG_PATTERN" value="%d{yyyy-MM-dd HH:mm:ss.SSS} ${LOG_LEVEL_PATTERN:-%5p} ${PID:
    - } --- [%t] %-40.40logger{39} : %m%n${LOG_EXCEPTION_CONVERSION_WORD:-%wEx}"/>
     <property name="LOG_FILE" value="${LOG_FILE:-${LOG_PATH:-${LOG_TEMP:-${java.io.tmpdir:-/tmp}}}
    /spring.log}"/>
     <springProperty scope="context" name="MAX_FILE_SIZE_MB" source="logging.maxfilesizemb" defaultValue="
    10"/>
     <springProperty scope="context" name="TOTAL_SIZE_MB" source="logging.totalsizemb" defaultValue="200"
    />
     <springProperty scope="context" name="HISTORY_DAYS" source="logging.historydays" defaultValue="30"/>
     <logger name="org.hibernate.SQL" level="ERROR"/>
     <logger name="org.apache.catalina.startup.DigesterFactory" level="ERROR"/>
     <logger name="org.apache.catalina.util.LifecycleBase" level="ERROR"/>
     <logger name="org.apache.coyote.http11.Http11NioProtocol" level="WARN"/>
     <logger name="org.apache.sshd.common.util.SecurityUtils" level="WARN"/>
     <logger name="org.apache.tomcat.util.net.NioSelectorPool" level="WARN"/>
     <logger name="org.crsh.plugin" level="WARN"/>
     <logger name="org.crsh.ssh" level="WARN"/>
     <logger name="org.eclipse.jetty.util.component.AbstractLifeCycle" level="ERROR"/>
     <logger name="org.hibernate.validator.internal.util.Version" level="WARN"/>
     <logger name="org.springframework.boot.actuate.autoconfigure.CrshAutoConfiguration" level="WARN"/>
     <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
     <encoder>
     <pattern>${CONSOLE_LOG_PATTERN}</pattern>
     <charset>utf8</charset>
     </encoder>
     </appender>
     <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
     <encoder>
     <pattern>${FILE_LOG_PATTERN}</pattern>
     </encoder>
     <file>${LOG_FILE}</file>
     <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
     <fileNamePattern>${LOG_FILE}-%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
     <maxFileSize>${MAX_FILE_SIZE_MB}MB</maxFileSize>
     </rollingPolicy>
     </appender>
     <root level="INFO">
     <appender-ref ref="CONSOLE" />
     <appender-ref ref="FILE" />
     </root>
     </configuration>''')
    run_command("keytool -import -alias adapterNazca -keystore server.jks -file adapterNazca.crt")
    run_command("keytool -exportcert -alias adapterSoftToken -file adapterSoftToken.crt -keystore /datos/uy-adapter-softtoken/conf/server.jks -storepass password")
    run_command("echo "" | openssl s_client -connect 10.234.0.8:636 -showcerts 2>/dev/null | openssl x509 -out active_directory.crt")
    run_command("keytool -import -alias uydcpan01.bancocomercial.com.uy -keystore server.jks -file active_directory.crt")
    run_command("openssl base64 -in keystore.jks | tr -d \'\\n\' >> keystore64.txt")
