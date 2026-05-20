name: Scraping Automático de Titulares

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch: # Permite ejecutarlo manualmente haciendo clic en un botón de GitHub

jobs:
  scraper-job:
    runs-on: ubuntu-latest

    steps:
    - name: 1. Descargando el código del repositorio
      uses: actions/checkout@v4

    - name: 2. Configurando Python en el servidor
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: 3. Instalando librerías (Requests y BeautifulSoup4)
      run: |
        python -m pip install --upgrade pip
        pip install requests beautifulsoup4

    - name: 4. Ejecutando Scraper en Vivo
      run: python script.py
