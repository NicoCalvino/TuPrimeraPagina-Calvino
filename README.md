# kiosco_sole
Web para Administracion del Kiosco de un Colegio.

El kiosco funciona con tarjetas prepagas que las alumnas utilizan para comprar los productos.
Idealmente cada aluma tendría una sola tarjeta, pero se puede llegar a dar que por perdida o rotura, cada alumna tenga asociada mas de una tarjeta.

El proyecto tiene 3 clases: 
Alumnas: nombre, apellido y curso 
Tarjetas: codigo, saldo, alumna, fecha activacion y fecha ultima modificacion
Productos: nombre, marca, categoria, precio, stock y codigo de barras

Pasos para probar el proyecto.

1) Luego de clonar el repositorio desde github, dirigirse a la carpeta del proyecto y ubicarse en el nivel donde este el archivo "manage.py"

2) crear el entorno virtual corriendo el siguiente comando

    python -m venv .venv

3) Activar el entorno virtual corriendo el siguiente comando

    .venv/Scripts/activate

4) Instalar los requerimientos del archivo requierements.txt corriendo el siguiente comando

    pip install -r requierements.txt

5) Levantar el servidor corriendo el siguiente comando 
    
    python manage.py runserver

6) Bajar el servidor utilizando el atajo "Ctrl+C"

7) Al levantar el servidor se tiene que haber creado el archivo "db.sqlite3" con migraciones pendientes. Correr los siguientes comandos para terminar de configurar la base de datos

    python manage.py makemigrations
    python manage.py migrate

8) Correr el siguiente comando para crear un superuser y poder tener acceso a la administracion del portal

    python manage.py createsuperuser

9) Volver a levantar el servidor corriendo el siguiente comando 
    
    python manage.py runserver

10) Abrir el vinculo http://127.0.0.1:8000 o localhost:8000

11) En la home del portal apareceran 3 links principales: "Productos", "Alumnas" y "Tarjetas". En el navbar figuran los mismos 3 links + Home y Admin

12) Entrar al sector de Alumnas. En la parte superior aparece el boton "+ Nueva" para dar de alta nuevas alumnas.

Crear las siguientes 5 personas
      Nombre - Apellido - Curso
    a) Sofía - Gonzalez - 4°A
    b) Martina - Rodríguez - 3°B
    c) Valentina - López - 5°C
    d) Camila - Fernández - 6°A
    e) Lucía - García - 1°B

13) Utilizar el Campo "Buscar" de la parte superior para probar las siguientes busquedas (la cadena de texto se busca en el nombre y en el apellido)

    a) Buscar: i - Deberían aparecer 3 resultados
    b) Buscar: ez - Deberian aparecer 4 resultados
    c) Buscar: ina - Deberian aparecer 2 resultados


14) Entrar a cualquiera de los resultados de busqueda. Aparecera un detalle de la alumna que muestra: Nombre, Apellido, Curso, Saldo, Tarjetas asociadas y Ultimos 10 Movimientos

15) Ingresar a la seccion de Productos. Tambien deberia aparecer el boton "+ Nuevo" para dar de alta un nuevo producto

Crear los siguientes productos
        Nombre - Marca - Categoria - Precio - Stock - Codigo de Barras 
    a) Alfajor (Negro/Blanco) - Rasta - Alfajores y Galletitas - 1300 - 24 - 7798345610023
    b) Alfajor Chocolate Negro - Guaymallén - Alfajores y Galletitas - 600 - 48 - 7790080000012
    c) Agua Mineral Sin Gas 500ml - Villavicencio - Bebidas - 1100 - 24 - 7790900000117
    d) Gaseosa Cola 500ml - Coca-Cola - Bebidas - 1500 - 30 - 7790895000087
    e) Bombón Bon o Bon (Unidad) - Arcor - Golosinas y Chocolates - 450 - 60 - 7790580000148
    f) Caramelos Sugus Confitados (Paq) - Sugus - Golosinas y Chocolates - 1600 - 15 - 7790345000179

16) Utilizar el Campo "Buscar" de la parte superior para probar las siguientes busquedas (la cadena de texto se busca en el nombre, en la marca y en la categoria)

    a) Buscar: choco - Deberían aparecer 3 resultados
    b) Buscar: car - Deberian aparecer 1 resultados
    c) Buscar: negr - Deberian aparecer 2 resultados


17) Entrar a cualquiera de los resultados de busqueda. Aparecera un detalle del producto que muestra: Nombre, Marca, Codigo de Barras, Stock y Precio

18) Ingresar a la seccion de Tarjetas. Tambien deberia aparece el boton "+ Nueva Tarjeta".

Dar de alta los siguientes codigos
    a) 501364000000001
    b) 501364000000002
    c) 501364000000003
    d) 501364000000004
    e) 501364000000005
    f) 501364000000006
    g) 501364000000007
    h) 501364000000008
    i) 501364000000009
    j) 501364000000010
    k) 501364000000011
    l) 501364000000012
    m) 501364000000013
    n) 501364000000014
    o) 501364000000015
    p) 501364000000016
    q) 501364000000017
    r) 501364000000018
    s) 501364000000019
    t) 501364000000020

19) Utilizar el Campo "Buscar" de la parte superior para probar las siguientes busquedas (los numeros buscados se buscan solo en los ultimos 9 digitos del codigo de tarjeta)

    a) Buscar: 1 - Deberían aparecer 11 resultados
    b) Buscar: 13 - Deberia aparecer 1 resultado
    c) Buscar: 501364 - Deberian aparecer 0 resultados

20) Entrar a cualquiera de los resultados de busqueda. Aparecera un detalle del producto que muestra:
Saldo, alumna que tiene la tarjeta (o "Sin alumna asociada" si la tarjeta no tiene dueña aun), codigo, fecha de activacion(fecha de alta) y fecha ultima modificacion