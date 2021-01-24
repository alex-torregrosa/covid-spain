import csv
import json
from os import path as p
from os import system 
from os import listdir

comunidades_iso = {
    "AN":	"andalucia",
    "AR":	"aragon",
    "AS":	"asturias",
    "CN":	"canarias",
    "CB":	"cantabria",
    "CM":	"castilla_la_mancha",
    "CL":	"castilla_y_leon",
    "CT":	"catalunya",
    "EX":	"extremadura",
    "GA":	"galicia",
    "IB":	"illes_balears",
    "RI":	"la_rioja",
    "MD":	"madrid",
    "MC":	"murcia",
    "NC":	"navarra",
    "PV":	"pais_vasco",
    "VC":	"comunidad_valenciana",
    "CE":       "ceuta",
    "ML":       "melilla"
}
reverse_iso_vacunas = {
    "Andalucía":            "AN",
    "Aragón":               "AR",
    "Asturias":             "AS",
    "Baleares":             "IB",
    "Canarias":             "CN",
    "Cantabria":            "CB",
    "Castilla y Leon":      "CL",
    "Castilla La Mancha":   "CM",
    "Cataluña":             "CT",
    "C. Valenciana":        "VC",
    "Extremadura":          "EX",
    "Galicia":              "GA",
    "La Rioja":             "RI",
    "Madrid":               "MD",
    "Murcia":               "MC",
    "Navarra":              "NC",
    "País Vasco":           "PV",
    "Ceuta":                "CE",
    "Melilla":              "ML"
}

tags = ["fecha", "casos", "TAR", "muertes", "vacunados_1", "vacunados_2"]

# Crear directorios de salida
out_dir = "datos"
out_dir_comun = p.join(out_dir, "comunidades")
data_glob_out = p.join(out_dir, "datos_estatales.csv")
system(f"mkdir -p {out_dir_comun}")
comunidades_out = {}

for ccaa in comunidades_iso:
    path = p.join(out_dir_comun, f"{comunidades_iso[ccaa]}.csv")
    comunidades_out[ccaa] = path

# Entrada de datos estatales
data_dir = "./tmp"
data_file =  p.join(data_dir, "spain.csv")

# Procesar datos estatales
esp_data = {}
for ccaa in comunidades_iso:
    esp_data[ccaa] = {}

print("Iniciando procesado de datos ESP")
with open(data_file) as csv_f:
    rd = csv.DictReader(csv_f, delimiter=',')
    for row in rd:
        # Comprobamos que existan todos los campos necesarios
        for kwd in ["ccaa_iso","fecha","num_casos","num_casos_prueba_ag"]:
                if kwd not in row:
                    print(f"Error: falta el atributo '{kwd}' en {data_file}")
                    exit(-1)
        ccaa = row["ccaa_iso"]
        my_date = row["fecha"]
        if my_date not in esp_data[ccaa]:
                esp_data[ccaa][my_date] = {"fecha": my_date, "casos": 0, "TAR":0, "muertes":0,"vacunados_1":0,"vacunados_2":0}
        esp_data[ccaa][my_date]["casos"]       += int(row["num_casos"])
        esp_data[ccaa][my_date]["TAR"]         += int(row["num_casos_prueba_ag"])
        #esp_data[ccaa][my_date]["muertes"]     += int(row["EXITUS"])
        #esp_data[ccaa][my_date]["vacunados_1"] += int(row["VACUNATS_DOSI_1"])
        #esp_data[ccaa][my_date]["vacunados_2"] += int(row["VACUNATS_DOSI_2"])


# Procesar datos de vacunación
dir_vacunas = p.join(data_dir, "vacunas")
datos_vacunas = listdir(dir_vacunas)
datos_vacunas.sort()
act_vacunados = {}
for ccaa in comunidades_iso:
    act_vacunados[ccaa] = 0;
for f in datos_vacunas:
    act_date = f[:-5]
    with open(p.join(dir_vacunas, f)) as fp:
        act_vac = json.load(fp)
        for ccaa in act_vac:
            if ccaa["ccaa"] == "Totales":
                continue
            ccaa_iso = reverse_iso_vacunas[ccaa["ccaa"]]
            if act_date in esp_data[ccaa_iso]:
                esp_data[ccaa_iso][act_date]["vacunados_1"] = ccaa["dosisAdministradas"] - act_vacunados[ccaa_iso]
                act_vacunados[ccaa_iso] = ccaa["dosisAdministradas"]
                if "dosisPautaCompletada" in ccaa:
                    esp_data[ccaa_iso][act_date]["vacunados_2"] = ccaa["dosisPautaCompletada"]



cat_file = p.join(data_dir, "catalunya_diari_total_pob.csv")
data_cat = {}

# Procesar datos de catalunya
print("Iniciando procesado de datos CAT")
with open(cat_file) as csv_f:
    rd = csv.DictReader(csv_f, delimiter=';')
    for row in rd:
        #print(row)
        for kwd in ["DATA", "CASOS_CONFIRMAT","CASOS_TAR","EXITUS","VACUNATS_DOSI_1","VACUNATS_DOSI_2"]:
            if kwd not in row:
                print(f"Error: falta el atributo '{kwd}' en {cat_file}")
                exit(-1)
        my_date = row["DATA"]
        if my_date not in data_cat:
            data_cat[my_date] = {"fecha": my_date, "casos": 0, "TAR":0, "muertes":0,"vacunados_1":0,"vacunados_2":0}

        data_cat[my_date]["casos"]       += int(row["CASOS_CONFIRMAT"])
        data_cat[my_date]["TAR"]         += int(row["CASOS_TAR"])
        data_cat[my_date]["muertes"]     += int(row["EXITUS"])
        data_cat[my_date]["vacunados_1"] += int(row["VACUNATS_DOSI_1"])
        data_cat[my_date]["vacunados_2"] += int(row["VACUNATS_DOSI_2"])

# Sobreescribir datos de Cataluña con los de la Generalitat
# Para días no disponibles en dadescvid.cat, se usan los datos del iscii
for date in data_cat:
    esp_data["CT"][date] = data_cat[date]

# Calculo de datos globales de España
datos_globales = {}
for ccaa in comunidades_iso:
    for dia in esp_data[ccaa]:
        if dia not in datos_globales:
            datos_globales[dia] = {"fecha": dia, "casos": 0, "TAR":0, "muertes":0,"vacunados_1":0,"vacunados_2":0}
        for attr in datos_globales[dia]:
            if attr != "fecha":
                datos_globales[dia][attr] += esp_data[ccaa][dia][attr]



# Escritura de datos
print("Escribiendo datos comunidades autonomas")
for ccaa in comunidades_iso:
    with open(comunidades_out[ccaa], "w") as f:
        w = csv.DictWriter(f, fieldnames=tags)
        w.writeheader()
        for date in esp_data[ccaa]:
            w.writerow(esp_data[ccaa][date])

print("Escribiendo datos estatales")
with open(data_glob_out, "w") as f:
    w = csv.DictWriter(f, fieldnames=tags)
    w.writeheader()
    for date in datos_globales:
        w.writerow(datos_globales[date])




print("Procesado de datos completado correctamente")

