from flask import Flask, render_template, jsonify

app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")

@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': "hello world"
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
