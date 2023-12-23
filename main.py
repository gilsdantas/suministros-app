from flask import Flask

app = Flask(__name__) # En app se encuentra nuestro servidor web de Flask


@app.route('/')
def home():
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True) # El debug=True hace que cada vez que reiniciemos
