from flask import Flask, render_template

app = Flask(__name__)

# Simulação de uma Base de Dados de Carros
# No futuro, isto virá de um ficheiro SQL
stock_carros = [
    {
        'id': 1,
        'marca': 'BMW',
        'modelo': 'M4 Competition',
        'preco': '89.900',
        'ano': 2022,
        'kms': '12.500',
        'img': 'https://images.unsplash.com/photo-1617531653332-bd46c24f2068?w=800'
    },
    {
        'id': 2,
        'marca': 'Mercedes-Benz',
        'modelo': 'AMG GT 63',
        'preco': '145.000',
        'ano': 2022,
        'kms': '18.000',
        'img': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800'
    }
]

@app.route('/')
def home():
    # Enviamos a lista de carros para o HTML
    return render_template('index.html', carros=stock_carros)

@app.route('/veiculo/<int:id>')
def detalhe(id):
    # Procura o carro pelo ID na nossa lista
    carro = next((c for c in stock_carros if c['id'] == id), None)
    return render_template('detalhe_veiculo.html', carro=carro)

@app.route('/sobre')
def sobre():
    return render_template('SobreNos.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)