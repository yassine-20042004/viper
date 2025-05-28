#!/usr/bin/env python3
"""
Personal Finance Manager - Point d'entrée principal
"""

from routes import app, data_manager
import os

def ensure_data_directory():
    """Créer le dossier data s'il n'existe pas"""
    if not os.path.exists('data'):
        os.makedirs('data')

if __name__ == '__main__':
    ensure_data_directory()
    print("🚀 Démarrage de Personal Finance Manager...")
    print("📊 Accédez à l'application sur: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)