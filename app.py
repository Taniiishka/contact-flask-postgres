from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


DB_HOST = 'localhost'
DB_NAME = 'contactdb'
DB_USER = 'postgres'
DB_PASS = 'tanishka@123'  

def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/')
def home():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone')  
        subject = request.form['subject']
        message = request.form['message']

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO contact_form (name, email, phone, subject, message)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, subject, message))
        conn.commit()
        cur.close()
        conn.close()

        return render_template('contact.html', success=True)

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
