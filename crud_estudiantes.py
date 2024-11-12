# Creare el CRUD de la forma mas organizada y legible posible

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# creare la base de datos SQLITE primero para su conexion y luego sus tablas
def crear_base_datos():
    conexion = sqlite3.connect("estudiantes.db")
    cursor = conexion.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS estudiantes (
                        id TEXT PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        edad INTEGER NOT NULL,
                        salon TEXT NOT NULL)""")
    conexion.commit()
    conexion.close()

# Agregar un estudiante a la base de datos
def agregar_estudiante_db(id_estudiante, nombre, edad, salon):
    conexion = sqlite3.connect("estudiantes.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO estudiantes (id, nombre, edad, salon) VALUES (?, ?, ?, ?)", 
                       (id_estudiante, nombre, edad, salon))
        conexion.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conexion.close()
ventana = tk.Tk()
ventana.title("CRUD PARA INSTITUCIONES EDUCATIVAS")
ventana.geometry("500x250")
ventana.config(bg="#003366")

nombre_var = tk.StringVar()
edad_var = tk.StringVar()
id_var = tk.StringVar()
salon_var = tk.StringVar()

fuente_estetica = ("Dosis ExtraBold", 12)
fuente_titulo = ("Dosis ExtraBold", 12, "bold")

frame_campos = tk.Frame(ventana, bg="#003366")
frame_campos.pack(pady=10)

tk.Label(frame_campos, text="Documento del Estudiante", bg="#003366", fg="white", font=fuente_titulo).grid(row=0, column=0, padx=5, pady=5, sticky='w')
tk.Entry(frame_campos, textvariable=id_var, font=("Dosis ExtraBold", 10)).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_campos, text="Nombre del Estudiante", bg="#003366", fg="white", font=fuente_titulo).grid(row=1, column=0, padx=5, pady=5, sticky='w')
tk.Entry(frame_campos, textvariable=nombre_var, font=("Dosis ExtraBold", 10)).grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_campos, text="Edad del Estudiante", bg="#003366", fg="white", font=fuente_titulo).grid(row=2, column=0, padx=5, pady=5, sticky='w')
tk.Entry(frame_campos, textvariable=edad_var, font=("Dosis ExtraBold", 10)).grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_campos, text="Salón del Estudiante", bg="#003366", fg="white", font=fuente_titulo).grid(row=3, column=0, padx=5, pady=5, sticky='w')
tk.Entry(frame_campos, textvariable=salon_var, font=("Dosis ExtraBold", 10)).grid(row=3, column=1, padx=5, pady=5)

# Creare la base de datos
crear_base_datos()

def validar_nombre(nombre):
    return all(x.isalpha() or x.isspace() for x in nombre)

def validar_id(id_estudiante):
    return id_estudiante.isdigit()

def agregar_estudiante():
    id_estudiante = id_var.get()
    nombre = nombre_var.get()
    edad = edad_var.get()
    salon = salon_var.get()

    if not validar_id(id_estudiante):
        messagebox.showerror("Error", "Documento del estudiante debe contener solo números.")
        return
    if not validar_nombre(nombre):
        messagebox.showerror("Error", "El nombre solo debe contener letras y espacios.")
        return
    if not edad.isdigit() or int(edad) <= 0:
        messagebox.showerror("Error", "La edad debe ser un número positivo.")
        return

    if id_estudiante and nombre and edad and salon:
        if agregar_estudiante_db(id_estudiante, nombre, edad, salon):
            messagebox.showinfo("Excelente", "Estudiante agregado al sistema")
            id_var.set("")
            nombre_var.set("")
            edad_var.set("")
            salon_var.set("")
        else:
            messagebox.showerror("Error", "El documento ya está registrado.")
    else:
        messagebox.showwarning("Error", "Debes llenar todos los campos")

# A continuacion creare para poder actualizar el estudiante en la base de datos
def actualizar_estudiante_db(id_estudiante, nuevo_id, nombre, edad, salon, ventana_actualizar):
    conexion = sqlite3.connect("estudiantes.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE estudiantes SET id=?, nombre=?, edad=?, salon=? WHERE id=?", 
                   (nuevo_id, nombre, edad, salon, id_estudiante))
    conexion.commit()
    conexion.close()
    messagebox.showinfo("Éxito", "Estudiante actualizado con éxito")
    ventana_actualizar.destroy()
    actualizar_tabla(ventana_estudiantes.children['!treeview'])

frame_botones = tk.Frame(ventana, bg="#003366")
frame_botones.pack(pady=10)

# Se crean los botones para agregar estudiante y ver estudiantes desde la interfaz ventana principal
tk.Button(frame_botones, text="Agregar Estudiante", command=agregar_estudiante, bg="#00796b", fg="white", font=fuente_estetica).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Ver Estudiantes", command=lambda: mostrar_estudiantes(), bg="#00796b", fg="white", font=fuente_estetica).pack(side=tk.LEFT, padx=5)

ventana_estudiantes = None

# Se codifica para mostrar estudiantes en una tabla
def mostrar_estudiantes():
    global ventana_estudiantes
    ventana.withdraw()
    if ventana_estudiantes is None or not ventana_estudiantes.winfo_exists():
        ventana_estudiantes = tk.Toplevel(ventana)
        ventana_estudiantes.title("Lista de Estudiantes")
        ventana_estudiantes.geometry("650x400")
        ventana_estudiantes.config(bg="#003366")

        columnas = ("Documento Estudiante", "Nombre", "Edad", "Salón")
        tabla = ttk.Treeview(ventana_estudiantes, columns=columnas, show='headings')

        for col in columnas:
            tabla.heading(col, text=col, anchor=tk.CENTER)
            tabla.column(col, anchor=tk.CENTER, width=150)

        tabla.pack(fill=tk.BOTH, expand=True)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview.Heading", font=("Dosis ExtraBold", 10, "bold"), 
                         background="#005580", foreground="#FFDD44", relief="raised")
        estilo.configure("Treeview", rowheight=25, background="#003366", foreground="white")

        actualizar_tabla(tabla)

        tk.Button(ventana_estudiantes, text="Actualizar Estudiante", command=lambda: actualizar_estudiante(tabla), bg="#00796b", fg="white", font=fuente_estetica).pack(pady=5)
        tk.Button(ventana_estudiantes, text="Eliminar Estudiante", command=lambda: eliminar_estudiante(tabla), bg="#d32f2f", fg="white", font=fuente_estetica).pack(pady=5)

        ventana_estudiantes.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_estudiantes(ventana_estudiantes))
    else:
        ventana_estudiantes.lift()

def cerrar_ventana_estudiantes(ventana_estudiantes):
    ventana_estudiantes.destroy()
    ventana.deiconify()

# A continuacion se crea la parte importante del CRUD y es el poder Actualizar la tabla de estudiantes
def actualizar_tabla(tabla):
    for item in tabla.get_children():
        tabla.delete(item)
    
    conexion = sqlite3.connect("estudiantes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    for estudiante in cursor.fetchall():
        tabla.insert("", tk.END, values=estudiante)
    conexion.close()

# Actualizar estudiante
def actualizar_estudiante(tabla):
    seleccion = tabla.selection()
    if seleccion:
        seleccionado = tabla.item(seleccion, 'values')
        id_estudiante = seleccionado[0]
        nombre_actual = seleccionado[1]
        edad_actual = seleccionado[2]
        salon_actual = seleccionado[3]

        ventana_actualizar = tk.Toplevel(ventana)
        ventana_actualizar.title("Actualizar Estudiante")
        ventana_actualizar.geometry("400x350")
        ventana_actualizar.config(bg="#003366")

        nuevo_id_var = tk.StringVar(value=id_estudiante)
        nuevo_nombre_var = tk.StringVar(value=nombre_actual)
        nueva_edad_var = tk.StringVar(value=edad_actual)
        nuevo_salon_var = tk.StringVar(value=salon_actual)

        tk.Label(ventana_actualizar, text="Actualizar Documento del Estudiante", bg="#003366", fg="white", font=fuente_titulo).pack(pady=5)
        tk.Entry(ventana_actualizar, textvariable=nuevo_id_var, font=("Dosis ExtraBold", 10)).pack(pady=5)

        tk.Label(ventana_actualizar, text="Actualizar Nombre del Estudiante", bg="#003366", fg="white", font=fuente_titulo).pack(pady=5)
        tk.Entry(ventana_actualizar, textvariable=nuevo_nombre_var, font=("Dosis ExtraBold", 10)).pack(pady=5)

        tk.Label(ventana_actualizar, text="Actualizar Edad del Estudiante", bg="#003366", fg="white", font=fuente_titulo).pack(pady=5)
        tk.Entry(ventana_actualizar, textvariable=nueva_edad_var, font=("Dosis ExtraBold", 10)).pack(pady=5)

        tk.Label(ventana_actualizar, text="Actualizar Salón del Estudiante", bg="#003366", fg="white", font=fuente_titulo).pack(pady=5)
        tk.Entry(ventana_actualizar, textvariable=nuevo_salon_var, font=("Dosis ExtraBold", 10)).pack(pady=5)

        tk.Button(ventana_actualizar, text="Actualizar Estudiante", command=lambda: confirmar_actualizacion(id_estudiante, nuevo_id_var, nuevo_nombre_var, nueva_edad_var, nuevo_salon_var, ventana_actualizar), bg="#00796b", fg="white", font=fuente_estetica).pack(pady=10)

def confirmar_actualizacion(id_estudiante, nuevo_id_var, nuevo_nombre_var, nueva_edad_var, nuevo_salon_var, ventana_actualizar):
    nuevo_id = nuevo_id_var.get()
    nuevo_nombre = nuevo_nombre_var.get()
    nueva_edad = nueva_edad_var.get()
    nuevo_salon = nuevo_salon_var.get()

    if not validar_id(nuevo_id):
        messagebox.showerror("Error", "Documento del estudiante debe contener solo números.")
        return
    if not validar_nombre(nuevo_nombre):
        messagebox.showerror("Error", "El nombre solo debe contener letras y espacios.")
        return
    if not nueva_edad.isdigit() or int(nueva_edad) <= 0:
        messagebox.showerror("Error", "La edad debe ser un número positivo.")
        return

    if nuevo_id and nuevo_nombre and nueva_edad and nuevo_salon:
        actualizar_estudiante_db(id_estudiante, nuevo_id, nuevo_nombre, nueva_edad, nuevo_salon, ventana_actualizar)
    else:
        messagebox.showwarning("Error", "Debes llenar todos los campos")
# Aqui se creara para poder eliminar el estudiante de la base de datos
def eliminar_estudiante_db(id_estudiante):
    conexion = sqlite3.connect("estudiantes.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM estudiantes WHERE id=?", (id_estudiante,))
    conexion.commit()
    conexion.close()
# Aqui se elimina desde la tabla
def eliminar_estudiante(tabla):
    seleccion = tabla.selection()
    if seleccion:
        seleccionado = tabla.item(seleccion, 'values')
        id_estudiante = seleccionado[0]

        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que deseas eliminar al estudiante con documento {id_estudiante}?")
        if confirmar:
            eliminar_estudiante_db(id_estudiante)
            messagebox.showinfo("Éxito", "Estudiante eliminado con éxito")
            actualizar_tabla(tabla)
    else:
        messagebox.showwarning("Advertencia", "Por favor selecciona un estudiante")

ventana.mainloop()

#Aqui termina toda la codificacion de todo el CRUD