import http.server
import socketserver
import json
import urllib.parse
import os

# Listes pour stocker les données
amounts_list = []
categories_list = []
descriptions_list = []

# Classe personnalisée pour gérer les requêtes HTTP
class FinanceTrackerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Servir la page d'accueil
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        # API pour récupérer toutes les dépenses
        elif self.path == '/api/expenses':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Préparation des données à envoyer
            expenses = []
            for i in range(len(amounts_list)):
                expenses.append({
                    'id': i + 1,
                    'amount': float(amounts_list[i]),
                    'category': categories_list[i],
                    'description': descriptions_list[i]
                })
            
            response = {
                'expenses': expenses,
                'total': sum(float(amount) for amount in amounts_list),
                'count': len(amounts_list)
            }
            
            # Envoi de la réponse JSON
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Si la route n'est pas reconnue, servir le fichier si existant
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        # API pour ajouter une dépense
        if self.path == '/api/add_expense':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Traitement des données JSON reçues
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # Extraction des données
                amount = float(data.get('amount', 0))
                category = data.get('category', '')
                description = data.get('description', '')
                
                # Ajout aux listes
                amounts_list.append(amount)
                categories_list.append(category)
                descriptions_list.append(description)
                
                # Calcul du total
                total = sum(float(amount) for amount in amounts_list)
                
                # Préparation de la réponse
                response = {
                    'success': True,
                    'total': total,
                    'count': len(amounts_list)
                }
                
                # Envoi de la réponse
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                # En cas d'erreur
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())
            
            return
        
        # Si la route n'est pas reconnue
        else:
            self.send_response(404)
            self.end_headers()
            return

def run_server(port=8000):
    """Lance le serveur HTTP sur le port spécifié"""
    handler = FinanceTrackerHandler
    
    # Utilisation du répertoire courant pour servir les fichiers statiques
    web_dir = os.path.join(os.path.dirname(__file__), '')
    os.chdir(web_dir)
    
    # Création et démarrage du serveur
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serveur démarré sur le port {port}")
        print(f"Ouvrez votre navigateur à l'adresse http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()