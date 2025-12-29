
import pandas as pd
import re

#extract , preprocessing
import whois as wi # whois lookup
import tldextract
import requests
from urllib.parse import urlparse

#========================================
# Lexical Features

# URL length - remove https, http , www
# Number of special character - includes [! # 	$ 	& 	' 	( 	) 	* 	+ 	, 	/ 	: 	; 	= 	? 	@ 	[ 	]]
# exist a query
# query length
# path length
#number of subdomains!!!!!!
# number of numbers used - [0 - 9 ]
# HTTPS - if it is using https
# geological data - get universal code
# shortened? - see if link is shortened --- not done
# TLD - include .com .org etc
# special words, "login ,  signin, account, virus, exe, dat, access"
# special cmds in query " ref, id, session, cmd"

# if root domain consist special code like org https etc


def get_url_length(url):
    url = url.replace('www.', '')
    protocol = ['http://', 'https://']
    for num in protocol:
        if url.startswith(num):
            url = url[len(num):]
    return len(url)

def get_query_length(url):
    query_str = urlparse(url).query
    if query_str:
        return len(query_str)
    return 0

def get_path_length(url):
    path = urlparse(url).path
    return len(path)

def get_path_depth(url):
    path_depth = len([segment for segment in urlparse(url).path.split('/') if segment])

    return path_depth

def get_num_count(url):
    count = 0
    for c in url:
        count += c.isdigit()
    return count

def get_num_count_TLD(url):
    count = 0
    for c in url:
        count += c.isdigit()
    return count

def has_https(url):
    return int(urlparse(url).scheme == 'https')

def get_count_special_characters(url):
    #reserved characters in url
    special_characters = set("!*'();:@&=+$,/?%#[]")
    protocol = ['http://', 'https://']
    for num in protocol:
        if url.startswith(num):
            url = url[len(num):]
    count = sum(1 for char in url if char in special_characters)
    return count

def get_count_unreserved_special_characters(url):
    #reserved characters in url
    special_characters = set("-_.~")
    protocol = ['http://', 'https://']
    for num in protocol:
        if url.startswith(num):
            url = url[len(num):]
    count = sum(1 for char in url if char in special_characters)
    return count



