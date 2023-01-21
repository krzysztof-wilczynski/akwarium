## Environment variables

| Name                | Default                | Description                                                                         |
|---------------------|------------------------|-------------------------------------------------------------------------------------|
| AQUA_SECRET_KEY     | 'rybka-lubi-plywac'    | Django secret key - **remember not to use default one in a production environment** |
| AQUA_ALLOWED_HOSTS  | 'localhost, 127.0.0.1' | Host (addresses) that can be used to access app separated by comma                  |
| AQUA_DEBUG          | False                  | Boolean asking if app should be running in debug mode                               |
| AQUA_MYSQL_HOST     | '127.0.0.1'            | MySQL DB host                                                                       |
| AQUA_MYSQL_USER     | 'root'                 | MySQL DB username                                                                   |
| AQUA_MYSQL_PASSWORD | 'rootpass'             | MySQL DB password                                                                   |
| AQUA_MYSQL_DB       | 'aquarium'             | MySQL database name                                                                 |
| AQUA_MYSQL_PORT     | '3306'                 | MySQL port                                                                          |
| AQUA_LOGFILE        | 'log/aquarium.log'     | Directory used to store log files                                                   |
| TZ                  | 'Europe/Warsaw'        | ENV for Docker container setting its timezone to Europe/Warsaw                      |

## Raspberry configuration

| Pin number | Usage                          | Channel |
|:----------:|--------------------------------|:-------:|
|     4      | Ogniwo Peltiera - załączenie   |    1    |
|     5      | Ogniwo - chłodzenie            |    4    |
|     6      | Pompa                          |    5    |
|     16     | Nawilżacz                      |    8    |
|     20     | Ogniwo - ogrzewanie            |    3    |
|     21     | Wywiew - obniżanie wilgotności |   2.1   |
|     22     | Czujnik temperatury 1          |    -    |
|     23     | Dolny wiatrak 5V               |    6    |
|     24     | Górny wiatrak                  |    7    |
|     26     | Czujnik temperatury 2          |    -    |
|     27     | Żarówka                        |    2    |
