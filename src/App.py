from flask import Flask, render_template, request, redirect, url_for, flash
from DataBase import DataBase
from DB_data import DB_data

bd = DataBase()
db_data = DB_data()

app = Flask(__name__)
app.secret_key = "mysecretkey"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index-table/<schema>/<table>', methods = ['GET', 'POST'])
def index_table(schema, table):
    if request.method == 'GET':
        data_table = db_data.get_table(table)
    elif request.method == 'POST':
        data = request.form['data']
        field = request.form['field']
        try:
            data_table = db_data.get_table_rows(table, field, data)
            if not data_table['data']:
                flash(f"ERROR: {table.capitalize().replace('_', ' ')} ({field.capitalize()}: {data}) Registro inexistente")
                return redirect(f"/index-table/{data_table['schema']}/{data_table['name']}")
        except:
            bd.execute_query('rollback')
            flash(f"ERROR: Error producido en la busqueda")
            data_table = db_data.get_info(table)
            return redirect(f"/index-table/{data_table['schema']}/{data_table['name']}")
    return render_template('index_table.html', table = data_table)


#INSERTS
@app.route('/index_register_form/<table_name>', methods = ['GET'])
def index_register_form(table_name):
    return render_template('index_register_form.html',
                            table = db_data.get_table(table_name),
                            data_select = db_data.get_data_select(table_name))

@app.route('/insert_register/<schema>/<table_name>', methods = ['POST'])
def insert_register(schema, table_name):
    form_data = get_form_data(table_name, 'insert')
    bd.insert_reg(db_data.get_info(table_name), form_data)
    flash(bd.get_message())
    if table_name == 'persona':
        try:
            return redirect(f"/index_register_form/persona_{request.form['tipo_persona']}")
        except:
            pass
    return redirect(f"/index-table/{schema}/{table_name}")
    

# UPDATES
@app.route('/index_update_form/<table_name>/<data>', methods = ['GET'])
def index_update_form(table_name, data):
    table = db_data.get_table_with_spec_row(table_name, data)
    return render_template('index_update_form.html',
                            table = table,
                            data_select = db_data.get_data_select(table_name),
                            default_values = table['spec_row'][0],
                            data = data)

@app.route('/update_register/<schema>/<table_name>/<data>', methods = ['POST'])
def update_register(schema, table_name, data):
    form_data = tuple([data]) + get_form_data(table_name, 'update')
    bd.update_reg(db_data.get_info(table_name), form_data)
    flash(bd.get_message())
    return redirect(f"/index-table/{schema}/{table_name}")

# DELETE
@app.route("/delete/<schema>/<table>/<field>/<reg>")
def delete(schema, table, field, reg):
    bd.delete_reg(db_data.get_info(table), tuple([reg]))
    flash(bd.get_message())
    return redirect(f"/index-table/{schema}/{table}")

def get_form_data(table_name, operation):
    data = []
    table_info = db_data.get_info(table_name)
    for field in bd.select_fields_names(table_info['schema'], table_info['name']):
        if (operation == 'update' and field[0] != table_info['index']) or (operation == 'insert' and (field[0] != 'id' or table_name == 'empleados' or table_name == 'piloto')):
            data.append(request.form[field[0]])
    return tuple(data)

if __name__ == '__main__':
    app.run(port=3000, debug=True)