def get_url_region(primary_domain):
    #data collected from wiki
    #ISO-3166-1 with the exception ac, eu and uk  (not used gb,bv,bl,mf,sj,um)
    ccTLD_to_region = {
        ".ac": "Ascension Island",
        ".ad": "Andorra",
        ".ae": "United Arab Emirates",
        ".af": "Afghanistan",
        ".ag": "Antigua and Barbuda",
        ".ai": "Anguilla",
        ".al": "Albania",
        ".am": "Armenia",
        ".ao": "Angola",
        ".aq": "Antarctica",
        ".ar": "Argentina",
        ".as": "American Samoa",
        ".at": "Austria",
        ".au": "Australia",
        ".aw": "Aruba",
        ".ax": "Åland",
        ".az": "Azerbaijan",
        ".ba": "Bosnia and Herzegovina",
        ".bb": "Barbados",
        ".bd": "Bangladesh",
        ".be": "Belgium",
        ".bf": "Burkina Faso",
        ".bg": "Bulgaria",
        ".bh": "Bahrain",
        ".bi": "Burundi",
        ".bj": "Benin",
        ".bm": "Bermuda",
        ".bn": "Brunei",
        ".bo": "Bolivia",
        ".bq": "Carribbean Netherlands",
        ".br": "Brazil",
        ".bs": "Bahamas",
        ".bt": "Bhutan",
        ".bw": "Botswana",
        ".by": "Belarus",
        ".bz": "Belize",
        ".ca": "Canada",
        ".cc": "Cocos Islands",
        ".cd": "Democratic Republic of the Congo",
        ".cf": "Central African Republic",
        ".cg": "Republic of the Congo",
        ".ch": "Switzerland",
        ".ci": "Ivory Coast",
        ".ck": "Cook Islands",
        ".cl": "Chile",
        ".cm": "Cameroon",
        ".cn": "China",
        ".co": "Colombia",
        ".cr": "Costa Rica",
        ".cu": "Cuba",
        ".cv": "Cape Verde",
        ".cw": "Curaçao",
        ".cx": "Christmas Island",
        ".cy": "Cyprus",
        ".cz": "Czech Republic",
        ".de": "Germany",
        ".dj": "Djibouti",
        ".dk": "Denmark",
        ".dm": "Dominica",
        ".do": "Dominican Republic",
        ".dz": "Algeria",
        ".ec": "Ecuador",
        ".ee": "Estonia",
        ".eg": "Egypt",
        ".eh": "Western Sahara",
        ".er": "Eritrea",
        ".es": "Spain",
        ".et": "Ethiopia",
        ".eu": "European Union",
        ".fi": "Finland",
        ".fj": "Fiji",
        ".fk": "Falkland Islands",
        ".fm": "Federated States of Micronesia",
        ".fo": "Faroe Islands",
        ".fr": "France",
        ".ga": "Gabon",
        ".gd": "Grenada",
        ".ge": "Georgia",
        ".gf": "French Guiana",
        ".gg": "Guernsey",
        ".gh": "Ghana",
        ".gi": "Gibraltar",
        ".gl": "Greenland",
        ".gm": "Gambia",
        ".gn": "Guinea",
        ".gp": "Guadeloupe",
        ".gq": "Equatorial Guinea",
        ".gr": "Greece",
        ".gs": "South Georgia and the South Sandwich Islands",
        ".gt": "Guatemala",
        ".gu": "Guam",
        ".gw": "Guinea-Bissau",
        ".gy": "Guyana",
        ".hk": "Hong Kong",
        ".hm": "Heard Island and McDonald Islands",
        ".hn": "Honduras",
        ".hr": "Croatia",
        ".ht": "Haiti",
        ".hu": "Hungary",
        ".id": "Indonesia",
        ".ie": "Ireland",
        ".il": "Israel",
        ".im": "Isle of Man",
        ".in": "India",
        ".io": "British Indian Ocean Territory",
        ".iq": "Iraq",
        ".ir": "Iran",
        ".is": "Iceland",
        ".it": "Italy",
        ".je": "Jersey",
        ".jm": "Jamaica",
        ".jo": "Jordan",
        ".jp": "Japan",
        ".ke": "Kenya",
        ".kg": "Kyrgyzstan",
        ".kh": "Cambodia",
        ".ki": "Kiribati",
        ".km": "Comoros",
        ".kn": "Saint Kitts and Nevis",
        ".kp": "North Korea",
        ".kr": "South Korea",
        ".kw": "Kuwait",
        ".ky": "Cayman Islands",
        ".kz": "Kazakhstan",
        ".la": "Laos",
        ".lb": "Lebanon",
        ".lc": "Saint Lucia",
        ".li": "Liechtenstein",
        ".lk": "Sri Lanka",
        ".lr": "Liberia",
        ".ls": "Lesotho",
        ".lt": "Lithuania",
        ".lu": "Luxembourg",
        ".lv": "Latvia",
        ".ly": "Libya",
        ".ma": "Morocco",
        ".mc": "Monaco",
        ".md": "Moldova",
        ".me": "Montenegro",
        ".mf": "Saint Martin (French part)",
        ".mg": "Madagascar",
        ".mh": "Marshall Islands",
        ".mk": "North Macedonia",
        ".ml": "Mali",
        ".mm": "Myanmar",
        ".mn": "Mongolia",
        ".mo": "Macao",
        ".mp": "Northern Mariana Islands",
        ".mq": "Martinique",
        ".mr": "Mauritania",
        ".ms": "Montserrat",
        ".mt": "Malta",
        ".mu": "Mauritius",
        ".mv": "Maldives",
        ".mw": "Malawi",
        ".mx": "Mexico",
        ".my": "Malaysia",
        ".mz": "Mozambique",
        ".na": "Namibia",
        ".nc": "New Caledonia",
        ".ne": "Niger",
        ".nf": "Norfolk Island",
        ".ng": "Nigeria",
        ".ni": "Nicaragua",
        ".nl": "Netherlands",
        ".no": "Norway",
        ".np": "Nepal",
        ".nr": "Nauru",
        ".nu": "Niue",
        ".nz": "New Zealand",
        ".om": "Oman",
        ".pa": "Panama",
        ".pe": "Peru",
        ".pf": "French Polynesia",
        ".pg": "Papua New Guinea",
        ".ph": "Philippines",
        ".pk": "Pakistan",
        ".pl": "Poland",
        ".pm": "Saint Pierre and Miquelon",
        ".pn": "Pitcairn Island",
        ".pr": "Puerto Rico",
        ".ps": "Palestine",
        ".pt": "Portugal",
        ".pw": "Palau",
        ".py": "Paraguay",
        ".qa": "Qatar",
        ".re": "Réunion",
        ".ro": "Romania",
        ".rs": "Serbia",
        ".ru": "Russia",
        ".rw": "Rwanda",
        ".sa": "Saudi Arabia",
        ".sb": "Solomon Islands",
        ".sc": "Seychelles",
        ".sd": "Sudan",
        ".se": "Sweden",
        ".sg": "Singapore",
        ".sh": "Saint Helena",
        ".si": "Slovenia",
        ".sk": "Slovakia",
        ".sl": "Sierra Leone",
        ".sm": "San Marino",
        ".sn": "Senegal",
        ".so": "Somalia",
        ".sr": "Suriname",
        ".ss": "South Sudan",
        ".st": "São Tomé and Príncipe",
        ".sv": "El Salvador",
        ".sx": "Sint Maarten",
        ".sy": "Syria",
        ".sz": "Eswatini",
        ".tc": "Turks and Caicos Islands",
        ".td": "Chad",
        ".tf": "French Southern and Antarctic Lands",
        ".tg": "Togo",
        ".th": "Thailand",
        ".tj": "Tajikistan",
        ".tk": "Tokelau",
        ".tl": "East Timor",
        ".tm": "Turkmenistan",
        ".tn": "Tunisia",
        ".to": "Tonga",
        ".tr": "Turkey",
        ".tt": "Trinidad and Tobago",
        ".tv": "Tuvalu",
        ".tw": "Taiwan",
        ".tz": "Tanzania",
        ".ua": "Ukraine",
        ".ug": "Uganda",
        ".uk": "United Kingdom",
        ".us": "United States of America",
        ".uy": "Uruguay",
        ".uz": "Uzbekistan",
        ".va": "Vatican City",
        ".vc": "Saint Vincent and the Grenadines",
        ".ve": "Venezuela",
        ".vg": "British Virgin Islands",
        ".vi": "US Virgin Islands",
        ".vn": "Vietnam",
        ".vu": "Vanuatu",
        ".wf": "Wallis and Futuna",
        ".ws": "Samoa",
        ".ye": "Yemen",
        ".yt": "Mayotte",
        ".za": "South Africa",
        ".zm": "Zambia",
        ".zw": "Zimbabwe"
    }

    for ccTLD in ccTLD_to_region:
        if primary_domain.endswith(ccTLD):
            return ccTLD_to_region[ccTLD]

    return "Global"


