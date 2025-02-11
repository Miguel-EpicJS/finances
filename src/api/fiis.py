from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Base URL for Fundamentus
BASE_URL = "https://www.fundamentus.com.br/detalhes.php?papel="

def scrape_fundamentus(papel):
    """
    Scrapes data from the Fundamentus website for the given stock/FII code.
    :param papel: Stock or FII code (e.g., HGLG11)
    :return: Dictionary containing scraped data
    """
    url = BASE_URL + papel
    headers = {
    'authority': 'www.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'SID=ZAjX93QUU1NMI2Ztt_dmL9YRSRW84IvHQwRrSe1lYhIZncwY4QYs0J60X1WvNumDBjmqCA.; __Secure- 
    #..,
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"115.0.5790.110"',
    'sec-ch-ua-full-version-list': '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.110", "Chromium";v="115.0.5790.110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': 'Windows',
    'sec-ch-ua-platform-version': '15.0.0',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-client-data': '#..',
    }

    
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract relevant data
        data = {}

        # Helper function to find and extract text
        def extract_value(label):
            element = soup.find("span", string=label)
            return element.find_next("span").text.strip() if element else None

        # Basic Information
        data["FII"] = papel
        data["Cotação"] = extract_value("Cotação")
        data["Nome"] = extract_value("Nome")
        data["Data últ cot"] = extract_value("Data últ cot")
        data["Mandato"] = extract_value("Mandato")
        data["Min 52 sem"] = extract_value("Min 52 sem")
        data["Segmento"] = extract_value("Segmento")
        data["Max 52 sem"] = extract_value("Max 52 sem")
        data["Gestão"] = extract_value("Gestão")
        data["Vol $ méd (2m)"] = extract_value("Vol $ méd (2m)")
        data["Valor de mercado"] = extract_value("Valor de mercado")
        data["Nro. Cotas"] = extract_value("Nro. Cotas")
        data["Relatório"] = extract_value("Relatório")
        data["Últ Info Trimestral"] = extract_value("Últ Info Trimestral")

        # Oscilações and Indicadores
        data["Oscilações - Dia"] = extract_value("Dia")
        data["Oscilações - Mês"] = extract_value("Mês")
        data["Oscilações - 30 dias"] = extract_value("30 dias")
        data["Oscilações - 12 meses"] = extract_value("12 meses")
        data["Indicadores - FFO Yield"] = extract_value("FFO Yield")
        data["Indicadores - FFO/Cota"] = extract_value("FFO/Cota")
        data["Indicadores - Div. Yield"] = extract_value("Div. Yield")
        data["Indicadores - Dividendo/cota"] = extract_value("Dividendo/cota")
        data["Indicadores - P/VP"] = extract_value("P/VP")
        data["Indicadores - VP/Cota"] = extract_value("VP/Cota")

        # Resultado
        data["Resultado - 2025"] = extract_value("2025")
        data["Resultado - 2024"] = extract_value("2024")
        data["Resultado - 2023"] = extract_value("2023")
        data["Resultado - 2022"] = extract_value("2022")
        data["Resultado - 2021"] = extract_value("2021")
        data["Resultado - 2020"] = extract_value("2020")
        data["Receita - Últimos 12 meses"] = extract_value("Receita")
        data["Receita - Últimos 3 meses"] = extract_value("Receita")
        data["Venda de ativos - Últimos 12 meses"] = extract_value("Venda de ativos")
        data["Venda de ativos - Últimos 3 meses"] = extract_value("Venda de ativos")
        data["FFO - Últimos 12 meses"] = extract_value("FFO")
        data["FFO - Últimos 3 meses"] = extract_value("FFO")
        data["Rend. Distribuído - Últimos 12 meses"] = extract_value("Rend. Distribuído")
        data["Rend. Distribuído - Últimos 3 meses"] = extract_value("Rend. Distribuído")

        # Balanço Patrimonial
        data["Ativos"] = extract_value("Ativos")
        data["Patrim Líquido"] = extract_value("Patrim Líquido")

        # Composição dos Ativos
        data["Qtd imóveis"] = extract_value("Qtd imóveis")
        data["Área (m2)"] = extract_value("Área (m2)")
        data["Cap Rate"] = extract_value("Cap Rate")
        data["Qtd Unidades"] = extract_value("Qtd Unidades")
        data["Aluguel/m2"] = extract_value("Aluguel/m2")
        data["Vacância Média"] = extract_value("Vacância Média")
        data["Imóveis/PL do FII"] = extract_value("Imóveis/PL do FII")
        data["Preço do m2"] = extract_value("Preço do m2")

        return data
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/scrape', methods=['GET'])
def scrape():
    """
    API endpoint to scrape data for a given stock/FII code.
    """
    papel = request.args.get('papel', '').strip().upper()
    if not papel:
        return jsonify({"error": "Please provide a valid 'papel' parameter."}), 400
    
    # Scrape data
    result = scrape_fundamentus(papel)
    
    # Return the result as JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
