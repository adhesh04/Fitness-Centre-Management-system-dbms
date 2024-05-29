from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mag@2004',
            database='adhkash'
        )
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def vain():
    return render_template('index.html')

@app.route('/main.html')
def main():
    return render_template('main.html')

@app.route('/modify.html')
def modify():
    return render_template('modify.html')

@app.route('/get_data')
def get_data():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM members;")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear_data')
def clear_data():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM members;")
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "All data cleared successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_data")
def delete_data():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM members ORDER BY id DESC LIMIT 1")
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/get_columns')
def get_columns():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Execute query to get column names
        cursor.execute("SHOW COLUMNS FROM members")
        columns = [column[0] for column in cursor.fetchall()]
        cursor.close()
        db.close()
        return jsonify(columns)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def update_data(id, column, new_value):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Assuming 'members' is the table name
        query = f"UPDATE members SET {column} = %s WHERE id = %s"
        cursor.execute(query, (new_value, id))
        db.commit()
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print("Error updating data:", e)
        return False

@app.route('/update_data/<int:id>', methods=['PUT'])
def update_member_data(id):
    try:
        data = request.get_json()
        if 'column' not in data or 'newValue' not in data:
            return jsonify({"error": "Column name or new value not provided"}), 400
        column = data['column']
        new_value = data['newValue']
        if update_data(id, column, new_value):
            return jsonify({"message": f"Data in column '{column}' updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update data"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        dateOfBirth = request.form['dateOfBirth']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        mobile = request.form['mobile']
        membershipType = request.form['membershipType']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO members (firstName, lastName, dateOfBirth, age, gender, address, mobile, membershipType)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (firstName, lastName, dateOfBirth, age, gender, address, mobile, membershipType))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('success'))
        else:
            return "Failed to connect to the database."
    except Exception as e:
        print("Error inserting data into database:", e)
        return "An error occurred while processing your request."

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