def get_generic_TLD(primary_domain, ccTLD):
    # for name and pro need eligibility so unlikely
    # edu,gov , mil , int are considered sponsered
    #source wiki
    TLD_to_generic = {
        ".com": "Commercial",
        ".org": "Organisation",
        ".net": "Network",
        ".int": "international",
        ".edu": "educational",
        ".gov": "government",
        ".mil": "military",
        ".biz": "business",
        ".info": "information",
        ".name": "(restricted) name",
        ".pro": "(restricted) pro",
    }
    if ccTLD != "Global":
        return "Country"
    else:
        for TLD in TLD_to_generic:
            if primary_domain.endswith(TLD):
                return TLD_to_generic[TLD]
    return "Unknown"


def is_url_shortened(uri):
    shortening_services = [
        'bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 'is.gd',
        'snipurl.com', 'short.io', 'kl.am', 'wp.me', 'to.ly', 'bit.do', 'bitly.is',
        'tinyurl.is', 'bit.ly', 'ity.im', 'is.gd',
        '1url.com', 'tr.im', 'linktr.ee', 'tiny.cc'
    ]

    host = urlparse(uri).hostname
    if host is not None:
        host = host.lower()

    for service in shortening_services:
        if host == service.lower():
            return 1

    return 0

# includes subdomain . domain . suffix
def extract_pri_domain(url):
    extracted = tldextract.extract(url)
    all = extracted.fqdn
    return all


def extract_root_domain(url):
    extract = tldextract.TLDExtract(include_psl_private_domains=True)
    extracted = extract(url)
    root_domain = extracted.domain
    return root_domain

def extract_sub_domain(url):
    extract = tldextract.TLDExtract(include_psl_private_domains=True)
    extracted = extract(url)
    subdomain = extracted.subdomain
    # Split the subdomain by '.' and count the parts
    subdomain_count = len(subdomain.split('.')) if subdomain else 0
    return subdomain_count

