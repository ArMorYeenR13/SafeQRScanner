#API
import whois as wi # whois lookup
import requests
import json
import time
import re
import tldextract
from dotenv import load_dotenv


APIKEY_urlscanio = os.getenv("APIKEY_urlscanio")

def API_urlscan_post(url):
    #has api limit, use with care
    api = "https://urlscan.io/api/v1/scan/"
    headers = {
        "API-Key": APIKEY_urlscanio,
        "Content-Type": "application/json",
    }
    payload = {
        "url": url,
        "visibility": "public"
    }
    response = requests.post(api, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result_api = response.json()["uuid"]
        return result_api
    else:
        print("Error:", response.text)
        return None


def API_urlscan_get(uuid):
    result_api = f"https://urlscan.io/api/v1/result/{uuid}/"
    print("Waiting for 15 seconds before polling for the scan result...")
    time.sleep(15)

    max_retries = 3  # Maximum number of retries
    retries = 0
    while retries < max_retries:
        response = requests.get(result_api)
        if response.status_code == 200:
            result = response.json()
            return result
        elif response.status_code == 404:
            print("Not done, wait another 10 seconds")
            time.sleep(10)  # Poll every 10 seconds
            retries += 1
        else:
            print("Error:", response.text)
            return None

    print("Max retries reached. Scan may still be in progress.")
    return None


def print_scan_result(result):
    if result:
        page = result.get("page", {})
        data = result.get("data", {})
        verdicts = result.get("verdicts", {})

        title = page.get("title")
        mimeType = page.get("mimeType")
        status = page.get("status")
        redirected = page.get("redirected")
        ranking = page.get("umbrellaRank")
        country = page.get("country")
        server = page.get("server")
        tlsIssuer = page.get("tlsIssuer")
        tlsvalidDays = page.get("tlsValidDays")

        numRequest = len(data.get("requests", []))
        numCookies =  len(data.get("cookies", []))
        numConsoleMsg =  len(data.get("console", []))
        numLinks = len(data.get("links", []))

        score = verdicts.get("overall", {}).get("score")
        category =  verdicts.get("overall", {}).get("categories")

        # print("\nPage Information:")
        # print("Page URL:", page.get("url")) #not needed
        #
        # print("Page Title:", title)
        # print("Page MIME type:", mimeType)
        #
        # print("Page Status:", status)
        # print("Page Redirected:", redirected)
        #
        # print("Page umbrella ranking:", ranking)
        # print("Page Country:", country)
        # print("Page City:", page.get("city"))  #not needed
        #
        # print("Page server:", server)
        # print("Page tlsIssuer:", tlsIssuer)
        # print("Page tlsValidDays:",tlsvalidDays)
        #
        #
        # print("\nData:")
        # print("Number of Requests:", numRequest)
        # print("Number of Cookies:", numCookies)
        #
        # print("Number of Console Messages:", numConsoleMsg)
        # print("Number of Links:", numLinks)
        #
        # print("\nVerdicts:")
        # print("URLScan Score:", score) #0 = benign , 100 = malicious
        # print("URLScan Categories:",category) # category of link

        return {
            "Page title": title,
            "mimeType": mimeType,
            "status": status,
            "redirected": redirected,
            "ranking": ranking,
            "country": country,
            "server": server,
            "tlsIssuer": tlsIssuer,
            "tlsValidDays": tlsvalidDays,
            "numRequest": numRequest,
            "num Links": numLinks,
            "num Cookies": numCookies,
            "num Console Msg": numConsoleMsg,
            "urlscan Score": score,
            "urlscan category": category,
        }

def print_scan_result_and_dom(result,dom):
    #not used, had ran this for some database but did not gather sufficient data from it
    # why iframe? -> basically another HTML on top of existing one
    # why eval(), atob() , eval() , unescape() ? usually used for javascript obfuscation to avoid detection
    if result and dom:
        page = result.get("page", {})
        data = result.get("data", {})
        verdicts = result.get("verdicts", {})

        title = page.get("title")
        mimeType = page.get("mimeType")
        status = page.get("status")
        redirected = page.get("redirected")
        ranking = page.get("umbrellaRank")
        country = page.get("country")
        server = page.get("server")
        tlsIssuer = page.get("tlsIssuer")
        tlsvalidDays = page.get("tlsValidDays")

        numRequest = len(data.get("requests", []))
        numCookies = len(data.get("cookies", []))
        numConsoleMsg = len(data.get("console", []))
        numLinks = len(data.get("links", []))

        score = verdicts.get("overall", {}).get("score")
        category = verdicts.get("overall", {}).get("categories")

        ##Dom
        count_link = dom.count('link(')
        count_eval = dom.count('eval(')
        count_exec = dom.count('exec(')
        count_unescape = dom.count('unescape(')
        count_search = dom.count('search(')
        count_find = dom.count('find(')
        count_escape = dom.count('escape(')
        presence_iframe = int('<iframe' in dom)
        presence_window_open = int(bool(re.search(r'window\.open\s*\(', dom, re.IGNORECASE)))

        return {
            "Page title": title,
            "mimeType": mimeType,
            "status": status,
            "redirected": redirected,
            "ranking": ranking,
            "country": country,
            "server": server,
            "tlsIssuer": tlsIssuer,
            "tlsValidDays": tlsvalidDays,
            "numRequest": numRequest,
            "num Links": numLinks,
            "num Cookies": numCookies,
            "num Console Msg": numConsoleMsg,
            "urlscan Score": score,
            "urlscan category": category,
            "JS_count_link": count_link,
            "JS_count_eval": count_eval,
            "JS_count_exec": count_exec,
            "JS_count_unescape": count_unescape,
            "JS_count_search": count_search,
            "JS_count_find": count_find,
            "JS_count_escape": count_escape,
            "JS_presence_iframe": presence_iframe,
            "presence_window.open" : presence_window_open
        }


def run_urlscan_api(url):
    scan_id = API_urlscan_post(url)
    #default final to status 400
    final = {"status": 400,}
    if scan_id:
        print("URLScan.io Scan ID:", scan_id)
        result = API_urlscan_get(scan_id)
        if result is None:
            final = {"status": 400,}
        else:
            final = print_scan_result(result)
    return final