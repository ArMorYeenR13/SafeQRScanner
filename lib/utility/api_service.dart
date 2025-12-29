import 'package:http/http.dart' as http;
import 'dart:convert';


class ApiServices {
  static Future<Map<String, dynamic>> predictUrl(String url) async {
    const apiUrl = 'http://10.132.229.11:5000/predict';
    final headers = <String, String>{'Content-Type': 'application/json'};
    final body = jsonEncode({'url': url});

    final response = await http.post(Uri.parse(apiUrl), headers: headers, body: body);

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
      
    } else {
      throw Exception('Failed to predict URL: ${response.statusCode}');
    }
  }

  static Future<String?> getAnalysisReportVirusTotal(String url) async {
    String formData = 'url=' + Uri.encodeComponent(url);
    final response = await http.post(
      Uri.parse('https://www.virustotal.com/api/v3/urls'),
      headers: {
        'x-apikey': 'I have ommited the key :) will be in env and used in production only',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    );

    if (response.statusCode == 200) {
      final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
      return jsonResponse['data']['id'] ?? 'No ID found';
    } else if (response.statusCode == 400) {
      return 'Failed to check $url with VirusTotal';
    } else {
      return 'it shouldnt be here';
    }
  }

  static Future<List<int>> getResults(String analysisId) async {
    Future<bool> isAnalysisCompleted(String analysisId) async {
      final response = await http.get(
        Uri.parse('https://www.virustotal.com/api/v3/analyses/$analysisId'),
        headers: {
          'x-apikey': 'I have ommited the key :) will be in env and used in production only',
        },
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        final String status = jsonResponse['data']['attributes']['status'];
        return status == 'completed';
      } else {
        throw Exception('Failed to check analysis status');
      }
    }

    while (!await isAnalysisCompleted(analysisId)) {
      await Future.delayed(Duration(seconds: 5)); // Wait for 5 seconds before checking again
    }

    // only  get result once analysis is done
    final response = await http.get(
      Uri.parse('https://www.virustotal.com/api/v3/analyses/$analysisId'),
      headers: {
        'x-apikey': 'I have ommited the key :) will be in env and used in production only',
      },
    );

    if (response.statusCode == 200) {
      final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
      final Map<String, dynamic> stats = jsonResponse['data']['attributes']['stats'];
      return [
        stats['malicious'],
        stats['suspicious'],
        stats['undetected'],
        stats['harmless'],
        stats['timeout'],
      ];
    } else {
      throw Exception('Failed to load analysis report');
    }
  }
}