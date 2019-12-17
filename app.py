from flask import Flask, render_template

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase" #needs to be changed

@app.route('/')
def main():
    return render_template('testing.html')

if __name__ == '__main__':
    app.run(debug=True)
