# Datos de COVID-19 en España

![Datos actualizados](https://img.shields.io/github/last-commit/alex-torregrosa/covid-spain?label=Actualizado)

Datos de la pandemia en España, actualizados automáticamente.

> :warning: **Actualmente solo se descargan datos de muertes para Catalunya, en el resto de comunidades el número mostrado es erroneo.**

## Formato

Los datos están disponibles en la carpeta `datos` en formato `.csv`. Estos son los distintos archivos:

| Nombre                   | Descripción             |
| ------------------------ | ----------------------- |
| `datos_estatales.csv`    | Datos de toda España    |
| `comunidades/[ccaa].csv` | Datos de cada comunidad |

Cada fila consiste en los datos de contagios, muertes y vacunados ese día, distribuidos en las siguientes columnas:

| Campo         | Descripción                            |
| ------------- | -------------------------------------- |
| `fecha`       | Fecha en formato `AAAA-MM-DD`          |
| `casos`       | Casos detectados (PCR y TAR)           |
| `TAR`         | Casos detectados por test de antígenos |
| `muertes`     | Muertes **[SOLO EN CATALUNYA]**        |
| `vacunados_1` | Vacunados primera dosis                |
| `vacunados_2` | Vacunados dosis completa               |

## Fuentes

- Numero de casos diarios (PCR y TAR): [Centro Nacional de Epidemiología](https://cnecovid.isciii.es/covid19/#documentaci%C3%B3n-y-datos)
- Número de vacunados: [Vacunación COVID-19](https://github.com/midudev/covid-vacuna) (_Recopila datos del [Ministerio de Sanidad](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/vacunaCovid19.htm)_)
- Datos Catalunya: [Dades Covid](https://dadescovid.cat/) (Departament de Salut)
