import sender_stand_request
import data

# función que cambia los valores del parámetro "firstName" en data
def get_user_body(first_name):
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" para conservar los datos del
    # diccionario de origen
    current_body = data.user_body.copy()
    #se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

#print(data.user_body)
#print(get_user_body("Mariana"))
#print(data.user_body)

# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body("Aa")
    print(user_body)
    # se crea una variable y se crea un nuevo usuario, en éste ejemplo "Aa"
    user_response = sender_stand_request.post_new_user(user_body)
    #Comprobar status code
    assert user_response.status_code == 201
    print('Status Code de comprobación 1 al crear un nuevo usuario :' + str(user_response.status_code))
    #Comprobar authToken
    assert user_response.json()["authToken"] != ""
    print('AuthToken: ' + user_response.json()["authToken"])
    #El resultado de la solicitud de recepción de datos de la tabla "user_model"
    #se guarda en la variable "users_table_response"
    #Aquí se crea una variable que accede a la tabla de usuario
    users_table_response = sender_stand_request.get_users_table()
    # El string que debe estar en el cuerpo de la respuesta para recibir datos de la tabla "users" se ve así
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1
    print('El usario existe y es único: ' + str_user)

#Función de prueba positiva
def positive_assert(first_name):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(first_name)
    # El resultado de la solicitud para crear un/a nuevo/a usuario/a se guarda en la variable user_response
    # Al enviar los datos o "el body" del usuario guardamos en user_response el estado del servicio al recibirlo
    user_response = sender_stand_request.post_new_user(user_body)
    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""

    # Comprobación en la tabla user_model ejercicio anterior
    # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
    users_table_response = sender_stand_request.get_users_table()

    # String que debe estar en el cuerpo de respuesta
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1

# Prueba 2.
# El parámetro "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")
    print('Prueba positiva al agregar el fisrtName con 15 caracteres')

# Prueba 3. Preparación
# Función de Pruebas Negativas para las Pruebas de la 3 a la 7
def negative_assert_symbol(first_name):
    # Comprueba si esta función recibe una versión actualizada del cuerpo de solicitud de creación de
    # un nuevo usuario/a a la vasriable user_body
    user_body = get_user_body(first_name)
    # Comprueba si la variable "response" alamacena el resultado de la solicitud
    response = sender_stand_request.post_new_user(user_body)
    # Comprueba si la respuesta contiene el código 400
    assert response.status_code == 400
    # Comprueba si el atribnuto "code" en el cuerpo de respuesta es 400
    assert response.json()["code"] == 400
    # Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:
    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, "\
                                         "la longitud debe ser de 2 a 15 caracteres."

#Ahora sí Prueba 3. Error
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")
    print('Prueba 3 statusCode 400 al agregar 1 sólo caracter')

#Prueba 4. Error
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")
    print('Prueba 4 statusCode 400 al agregar 16 caracteres')

#Prueba 5. Error
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")
    print('Prueba 5 statusCode 400 al agregar espacios en el nombre')

#Prueba 6. Error
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")
    print('Prueba 6 statusCode 400 al agregar símbolos en el nombre')

#Prueba 7. Error
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")
    print('Prueba 7 statusCode 400 al agregar letras en el nombre')

#Función para Prueba 8 y Prueba 9. Error
def negative_assert_no_firstname(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

#Prueba 8. Error
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    user_body = data.user_body.copy()
    #El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    #Mi explicación. Hago una llamada a la función negative_asser_no_firstname y le envío el body que copié de data y en
    #el cual borré "firstname
    negative_assert_no_firstname(user_body)
    print('Prueba 8 statusCode 400 al agregar un usuario sin el campo nombre')

#Prueba 9. Error
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)
    print('Prueba 9 statusCode 400 al agregar un usuario con el campo nombre vacío')

#Prueba 10. Error
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    print('Prueba 10 statusCode 400 al agregar un usuario con un número en el campo nombre')
