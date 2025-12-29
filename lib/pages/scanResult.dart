import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:qr_flutter/qr_flutter.dart';

import 'package:url_launcher/url_launcher.dart';

//own styles
import 'package:flutter_qr_scanner/styles/colors.dart';


//utility
import 'package:flutter_qr_scanner/utility/api_service.dart';

class ScanResult extends StatefulWidget {

  final String code;
  final Barcode barcode;
  const ScanResult({super.key  , required this.code, required this.barcode });

  @override
  State<ScanResult> createState() => _ScanResultState();
}

class _ScanResultState extends State<ScanResult> {
  bool _ownModelLoading = false;
  String _ownModelResponse = '';
  String? virusTotalResponse;
  List<int>? virusTotalResult;


  String? predictionResult;
  bool _determineColour = false;

  bool _VirusTotalLoading = false;
  

  String printBarcodeType(Barcode barcode) {
      return barcode.type.toString().split('.').last.toUpperCase();
  }


  bool _isCardMalicious() {
    if (predictionResult != null && virusTotalResult != null) {
      if (predictionResult == 'Malicious' && (virusTotalResult![0] > 1 || virusTotalResult![1] > 5)) {
        return true;
      }
    }
    return false;
  }



  Future<void> runOwnModelPrediction(String url) async {
    setState(() {
      _ownModelLoading = true; // Start loading
      _ownModelResponse = ''; // Reset response
    });

    try {
      // Make API request to the model
      final result = await ApiServices.predictUrl(url);
      setState(() {
        _ownModelResponse = result.toString(); // Update response
        List<dynamic> predictions = result['predictions'];

        predictionResult = predictions.isNotEmpty ? predictions.first : '';

     
        
      });
    } catch (e) {
      debugPrint('Error: $e');
    } finally {
      setState(() {
        _ownModelLoading = false; // Stop loading
      });
    }
  } 



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: scanResultAppBar(context),


