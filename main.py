import pandas as pd
import mysql.connector
from mysql.connector import Error

# 1. Leer el archivo Excel y anular las columnas 'City' y 'Country'
df = pd.read_excel('data1.xlsx', sheet_name='Data')
df = df.drop(columns=['City', 'Country'])

# Reemplazar valores nulos (NaN) por None para evitar errores en MySQL
df = df.where(pd.notnull(df), None)

filas = df.values.tolist()

connection = None
try:
    # 2. Conexión a la base de datos solicitada: mi_db_1 (XAMPP sin contraseña)
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        db='mi_db_1'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # 3. Carga masiva de las 10 columnas restantes
        sql_insert = """INSERT INTO empleados (
            Employee_ID,
            Full_Name,
            Job_Title,
            Department,
            Business_Unit,
            Gender,
            Ethnicity,
            Age,
            Annual_Salary,
            Bonus
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.executemany(sql_insert, filas)

        if len(filas) == cursor.rowcount:
            connection.commit()
            print(f"{len(filas)} filas insertadas correctamente en mi_db_1.")
        else:
            connection.rollback()
            print("No se insertaron todos los registros. Se ejecutó rollback.")

        # 4. Manipulación de la base de datos con sentencias SQL desde Python
        # A) Consulta SELECT
        cursor.execute("SELECT Employee_ID, Full_Name, Job_Title, Annual_Salary FROM empleados WHERE Department = 'IT' LIMIT 5")
        print("\n--- Empleados del departamento IT ---")
        for emp in cursor.fetchall():
            print(emp)

        # B) Actualización UPDATE
        cursor.execute("UPDATE empleados SET Bonus = Bonus + 0.01 WHERE Age > 50")
        connection.commit()
        print(f"\nRegistros actualizados (UPDATE): {cursor.rowcount}")

        # C) Eliminación DELETE
        cursor.execute("DELETE FROM empleados WHERE Annual_Salary <= 0")
        connection.commit()
        print(f"Registros eliminados (DELETE): {cursor.rowcount}")

except Error as ex:
    print(f"Error en la conexión o ejecución SQL: {ex}")
finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("\nConexión cerrada.")