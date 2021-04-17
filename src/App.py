from flask import Flask, render_template, request, redirect, url_for, flash
from DataBase import DataBase

bd = DataBase()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hangar/')
def hangares():
    data = bd.select_all("eq.clase_hangar order by num_hangar")
    return render_template('body_data_table.html', table = data, direction = "hangar.html")

@app.route('/persona')
def personas():
    data = bd.select_all("per.persona order by id")
    return render_template('body_data_table.html', table = data, direction = "persona.html")

@app.route('/corporacion')
def corporacion():
    data = bd.select_all("prop.corporacion")
    return render_template('body_data_table.html', table = data, direction = "corporacion.html")

@app.route('/tipo-avion')
def tipo_avion():
    data = bd.select_all("eq.tipo_avion order by id")
    return render_template('body_data_table.html', table = data, direction = "tipo_avion.html")

@app.route("/empleados")
def empleados():
    data = bd.select_all("per.empleados order by id")
    data_select = bd.select_fields('tipo_servicio', 'per.servicio')
    return render_template('body_data_table.html', table = data, table_select = data_select, direction = "empleado.html")

@app.route("/piloto")
def piloto():
    data = bd.select_all("eq.piloto order by id")
    return render_template('body_data_table.html',table = data, direction = "piloto.html")

@app.route("/avion")
def avion():
    data = bd.select_all("eq.avion")
    data_num_hangar = bd.select_fields("num_hangar", "eq.clase_hangar order by num_hangar")
    data_piloto = bd.execute_query_returning_table("""select pi.num_lic, pe.nombre from eq.piloto pi
                                                    inner join per.persona pe on pi.id = pe.id""")
    data_corporacion = bd.select_fields("nombre", "prop.corporacion")
    data_tipo_avion = bd.select_fields("id, modelo", "eq.tipo_avion order by tipo_avion")
    return render_template('body_data_table.html', 
                            table = data,
                            table_num_hangar = data_num_hangar,
                            table_piloto = data_piloto,
                            table_corporacion = data_corporacion,
                            table_tipo_avion = data_tipo_avion,
                            direction = "avion.html")

# INSERT CLASE_HANGAR
@app.route("/add-hangar", methods = ['POST'])
def add_hangar():
    num_hangar = request.form['num_hangar']
    capacidad = request.form['capacidad']
    reg = bd.select_row("eq.clase_hangar", f"num_hangar = {num_hangar}")
    if len(reg) == 0:
        # query = f"""insert into eq.clase_hangar
        #             values({num_hangar}, {capacidad})"""
        # bd.execute_query(query)
        bd.insert_clase_hangar(capacidad)
    return redirect(url_for("hangares"))

#INSERT PERSONA
@app.route("/add-persona", methods = ['POST'])
def add_persona():
    nss = request.form['nss']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    try:
        tipo_persona = request.form['tipo_persona']
    except:
        tipo_persona = 'persona'
    print(nss, nombre, telefono, tipo_persona)
    # query = f"""insert into per.persona (nss, nombre, telefono)
    #             values({nss}, '{nombre}', {telefono})"""
    # bd.execute_query(query)
    # bd.insert_persona(nss, nombre, telefono)
    if tipo_persona == 'empleado':
        return redirect(url_for("empleados"))
    elif tipo_persona == 'piloto':
        return redirect(url_for("piloto"))
    return redirect(url_for("personas"))

#INSERT EMPLEADO
@app.route("/add-empleado", methods = ['POST'])
def add_empleado():
    salario = request.form['salario']
    turno = request.form['turno']
    tipo_servicio = request.form['tipo_servicio']
    print(salario, turno, tipo_servicio)
    return redirect(url_for("empleados"))

#INSERT PILOTO
@app.route("/add-piloto", methods = ['POST'])
def add_piloto():
    num_lic = request.form['num_lic']
    print(num_lic)
    return redirect(url_for("piloto"))

#INSERT CORPORACION
@app.route("/add-corporacion", methods = ['POST'])
def add_corporacion():
    nombre = request.form['nombre_corporacion']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    reg = bd.select_row("prop.corporacion", f"nombre = '{nombre}'")
    if len(reg) == 0:
        # query = f"""insert into prop.corporacion(nombre, direccion, telefono)
        #             values('{nombre}', '{direccion}', {telefono})"""
        # bd.execute_query(query)
        bd.insert_corporacion(nombre, direccion, telefono)
    return redirect(url_for("corporacion"))

