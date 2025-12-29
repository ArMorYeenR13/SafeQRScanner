import 'dart:math';
import 'dart:core';
import 'dart:convert';
import 'package:crypto/crypto.dart';
import 'package:flutter/material.dart';

import 'package:flutter/services.dart';
import 'package:public_suffix/public_suffix.dart';



int wordHashing(String word) {
 List<int> bytes = utf8.encode(word);
 Digest hash = sha256.convert(bytes);
  
 
 String hexString = hash.bytes.map((byte) => byte.toRadixString(16).padLeft(2, '0')).join();
 BigInt hashValue = BigInt.parse(hexString, radix: 16);
  
 int finalHashValue = (hashValue % BigInt.from(pow(10, 8))).toInt();
 return finalHashValue;
}

//Index(['url_len', 'path_length', 'path_depth', 'query_length', 'num 0-9 count',
      //  'reserved char count', 'url shortened', 'num 0-9 count TLD',
      //  'url_region', 'has_https', 'root_domain', 'TLD_identified_Commercial',
      //  'TLD_identified_Country', 'TLD_identified_Network',
      //  'TLD_identified_Organisation', 'TLD_identified_Unknown',
      //  'TLD_identified_business', 'TLD_identified_educational',
      //  'TLD_identified_government', 'TLD_identified_information',
      //  'TLD_identified_international', 'TLD_identified_military',
      //  'TLD_identified_restricted name', 'TLD_identified_restricted pro'],

int countNum(Uri uri){
  int count = 0;
  count += uri.host.split('').where((char) => char.contains(RegExp(r'\d'))).length;
  count += uri.path.split('').where((char) => char.contains(RegExp(r'\d'))).length;

  return count;
}

int countSpecialChar(Uri uri) {
  int count = 0;
  final Set<String> specialCharacters = {'!', '*', '\'', '(', ')', ';', ':', '@', '&', '=', '+' '\$', ',', '/', '?', '%', '#', '[', ']'};
  
  count += uri.host.split('').where((char) => specialCharacters.contains(char)).length;
  count += uri.path.split('').where((char) => specialCharacters.contains(char)).length;

  return count;
}

int isUrlShortened(Uri uri){
  final List<String> shorteningServices = [
    'bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 'is.gd',
    'snipurl.com', 'short.io', 'kl.am', 'wp.me', 'to.ly', 'bit.do', 'bitly.is', 
    'tinyurl.is', 'bit.ly', 'ity.im', 'is.gd',
     '1url.com', 'tr.im', 'linktr.ee', 'tiny.cc'
  ];
 
  final String host = uri.host.toLowerCase();

  for (String service in shorteningServices) {
    if (host == service.toLowerCase()) {
      return 1; 
    }
  }
  return 0; 
}


String urlRegion(Uri uri){
  Map<String, String> ccTLDToRegion = {
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
  };

   for (String ccTLD in ccTLDToRegion.keys) {
    if (uri.host.endsWith(ccTLD)) {
      return ccTLDToRegion[ccTLD] ?? 'Global';
    }
  }
 return "Global";
}


String getGenericTLD(Uri uri) {
 Map<String, String> TLDToGeneric = {
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
 };

 if (urlRegion(uri) != "Global") {
    return "Country";
 } else {
    for (String TLD in TLDToGeneric.keys) {
      if (uri.host.endsWith(TLD)) {
        return TLDToGeneric[TLD] ?? "Unknown";
      }
    }
    return "Unknown";
 }
}

Future<String> getRootDomain(Uri uri) async {
  var suffixListString = await rootBundle.loadString('assets/models/public_suffix_list.dat');
  DefaultSuffixRules.initFromString(suffixListString);
  final parsedUrl = PublicSuffix(urlString:uri.origin);
  return parsedUrl.root;
}


