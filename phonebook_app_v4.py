from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask, render_template, request, redirect
import pg
import os

db = pg.DB(
    dbname=os.environ.get('PG_DBNAME'),
    host=os.environ.get('PG_HOST'),
    user=os.environ.get('PG_USERNAME'),
    passwd=os.environ.get('PG_PASSWORD')
)
tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('phonebook', template_folder=tmp_dir)


@app.route('/')
def main():
    query = db.query('select * from phonebook order by name')

    return render_template(
        'list_entries.html',
        title='Entries',
        entry_list=query.namedresult()
    )


@app.route('/add_entry')
def new_entry():
    return render_template(
        'add_entry.html',
        title='Add Entry'
    )


@app.route('/update_entry')
def update_entry():
    entry_id = request.args.get('id')
    query = db.query("select * from phonebook where id = '%s'" % entry_id)

    return render_template(
        'update_entry.html',
        title='Update Entry',
        entry_list=query.namedresult()
    )


@app.route('/edit_entry', methods=['POST'])
def edit_entry():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    entry_id = request.form.get('id')
    action = request.form.get('action')
    if action == 'edit':
        db.update(
            'phonebook',
            # id=entry_id,
            # name=name,
            # phone_number=phone_number,
            # email=email
            {
                'id': entry_id,
                'name': name,
                'phone_number': phone_number,
                'email': email
            }
        )
    elif action == 'delete':
        db.delete(
            'phonebook',
            id=entry_id
        )
    return redirect('/')


# @app.route('/delete_entry')
# def delete_entry():
#     entry_id = request.args.get('id')
#     db.delete(
#         'phonebook',
#         id=entry_id
#     )
#     return redirect('/')


@app.route('/submit_new_entry', methods=['POST'])
def add_entry():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    db.insert(
        'phonebook',
        name=name,
        phone_number=phone_number,
        email=email
    )
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
