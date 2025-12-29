import re

#extract , preprocessing
import tldextract
from urllib.parse import urlparse
"""
Lexical Features :
#overall
- URL length
- query length
- total number of reserved char
- total number of unreserved char


- Scheme (https / http)
- Count digits in domain


#main domain
- is domain CCTLD
- domain categories
- used shortened TLD

#reserved 
- (:) if it is using a port
- (@) identify if user is used
- (#) identify fragments/ anchors
- (=) number of query assigned
- (%) URL encoding

#unreserved
- (~) has any reference
- (_,-) word joiners and seperator
- (.) if it is a TLD rather than a directory path


#path analysis
- Path length
- path depth (/)
- num count in path
- special character in path


Total 18 features
"""


def get_info_url(url):
  extracted = tldextract.extract(url)
  urlparsed = urlparse(url)

  # tldextract
  subdomain = extracted.subdomain
  domain = extracted.domain
  suffix = extracted.suffix

  # urlparse
  hostname = urlparsed.hostname
  scheme = urlparsed.scheme
  netloc = urlparsed.netloc
  port = urlparsed.port
  username = urlparsed.username
  path = urlparsed.path
  query = urlparsed.query
  fragment = urlparsed.fragment

  # print("Original:", url)
  # print("Hostname:", hostname) #no port num
  # print("Scheme:", scheme)
  # print("Subdomain:", subdomain)
  # print("Domain:", domain)
  # print("username:", username)
  # print("Suffix:", suffix)
  # print("Netloc:", netloc)  # netsoc, path to url
  # print("Port:", port)  # port, uses :
  # print("Path:", path)  # path file , uses / and .
  # print("Query:", query)  # Query , uses ? , uses = and &
  # print("Fragment:", fragment)  # Anchor, somewhere to a doc uses #

  return {
    "Hostname" : hostname,
    "Scheme": scheme,
    "Subdomain": subdomain,
    "Domain": domain,
    "Username" : username,
    "Suffix": suffix,
    "Netloc": netloc,
    "Port": port,
    "Path": path,
    "Query": query,
    "Fragment": fragment
  }

def get_overall_feature(url,query,netloc,scheme):
  #URL length
  url = url.replace('www.', '') #remove www. if exist
  protocol = ['http://', 'https://'] #dont need count http/s
  for num in protocol:
    if url.startswith(num):
      urlLengthcount = url[len(num):]

  TotalurlLength = len(urlLengthcount)

  #netloc length
  urlLength = len(netloc)

  #query length
  queryLength = len(query)

  #count of digits
  num_digits = sum(1 for char in netloc if char.isdigit())

  #count of unreserved char
  unreservedChar = set(".-_~")
  num_unreservedChar = sum(1 for char in netloc if char in unreservedChar)

  #has https
  has_https = int(scheme == 'https')

  return {
    "Total URL length": TotalurlLength,
    "netloc length": urlLength,
    "Query Length": queryLength,
    "count digits": num_digits,
    "count reserved char": num_unreservedChar,
    "has https": has_https,
  }

#-----------------------------------------------------

def get_url_region(netloc):
  # data collected from wiki
  # ISO-3166-1 with the exception ac, eu and uk  (not used gb,bv,bl,mf,sj,um)
  #".ly": "Libya",
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
    if netloc.endswith(ccTLD):
      return ccTLD_to_region[ccTLD]

  return "Global"

def get_generic_TLD(netloc,ccTLD):
  # for name and pro need eligibility so unlikely
  # edu,gov , mil , int are considered sponsered
  # source wiki
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
      if netloc.endswith(TLD):
        return TLD_to_generic[TLD]
  return "Unknown"

def url_shortened_TLD(host):
  #collected by randomly googling url shortener, some are from big companies
  # like goo.gl  and linktr.ee
  shortening_services = [
    'bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 'is.gd',
    'snipurl.com', 'short.io', 'kl.am', 'wp.me', 'to.ly', 'bit.do', 'bitly.is',
    'tinyurl.is', 'bit.ly', 'ity.im', 'is.gd',
    '1url.com', 'tr.im', 'linktr.ee', 'tiny.cc'
  ]

  if host is not None:
    host = host.lower()

  for service in shortening_services:
    if host == service.lower():
      return 1

  return 0

def get_domain_feature(hostname):

  ccTLD = get_url_region(hostname)
  gTLD = get_generic_TLD(hostname,ccTLD)


  return {
    "Country Code TLD": ccTLD,
    "Generic TLD": gTLD,
    "is shortened TLD": url_shortened_TLD(hostname),
  }


def get_url_reserved_feature(url,port,username,fragment,query):

  return {
    "has Port": 1 if port else 0,
    "has username": 1 if username else 0,
    "has fragments": 1 if fragment else 0,
    "num queries (count =)": len(query.split('&')) if query else 0 ,
    "URL encoding": url.count("%"),
  }


def get_path_feature(path):
  special_characters = set("!*'();:@&=+$,/?%#[]._-~")

  return {
    "Path length": len(path),
    "Path depth": len([segment for segment in urlparse(path).path.split('/') if segment]),
    "Path digit counts": sum(1 for char in path if char.isdigit()),
    "Path special character count": sum(1 for char in path if char in special_characters),
  }




def lexical_feature(url):
  info_table = get_info_url(url)

  overall_feature_table = get_overall_feature(url, info_table['Query'], info_table['Netloc'],info_table['Scheme'])
  overall_domain_L_table = get_domain_feature(info_table['Hostname'])
  overall_reserved_table = get_url_reserved_feature(url,info_table['Port'], info_table['Username'],
                                                    info_table['Fragment'], info_table['Query'])
  overall_path_table = get_path_feature(info_table['Path'])

  # Combine all tables into one dictionary
  combined_features = {}
  combined_features.update({"URL": url})
  combined_features.update(overall_feature_table)
  combined_features.update(overall_domain_L_table)
  combined_features.update(overall_reserved_table)
  combined_features.update(overall_path_table)

  return combined_features