#========================================

# host based features
# whois mask is used
# redirects occurs
# expiry date
# date created
# registrar (which domain host)
# name  ( can be whois masked)


def get_status_code(url):
    try:
        response = requests.get(url, allow_redirects=False,timeout=5)
        return response.status_code
    except requests.exceptions.Timeout:
        return "Timeout"
    except requests.exceptions.RequestException as e:
        return "ERROR"



def get_whois_info(url):
    try:

        domain = extract_pri_domain(url)

        if len(domain) > 253:
            print(f"Skipping {url} - Domain name too long")
            return None

        # Encode the domain
        encoded_domain = domain.encode('idna')
        #  WHOIS lookup
        w = wi.whois(encoded_domain.decode('utf-8'))
        return w
    except wi.parser.PywhoisError:
        print(f"Error extracting WHOIS information for {url}")
        return None

edited_path = '../list_combined.csv'

if __name__ == '__main__':
    print("running...")
    url_table = pd.read_csv(edited_path)

    url_table = url_table.rename(columns={"Domain": 'url'})
    print(url_table.head())

    # Lexical features
    url_table['url_len'] = url_table['url'].apply(lambda x: get_url_length(str(x)))
    url_table['path_length'] = url_table['url'].apply(lambda x: get_path_length(str(x)))
    url_table['path_depth'] = url_table['url'].apply(lambda x: (get_path_depth((x))))
    url_table['query_length'] = url_table['url'].apply(lambda x: get_query_length(str(x)))
    url_table['num 0-9 count'] = url_table['url'].apply(lambda x: get_num_count(x))
    url_table['reserved char count'] = url_table['url'].apply(lambda x: get_count_special_characters(x))
    url_table['pri_domain'] = url_table['url'].apply(lambda x: extract_pri_domain(x))
    url_table['url shortened'] = url_table['url'].apply(lambda x: is_url_shortened(x))
    url_table['num 0-9 count TLD'] = url_table['pri_domain'].apply(lambda x: get_num_count(str(x)))
    url_table['num sub domains'] = url_table['url'].apply(lambda x: extract_sub_domain(str(x)))
    url_table['url_region'] = url_table['pri_domain'].apply(lambda x: get_url_region(str(x)))
    url_table['TLD_identified'] = url_table.apply(lambda row: get_generic_TLD(str(row['pri_domain']), str(row['url_region'])), axis=1)
    url_table['has_https'] = url_table['url'].apply(lambda x: has_https(x))
    url_table['root_domain'] = url_table['pri_domain'].apply(lambda x: extract_root_domain(str(x)))



    # Host Based Features
    #url_table['status_code'] = url_table['url'].apply(lambda x: get_status_code(str(x)))
    #url_table['has_redirect'] = url_table['status_code'].apply(lambda x: 1 if 300 <= x < 400 else 0)

    #url_table['whois_info'] = url_table['url'].apply(lambda x: get_whois_info(x))
    #url_table['expiry_date'] = url_table['whois_info'].apply(lambda x: x.expiration_date[0] if x and isinstance(x.expiration_date, (list, tuple)) else x.expiration_date if x and x.expiration_date else None)
    #url_table['creation_date'] = url_table['whois_info'].apply(lambda x: x.creation_date[0] if x and isinstance(x.creation_date, (list, tuple)) else x.creation_date if x and x.creation_date else None)
    #url_table['update_date'] = url_table['whois_info'].apply(lambda x: x.updated_date[0] if x and isinstance(x.updated_date, (list, tuple)) else x.updated_date if x and x.updated_date else None)

    #url_table['registrar'] = url_table['whois_info'].apply(lambda x: x.registrar[0] if x and isinstance(x.registrar, (list, tuple)) else x.registrar if x and x.registrar else None)
    #url_table['name'] = url_table['whois_info'].apply(lambda x: x.name[0] if x and isinstance(x.name, (list, tuple))else x.name if x and x.name else None)
    #url_table = url_table.drop(columns='whois_info')

    print(url_table.isnull().sum())
    url_table.fillna(0, inplace=True) # repalce all none

    print(url_table.shape)
    print(url_table.duplicated().sum())

    url_table.drop_duplicates(inplace=True)

    url_table.to_csv('output_features.csv', index=False)

    url_count = url_table.shape[0]
    print(f"Number of URLs: {url_count}")
    print("Done")