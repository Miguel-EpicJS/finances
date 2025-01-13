from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

def fetch_fundamentus_data():
    url = "https://www.fundamentus.com.br/fii_resultado.php"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch data from Fundamentus")

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "tabelaResultado"})  # Find the target table by its ID

    if not table:
        raise Exception("Table not found on the page")

    # Extract the table headers
    headers = [th.text.strip() for th in table.find_all("th")]

    # Extract the table rows
    rows = []
    for tr in table.find_all("tr")[1:]:  # Skip the header row for rows
        cells = [td.text.strip() for td in tr.find_all("td")]
        if cells:
            rows.append(cells)

    # Convert to a pandas DataFrame
    df = pd.DataFrame(rows, columns=headers)
    df["Vacância Média"]= df["Vacância Média"].str.replace(',', '', regex=True).str.rstrip('%').astype(float) / 100
    df["Cap Rate"]= df["Cap Rate"].str.replace(',', '', regex=True).str.rstrip('%').astype(float) / 100
    df["P/VP"]= df["P/VP"].str.replace(',', '', regex=True).str.rstrip('%').astype(float) / 100
    df["Dividend Yield"]= df["Dividend Yield"].str.replace(',', '', regex=True).str.rstrip('%').astype(float) / 100
    df["FFO Yield"]= df["FFO Yield"].str.replace(',', '', regex=True).str.rstrip('%').astype(float) / 100

    df["Cotação"]= df["Cotação"].str.replace(',', '', regex=True).astype(float) / 100
    df["Valor de Mercado"]= df["Valor de Mercado"].str.replace('.', '').astype(int)
    df["Liquidez"]= df["Liquidez"].str.replace('.', '').astype(int)

    return df

@app.route('/fii', methods=['GET'])
def get_fundamentus_data():
    try:
        df = fetch_fundamentus_data()
        data = df.to_dict(orient="list")  # Convert DataFrame to a dictionary with arrays
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
