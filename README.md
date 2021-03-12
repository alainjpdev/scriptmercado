# README


## Requerimientos

    - Python >= 3.5 
## Instrucciónes de uso


- Crear una app: http://applications.mercadolibre.com/
- Copiar el app id y secret key
- Crear usuarios de test: https://www.mercadopago.com.ar/developers/en/solutions/payments/basic-checkout/test/test-users/
- Identificarse con el usuario y contraseña de test: https://www.mercadolibre.com
- Copiar el client id y el access token
- Dar acceso a la app al usuario: https://developers.mercadolibre.com/authentication-and-authorization/

    - En este punto es necesario obtener el **SERVER_GENERATED_AUTHORIZATION_CODE** para la primera ejecución del programa, el mismo aparece luego de realizar el paso número 3 de https://developers.mercadolibre.com.mx/es_ar/autenticacion-y-autorizacion/#Autenticaci%C3%B3n

    ![Drag Racing](https://http2.mlstatic.com/storage/developers-site-cms-admin/DevSite/335687742731-code-resaltado.png)

    - Deberá copiarse este código y pegarlo en el archivo **client_code.txt** que se debe ubicar en la misma carpeta que el archivo `main.py`. El contenido del archivo deberá quedar como sigue.
    ```
    TG-5eb03c9705e80800061c2820-549818682
    ```

    - Obtener este código es necesario para obtener el **REFRESH_TOKEN" para que cada vez que se ejecute el script se renueve el token de acceso.


- Definir en código las variables necesarias para la ejecución:
    ```
    APP_ID = 7629182635292394
    APP_SECRET = 'zGtGw7UsQkK8boIcU9eBqv4CBZb9zKwL'
    CLIENT_ID = 549818682
    CSV_FILE = 'DEMO-matriz-MONTH-YEAR.csv'
    LAST_DATE_CLOSED_FILE = 'last_date_closed.txt'
    CLIENT_ACCESS_TOKEN_FILE = 'access_token_ARMANDO.txt'
    REFRESH_TOKEN_FILE = 'refresh_token.txt'
    CLIENT_CODE_FILE = 'client_code.txt'
    REDIRECT_URI = 'https://localhost'
    ```

    - REDIRECT_URI se utiliza para la generación automática del token en cada ejecución a partir del REFRESH_TOKEN, **debe coincidir con la configurada en la app en mercadolibre (Redirect URI *)** https://developers.mercadolibre.com.mx/devcenter/edit-app/<APP_ID>


- Instalar dependencias (es necesario tener pip instalado)

    - pip install -r requirements.txt

- Ejecutar archivo `main.py`

    - python main.py

    *Este archivo ejecutara todo el script una vez y luego (si no se detiene la ejecución lo hará cada TIME_DELTA_TEST segundos)*

    *Se puede editar el tiempo cada cuanto se ejecutara la funcion principal editando la variable `TIME_DELTA_TEST` colocando los segundos que deben pasar hasta que se ejecute nuevamente*