Future<List<double>> preprocessUrl(String url) async{
 
  Uri uri = Uri.parse(url);

  int urlLength = url.replaceFirst(RegExp(r'https?://'), '').length;
  int pathLength = uri.path.length;
  int pathDepth = uri.pathSegments.length;
  int queryLength = uri.query.length;
  int numCount = countNum(uri);
  int specialCharCount = countSpecialChar(uri);
  int urlShortened = isUrlShortened(uri);
  int numInTLDCount = uri.host.split('').where((char) => char.contains(RegExp(r'\d'))).length;
  int url_region = wordHashing(urlRegion(uri));
  int checkHttps = uri.isScheme('https') ? 1 : 0;

  String stringRootDomain = await getRootDomain(uri);
  int rootDomain = wordHashing(stringRootDomain);

  // one hot encoded
  //'TLD_identified_Commercial','TLD_identified_Country', 'TLD_identified_Network',
      //  'TLD_identified_Organisation', 'TLD_identified_Unknown',
      //  'TLD_identified_business', 'TLD_identified_educational',
      //  'TLD_identified_government', 'TLD_identified_information',
      //  'TLD_identified_international', 'TLD_identified_military',
      //  'TLD_identified_restricted name', 'TLD_identified_restricted pro'],
  double isTLDComm = getGenericTLD(uri)=='Commercial'? 1 : 0;
  double isTLDCountry = getGenericTLD(uri)=='Country' ? 1 : 0;
  double isTLDNetwork = getGenericTLD(uri)=='Network' ? 1 : 0;
  double isTLDOrganisation = getGenericTLD(uri)=='Organisation' ? 1 : 0;
  double isTLDUnknown = getGenericTLD(uri)=='Unknown' ? 1 : 0;
  double isTLDBusiness = getGenericTLD(uri)=='business' ? 1 : 0;
  double isTLDEducational = getGenericTLD(uri)=='educational' ? 1 : 0;
  double isTLDGovernment = getGenericTLD(uri)=='government' ? 1 : 0;
  double isTLDInformation = getGenericTLD(uri)=='information' ? 1 : 0;
  double isTLDInternational = getGenericTLD(uri)=='international' ? 1 : 0;
  double isTLDmilitary = getGenericTLD(uri)=='military' ? 1 : 0;
  double isTLDName = getGenericTLD(uri)=='(restricted) name' ? 1 : 0;
  double isTLDPro = getGenericTLD(uri)=='(restricted) pro' ? 1 : 0;

  

 //Index(['url_len', 'path_length', 'path_depth', 'query_length', 'num 0-9 count',
      //  'reserved char count', 'url shortened', 'num 0-9 count TLD',
      //  'url_region', 'has_https', 'root_domain', 'TLD_identified_Commercial',
      //  'TLD_identified_Country', 'TLD_identified_Network',
      //  'TLD_identified_Organisation', 'TLD_identified_Unknown',
      //  'TLD_identified_business', 'TLD_identified_educational',
      //  'TLD_identified_government', 'TLD_identified_information',
      //  'TLD_identified_international', 'TLD_identified_military',
      //  'TLD_identified_restricted name', 'TLD_identified_restricted pro'],
  List<double> input = List.filled(24, 0);
    input[0] = urlLength.toDouble();
    input[1] = pathLength.toDouble();
    input[2] = pathDepth.toDouble();
    input[3] = queryLength.toDouble();
    input[4] = numCount.toDouble();
    input[5] = specialCharCount.toDouble();
    input[6] = urlShortened.toDouble();
    input[7] = numInTLDCount.toDouble();
    input[8] = url_region.toDouble();
    input[9] = checkHttps.toDouble();
    input[10] = rootDomain.toDouble();
    input[11] = isTLDComm.toDouble();
    input[12] = isTLDCountry.toDouble();
    input[13] = isTLDNetwork.toDouble();
    input[14] = isTLDOrganisation.toDouble();
    input[15] = isTLDUnknown.toDouble();
    input[16] = isTLDBusiness.toDouble();
    input[17] = isTLDEducational.toDouble();
    input[18] = isTLDGovernment.toDouble();
    input[19] = isTLDInformation.toDouble();
    input[20] = isTLDInternational.toDouble();
    input[21] = isTLDmilitary.toDouble();
    input[22] = isTLDName.toDouble();
    input[23] = isTLDPro.toDouble();

  // debugging
  String inputString = input.join(', '); 
  debugPrint(inputString, wrapWidth: 1024);

  return input;
}

