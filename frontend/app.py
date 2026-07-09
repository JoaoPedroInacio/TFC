from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulação de uma Base de Dados de Carros (Mais completa para testar filtros)
stock_carros = [
    {
        'id': 1,
        'marca': 'BMW',
        'modelo': 'M4 Competition',
        'preco': '89.900',
        'ano': 2023,
        'kms': '12.500',
        'combustivel': 'Gasolina',
        'img': 'https://images.unsplash.com/photo-1617531653332-bd46c24f2068?w=800'
    },
    {
        'id': 2,
        'marca': 'Mercedes-Benz',
        'modelo': 'AMG GT 63',
        'preco': '145.000',
        'ano': 2022,
        'kms': '18.000',
        'combustivel': 'Gasolina',
        'img': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800'
    },
    {
        'id': 3,
        'marca': 'Audi',
        'modelo': 'RS6 Avant',
        'preco': '132.900',
        'ano': 2023,
        'kms': '24.000',
        'combustivel': 'Gasolina',
        'img': 'https://images.unsplash.com/photo-1606016159991-dfe4f974be5c?w=800'
    },
    {
        'id': 4,
        'marca': 'Porsche',
        'modelo': 'Taycan 4S',
        'preco': '98.500',
        'ano': 2021,
        'kms': '31.200',
        'combustivel': 'Elétrico / Híbrido',
        'img': 'https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=800'
    }
]

@app.route('/')
def home():
    # Na homepage, podemos enviar apenas os 3 carros mais recentes/destaques
    return render_template('index.html', carros=stock_carros[:3])

@app.route('/veiculos')
def veiculos_page():
    # Nova página dedicada apenas para ver o stock e filtrar
    return render_template('veiculos.html')

@app.route('/api/veiculos')
def api_veiculos():
    # Rota que o JavaScript vai chamar para obter os carros filtrados
    pesquisa = request.args.get('pesquisa', '').lower()
    marca = request.args.get('marca', 'Todas as Marcas')
    combustiveis = request.args.getlist('combustivel') # Recebe múltiplos se selecionados

    carros_filtrados = stock_carros

    # 1. Filtro de Pesquisa de Texto
    if pesquisa:
        carros_filtrados = [c for c in carros_filtrados if pesquisa in c['marca'].lower() or pesquisa in c['modelo'].lower()]

    # 2. Filtro de Marca
    if marca != 'Todas as Marcas':
        carros_filtrados = [c for c in carros_filtrados if c['marca'] == marca]

    # 3. Filtro de Combustível
    if combustiveis:
        carros_filtrados = [c for c in carros_filtrados if c['combustivel'] in combustiveis]

    return jsonify(carros_filtrados)

@app.route('/veiculo/<int:id>')
def detalhe(id):
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