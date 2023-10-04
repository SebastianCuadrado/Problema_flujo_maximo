from flask import Flask, render_template, request, jsonify
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import json
import matplotlib
import math
matplotlib.use('Agg')

app = Flask(__name__, static_folder='static')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/principal', methods=['GET', 'POST'])
def principal():
    
    return render_template('principal.html')

@app.route('/generar_grafo', methods=['POST'])
def generar_grafo():
    pos={}
    try:
        # Obtener la matriz desde los datos del formulario
        matriz_data = request.form.get('matrizData')
        print("Matriz recibida:")
        print(matriz_data)  # Debe ir después de obtener la matriz

        matriz = json.loads(matriz_data)
        plt.figure()

        # Procesa la matriz para crear un grafo (debes implementar esta lógica)
        G = nx.DiGraph()
        # Agrega nodos y aristas basados en la matriz
        num_nodos = len(matriz)
        G.add_nodes_from(range(num_nodos))

        for i in range(num_nodos):
            for j in range(num_nodos):
                if matriz[i][j] > 0:
                    G.add_edge(i, j, weight=matriz[i][j])
                    
        pos[0] = (0, 0)
        pos[num_nodos - 1] = (10, 0)

        # Calcular las posiciones de los nodos intermedios en línea recta
        for i in range(1, num_nodos - 1):
            if num_nodos<=8:
                if i%2==0:
                    x = 10 * (i-1) / (num_nodos - 1)  # Distribuir nodos uniformemente
                    y = -3  # En la misma línea horizontal
                else:
                    x = 10 * i / (num_nodos - 1)  # Distribuir nodos uniformemente
                    y = 3  # En la misma línea horizontal 
            else:
                if i%3==1:
                    x = 10 * (i) / (num_nodos - 1)  # Distribuir nodos uniformemente
                    y = -3  # En la misma línea horizontal
                if i%3==2:
                    x = 10 * (i-1) / (num_nodos - 1)  # Distribuir nodos uniformemente
                    y = 0  # En la misma línea horizontal
                if i%3==0:
                    x = 10 * (i-2) / (num_nodos - 1)  # Distribuir nodos uniformemente
                    y = 3  # En la misma línea horizontal
                    
            
            pos[i] = (x, y)

        
        # Dibuja el grafo
        
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue")
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # Convierte el grafo en una imagen y devuelve los datos de la imagen
        print("Generando imagen del grafo")

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        print("Imagen generada")

        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        print("Imagen generada")
        plt.close()

        return jsonify({'image_url': 'data:image/png;base64, ' + img_base64})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
