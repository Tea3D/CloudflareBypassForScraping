from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

def get_page_with_cookies(url, cookies_str):
    try:
        cookies = {c.split('=')[0]: c.split('=')[1] for c in cookies_str.split('; ')}
        response = requests.get(url, cookies=cookies, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        })
        return {"status": "success", "html": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/html', methods=['GET'])
def get_html():
    url = request.args.get('url')
    cookies_str = os.getenv("CLOUDFLARE_COOKIES", "")
    if not url or not cookies_str:
        return jsonify({"status": "error", "message": "URL и CLOUDFLARE_COOKIES обязательны"})
    result = get_page_with_cookies(url, cookies_str)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
