import requests

class Fetching:
    @staticmethod
    def get(url):
        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Server error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Network error {e}")


    @staticmethod
    def convert_currency(amt_base, base, quote):
        data = Fetching.get(f"https://api.frankfurter.dev/v2/rates?base={base}&quotes={quote}")

        rate = data[0]["rate"]
        amt_quote = amt_base*rate

        return amt_quote