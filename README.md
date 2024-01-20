# Solución challenge *its solutions*
 Repositorio con la solución del challenge para posición Python developer Sr. \
 Es una aplicación que usa `Django` como framework y en su Docker corre en el servidor `Gunicorn`, su base de datos usa el motor `sqlite` para ligereza y rápida ejecución más no es recomendable en ambiente reales productivos.
- **Autor:** Cristian Pardo
- **Email:** cristianpardoluna@gmail.com
- **Fecha:** 20 de enero de 2024

## Requerimientos
- Python 3.8
- Docker 24.0.7

## Supuestos y premisas
- **Test Driven Development:** Todos los parámetros de aceptación (enunciados en el documento que describe el challenge) tienen un caso de prueba asociado, las pruebas se encuentran en la ruta `backend/tests`.
- **Token de autenticación:** En la prueba se describe que cada oficial debe tener un token con el que el servidor autentica y permite publicar una infracción, en este caso opté por hacer una función que genera un token the 30 dígitos desde la interfaz administrativa cada vez que se crea un oficial, al momento de hacer el `POST` el servidor verifica que el token exista y asocia la solicitud al oficial sin necesidad de hacer `login` previamente. En ambientes reales productivos mi recomendación sería usar protocolos completos como oAuth2.0 y requerir un `login` lo que implica crear una sesión previamente, aquí no lo hice así para simplicidad y ligereza del servidor.
- **Infracciones asociadas al oficial:** Existe una llave foránea que asocia un oficial por cada infracción aunque no se presente como requerimiento en la prueba para demostrar una correcta autenticación.
- **Timestamp de infracciones automático:** Cada infracción crea un timestamp automáticamente al momento de creación del registro, aunque en la prueba se requiere que vaya en el cuerpo de la solicitud `POST` supuse que sería más fácil y reduce errores en las pruebas de los endpoints.
- **Enfoque orientado a funciones:** En un ambiente colaborativo optaría desarrollar bajo un enfoque orientado a objetos (OOP), sin embargo en este caso lo hice con funciones para reducir el tamaño del código final, se puede evidenciar por el uso de vistas como funciones y `wrappers` como `middleware`.

## Arquitectura AWS propuesta
Se propone dos tipos de arquitecturas dependiendo el tipo de uso y tráfico que se espere en la aplicación.

1. **Uso administrativo, tráfico estable:** En este caso propongo una arquitectura orientada al escalamiento vertical de una instancia provisionada con el contenedor Docker de la aplicación, bajo este stack:
    - **EC2:** Instancia virtual con un tamaño definido dependiendo del tamaño de la compañía.
    - **Multithreading:** Servidores como `gunicorn` tienen arquitectura maestro-esclavo con el cual se aseguran de repartir la carga interna equitativamente entre cada worker, la cantidad de workers se define bajo la fórmula `(Número de CPUs * 2) + 1`.
    - **RDS:** Servicio de base de datos relacionales administrado por AWS.
    - **CloudWatch:** Monitorear las métricas y definir si se escala verticalmente (Si se aumenta o reduce el tamaño de la máquina virtual) desde la interfaz de AWS dependiendo del uso
2. **Uso general, tráfico inestable:** Para facilidad y uniformidad propongo un cluster `kubernetes` en donde el balanceo de cargas, provisionamiento de imagenes, **escalamiento horizontal** sea administrado por el mismo cluster:
    - **EKS (Modo Autopilot):** Servicio de `kubernetes` administrado por AWS en modo autopilot para asegurar que una vez se alcance umbrales de uso, el cluster escale creando más `pods` disponibles y los provisione con la imagen `Docker`.
    - **RDS:** Base de datos relacional administrada por AWS.
    - **ELK (Elasticsearch, Logstash, Kibana):** Servidor de logs con este stack para redirigir todos los logs de multiples `pods` bajo las mismas métricas e interfaz de `kibana`.

## Desplegar aplicación con Docker
Correr la aplicación desde un docker es más fácil puesto que ya trae la base de datos con registros precargados y un usuario **superadmin**, la imagen corre un servidor `gunicorn` usado en ambientes productivos

1. Hacer pull de la imagen desde el repositorio público
    ```sh
    docker pull cristianpardoluna/its-solutions-challenge:latest
    ```
1. Correr imagen Docker en puerto 8000 con nombre `challenge`. (Se puede ejecutar sólo este comando y descargará la imagen desde el repositorio público automáticamente)
    ```sh
    sudo docker run --name challenge -p 8000:8000 cristianpardoluna/its-solutions-challenge:latest
    ```
1. Ingresar a la interfaz de administrador en `http://127.0.0.1:8000/admin` e ingresar las credenciales
    - **Username:** admin
    - **Password:** 12345

## Desplegar aplicación desde ambiente local de desarrollo
Desplegar desde el repositorio en modo DEBUG require crear el ambiente, correr las migraciones y crear un usuario **superadmin** como se describe acá

1. Clonar este repositorio localmente y abrir una terminal desde el folder raíz
1. Crear una carpeta llamada `.venv` con el ambiente local de desarrollo
    ```sh
    python3 -m venv .venv
    ```
1. Activar el ambiente virtual
    ```sh
    source .venv/bin/activate
    ```
1. Instalar las dependencias en el ambiente virtual
    ```sh
    pip install -r requirements.txt
    ```
1. Correr las migraciones para crear el esquema localmente
    ```sh
    python3 manage.py migrate
    ```
1. Crear el usuario **superadmin** (requiere ingresar los datos en una consola interactiva)
    ```sh
    python3 manage.py createsuperuser
    ```
1. Correr el servidor de desarrollo (corre por defecto en el puerto `8000`)
    ```sh
    python3 manage.py runserver
    ```
1. Visitar la interfaz administrativa en `http://127.0.0.1:8000/admin` e ingresar con el usuario recién creado
1. Correr casos de prueba
    ```sh
    python3 manage.py test
    ```