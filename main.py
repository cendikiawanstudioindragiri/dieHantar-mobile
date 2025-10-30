import os

from flask import Flask
from blueprints.food_and_drinks import food_and_drinks_bp
from blueprints.auth import auth_bp
from blueprints.data_catalog import data_catalog_bp
from blueprints.orders import orders_bp
from blueprints.payments import payments_bp
from blueprints.drivers import drivers_bp # Impor blueprint driver

# Inisialisasi Firebase ditangani secara otomatis di dalam firebase_config.py

app = Flask(__name__)

# Daftarkan semua blueprint
app.register_blueprint(food_and_drinks_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(data_catalog_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(drivers_bp) # Daftarkan blueprint driver

@app.route("/")
def hello_world():
  """Contoh rute Hello World."""
  name = os.environ.get("NAME", "World")
  return f"Hello {name}!"

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))