from mysql.connector import Error
import mysql.connector
import openpyxl

archivo_excel = openpyxl.load_workbook('data1.xlsx')
hoja_excel = archivo_excel.active
filas = []

# Saltamos los encabezados (min_row=2) y anulamos las columnas 'Country' (10) y 'City' (11)
for fila in hoja_excel.iter_rows(min_row=2, values_only=True):
    fila_sin_ubicacion = fila[:10]
    filas.append(fila_sin_ubicacion)

print("Ejemplo de registro sin City ni Country:", filas[2])
print("Total de registros procesados:", len(filas))