#INSERT AVION
@app.route("/add-avion", methods = ['POST'])
def add_avion():
    matricula = request.form['matricula']
    num_hangar = request.form['num_hangar']
    piloto = request.form['piloto']
    corporacion = request.form['corporacion']
    tipo_avion = request.form['tipo_avion']
    print(matricula, num_hangar, piloto, corporacion, tipo_avion)
    return redirect(url_for("avion"))

#INSERT TIPO_AVION
@app.route("/add-tipo-avion", methods = ['POST'])
def add_tipo_avion():
    modelo = request.form['modelo']
    capacidad = request.form['capacidad']
    peso = request.form['peso']
    # query = f"""insert into eq.tipo_avion(modelo, capacidad, peso_avion)
    #             values('{modelo}', {capacidad}, {peso})"""
    # bd.execute_query(query)
    bd.insert_tipo_avion(modelo, capacidad, peso)
    return redirect(url_for('tipo_avion'))

# UPDATE CLASE_HANGAR
@app.route("/form-clase-hangar", methods = ['POST'])
def form_update_clase_hangar():
    num_hangar = request.form['num_hangar_update']
    data = bd.select_row("eq.clase_hangar", f"num_hangar = {num_hangar}")
    try:
        return render_template('body_data_table.html', table = data, direction = "updates/clase_hangar.html")
    except:
        return redirect(url_for("hangares"))

@app.route("/update-clase-hangar/<num_hangar>", methods = ['POST'])
def update_clase_hangar(num_hangar):
    capacidad = request.form['capacidad']
    # query = f"update eq.clase_hangar set capacidad = {capacidad} where num_hangar = {num_hangar}"
    # bd.execute_query(query)
    bd.update_clase_hangar(num_hangar, capacidad)
    print(num_hangar, capacidad)
    return redirect(url_for("hangares"))

# UPDATE CORPORACION
@app.route("/form-corporacion", methods = ['POST'])
def form_update_corporacion():
    nombre = request.form['nombre_update']
    data = bd.select_row("prop.corporacion", f"nombre = '{nombre}'")
    try:
        return render_template('body_data_table.html', table = data, direction = "updates/corporacion.html")
    except:
        return redirect(url_for('corporacion'))

@app.route("/update-corporacion/<nombre>", methods = ['POST'])
def update_corporacion(nombre):
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    print(nombre, direccion, telefono)
    # query = f"update prop.corporacion set direccion = '{direccion}', telefono = {telefono} where nombre = '{nombre}'"
    # bd.execute_query(query)
    bd.update_corporacion(nombre, direccion, telefono)
    return redirect(url_for("corporacion"))

# UPDATE PERSONA
@app.route("/form-persona", methods = ['POST'])
def form_update_persona():
    id = request.form['id_update']
    data = bd.select_row("per.persona", f"id = {id}")
    try:
        return render_template('body_data_table.html', table = data, direction = "updates/persona.html")
    except:
        redirect(url_for('personas'))

@app.route("/update-persona/<id>", methods = ['POST'])
def update_persona(id):
    nss = request.form['nss']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    # query = f"update per.persona set nss = '{nss}', nombre = '{nombre}', telefono = {telefono} where id = {id}"
    # bd.execute_query(query)
    bd.update_persona(id, nss, nombre, telefono)
    return redirect(url_for("personas"))

# UPDATE TIPO_AVION
@app.route("/form-tipo-avion", methods = ['POST'])
def form_update_tipo_avion():
    id = request.form['id_update']
    data = bd.select_row("eq.tipo_avion", f"id = {id}")
    try:
        return render_template('body_data_table.html', table = data, direction = "updates/tipo_avion.html")
    except:
        return redirect(url_for('tipo_avion'))

@app.route("/update-tipo-avion/<id>", methods = ['POST'])
def update_tipo_avion(id):
    modelo = request.form['modelo']
    capacidad = request.form['capacidad']
    peso = request.form['peso']
    # query = f"update eq.tipo_avion set modelo = '{modelo}', capacidad = {capacidad}, peso_avion = {peso} where id = {id}"
    # bd.execute_query(query)
    bd.update_tipo_avion(id, modelo, capacidad, peso)
    return redirect(url_for("tipo_avion"))

# DELETE ROW
@app.route('/delete_row/<table>/<field>/<data>/<url>')
def delete_row(table, field, data, url):
    print(table, field, data, url)
    print(table, f"{field} = '{data}'")
    bd.delete_row(table, f"{field} = '{data}'")
    return redirect(url_for(url))

if __name__ == '__main__':
    app.run(port=3000, debug=True)