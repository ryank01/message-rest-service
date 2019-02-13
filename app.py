from flask import Flask, jsonify, abort, make_response, request
from datetime import datetime
import sqlite3 as sql

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    '''handle 404 errors elegantly'''
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/sms-service/api/v1.0/messages', methods=['POST'])
def create_message():
    '''create a message and store it in the db'''
    if not request.json or not 'identifier' in request.json:
        abort(404)
    try:
        identifier = request.json['identifier']
        message_body = request.json.get('message_body', "")

        with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("INSERT INTO messages (identifier, message_body, date_created) VALUES (?, ?, ?)", (identifier, message_body, datetime.utcnow()))

            con.commit()
            msg = "Record successfully added"

    except:
        con.rollback()
        msg = "error in insert operation"

    finally:
        con.close()
        return jsonify({'msg': msg})


@app.route('/sms-service/api/v1.0/messages', methods=['GET'])
def get_messages():
    if request.json:
        try:
            start = request.json['start']
            stop = request.json['stop']
            
            con = sql.connect("database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            #cur.execute("UPDATE messages SET fetched = 1")
            cur.execute("SELECT * FROM messages ORDER BY datetime(date_created) DESC")
            messages =  [{j: i[j] for j in i.keys()} for i in cur.fetchall()]
            con.commit()
            con.close()
            return jsonify({'messages': messages[int(start):int(stop)]})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM messages WHERE fetched != 1 ORDER BY datetime(date_created) DESC")
        messages =  [{j: i[j] for j in i.keys()} for i in cur.fetchall()]
        cur.execute("UPDATE messages SET fetched = 1 where fetched != 1")
        con.commit()
        con.close()
        return jsonify({'messages': messages})


@app.route('/sms-service/api/v1.0/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    '''fetch a single message based on id passed in'''
    if not message_id:
        abort(404)
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM messages WHERE ID == ?", (str(message_id)))
    message = [{j: i[j] for j in i.keys()} for i in cur.fetchall()]
    con.close()
    if len(message) == 0:
        abort(404)
    else:
        return jsonify({'message': message})


@app.route('/sms-service/api/v1.0/messages/<int:message_id>', methods=['DELETE'])
def delete(message_id):
    '''delete a message based on id passed'''
    if not message_id:
        abort(404)
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM messages WHERE ID == ?", (str(message_id)))
            con.commit()

            msg = "Record successfully deleted"
    except:
        con.rollback()
        msg = "error in delete operation"

    finally:
        con.close()
        return jsonify({'msg': msg})

    




if __name__ == '__main__':
    app.run(debug=True)