      body: scanResultBody(context),
    
    );
  }

  AppBar scanResultAppBar(BuildContext context) {
    return AppBar(
      toolbarHeight: 70,
      title: Text(
        'Qr Scan',
        style: TextStyle(
          color: ownBlack,
          fontSize: 21,
          fontWeight: FontWeight.bold,
        )
      ),
      centerTitle: true,
      backgroundColor: ownSecondary,
      elevation: 0,

      // back button in appbar
      leading: GestureDetector(
        onTap: () {
          Navigator.pop(context);
          debugPrint('[Button] Back Button || Pressed');
        },

        child: Container(
          margin: const EdgeInsets.all(10),
          alignment: Alignment.center,
          width: 50,

          child: SvgPicture.asset(
            'assets/icons/Arrow - Left 2.svg',
            height: 35,
            width: 35,
          ),
        ),
      ),

      actions: [
        GestureDetector(
          onTap: () {
            debugPrint('[Button] Menu Button || Pressed');
          },
          child: Container(
            margin: const EdgeInsets.all(10),
            alignment: Alignment.center,
            width: 50,
            
            decoration: BoxDecoration(
            
              borderRadius: BorderRadius.circular(10),

            ),

            child: SvgPicture.asset(
              'assets/icons/menu.svg',
              height: 35,
              width: 35,
            ),
          ),
        )
      ],
    );
  }



  Container scanResultBody(BuildContext context) {
  return Container(
    padding: const EdgeInsets.all(12.0),
    child: Center( 
      child: Card( 
        color: _determineColour ? (_isCardMalicious() ? const Color.fromARGB(255, 225, 99, 90) : const Color.fromARGB(255, 135, 215, 138)) : Color.fromARGB(255, 218, 218, 218),
        elevation: 4.0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10.0), 
        ),
        child: Padding(
          padding: const EdgeInsets.all(16.0), 
          child: Column(
            mainAxisSize: MainAxisSize.min, 
            children: [
              // show qr code result
              QrImageView(
                data: widget.code,
                version: QrVersions.auto,
                size: 150,
                gapless: false,
              ),

              const Text(
                "Scan Result",
                style: TextStyle(
                 color: Colors.black54,
                 fontSize: 16,
                 fontWeight: FontWeight.bold,
                 letterSpacing: 1,
                ),
              ),


              const SizedBox(height: 10),
              Text(
                widget.code,
                style: const TextStyle(
                 color: Colors.black87,
                 fontSize: 16,
                 letterSpacing: 1,
                ),
              ),


              Text(
                "Barcode Type: ${printBarcodeType(widget.barcode)}",
                style: const TextStyle(
                 color: Colors.black54,
                 fontSize: 16,
                 fontWeight: FontWeight.bold,
                 letterSpacing: 1,
                ),
              ),

              // ---------------------------------------------------- 

              const SizedBox(height: 10),

              if (!_determineColour)
              Container(
                padding: const EdgeInsets.symmetric(vertical: 10.0),
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                  ),
                  onPressed: (_ownModelResponse.isEmpty && !_ownModelLoading) ? () async {
                    // Run own model prediction
                    await runOwnModelPrediction(widget.code); 
                    
                    // Check with VirusTotal
                    if (widget.barcode.url != null) {
                      setState(() {
                        _VirusTotalLoading = true;
                      });
                      
                      final String urlString = widget.code;
                      final String? analysisId = await ApiServices.getAnalysisReportVirusTotal(urlString);
                      virusTotalResponse = analysisId;

                      if (analysisId != null && analysisId != 'No ID found') {
                        final List<int>? stats = await ApiServices.getResults(analysisId);
                        setState(() {
                          virusTotalResult = stats; 
                        });
                      } 
                      
                      setState(() {
                        _VirusTotalLoading = false;
                      });
                    }

                    setState(() {
                      _determineColour = true; 
                    });

                  } : null,
                  child: (_ownModelResponse.isEmpty && !_ownModelLoading)
                    ? _VirusTotalLoading
                      ? const CircularProgressIndicator(
                          valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                        )
                      : const Text(
                          "Run Analysis",
                          style: TextStyle(
                            color: Colors.black87,
                            fontSize: 16,
                            letterSpacing: 1,
                          ),
                        )
                    : (_ownModelLoading
                        ? const CircularProgressIndicator() 
                        : const Text(
                            "Run Own Model",
                            style: TextStyle(
                              color: Colors.black87,
                              fontSize: 16,
                              letterSpacing: 1,
                            ),
                          )),
                ),
              ),

              if (predictionResult != null && predictionResult!.isNotEmpty)
              Text(
                "Model Predictions: $predictionResult",
                style: const TextStyle(
                  color: Colors.black54,
                  fontSize: 11,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1,
                ),
              ),

              if (virusTotalResponse != null)
                Container(
                  padding: const EdgeInsets.symmetric(vertical: 10.0),
                  child: Table(
                    border: TableBorder.all(color: Colors.grey),
                    children: [
                      TableRow(
                        children: [
                          const Text('Malicious',textAlign: TextAlign.center),
                          Text('${virusTotalResult?[0]}',textAlign: TextAlign.center),
                        ],
                      ),
                      TableRow(
                        children: [
                          const Text('Suspicious',textAlign: TextAlign.center),
                          Text('${virusTotalResult?[1]}',textAlign: TextAlign.center),
                        ],
                      ),
                      TableRow(
                        children: [
                          const Text('Undetected',textAlign: TextAlign.center),
                          Text('${virusTotalResult?[2]}',textAlign: TextAlign.center),
                        ],
                      ),
                      TableRow(
                        children: [
                          const Text('Harmless',textAlign: TextAlign.center),
                          Text('${virusTotalResult?[3]}',textAlign: TextAlign.center),
                        ],
                      ),
                      TableRow(
                        children: [
                          const Text('Timeout',textAlign: TextAlign.center),
                          Text('${virusTotalResult?[4]}',textAlign: TextAlign.center),
                        ],
                      ),
                    ],
                  ),
                ),
                

              if (_determineColour)
              Text(
                _isCardMalicious() ? "Final Prediction: Malicious" : "Final Prediction: Benign",
                style: const TextStyle(
                  color: Colors.black54,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1,
                ),
              ),
               
              // Open Link button
              SizedBox(
                width: MediaQuery.of(context).size.width - 100,
                child: ElevatedButton(
                 style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                 ),
                
                onPressed: () async {
                  if (_isCardMalicious()) {
                    bool? confirmed = await showDialog<bool>(
                      context: context,
                      builder: (BuildContext context) {
                        return AlertDialog(
                          title: const Text("Warning"),
                          content: const Text("This link may be malicious. Are you sure you want to continue?"),
                          actions: [
                            TextButton(
                              onPressed: () {
                                Navigator.of(context).pop(false); 
                              },
                              child: const Text("Cancel"),
                            ),
                            TextButton(
                              onPressed: () {
                                Navigator.of(context).pop(true); 
                              },
                              child: const Text("Continue"),
                            ),
                          ],
                        );
                      },
                    ) ?? false;

                    if (confirmed) {
                      var url = Uri.parse(widget.code);
                      if (await canLaunchUrl(url)) {
                        await launchUrl(url);
                      } else {
                        throw 'Could not launch $url';
                      }
                    }
                  } else {
                    var url = Uri.parse(widget.code);
                    if (await canLaunchUrl(url)) {
                      await launchUrl(url);
                    } else {
                      throw 'Could not launch $url';
                    }
                  }
                },
                child: const Text(
                  "Open",
                  style: TextStyle(
                      color: Colors.black87,
                      fontSize: 16,
                      letterSpacing: 1,
                    ),
                  ),
                ),
              ),




            ],
          ),
        ),
      ),
    )
  );
  }
}