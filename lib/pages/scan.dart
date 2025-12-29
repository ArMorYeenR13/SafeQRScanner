import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
//own styles
import 'package:flutter_qr_scanner/styles/colors.dart';
import 'package:flutter_qr_scanner/pages/scanResult.dart';





class MyScanPage extends StatefulWidget {
  const MyScanPage({super.key});
  

  @override
  State<MyScanPage> createState() => _MyScanPageState();
  
}



class _MyScanPageState extends State<MyScanPage> {
  bool isScanCompleted = false;
  MobileScannerController controller = MobileScannerController(
    detectionSpeed: DetectionSpeed.noDuplicates,
    facing: CameraFacing.back,
    torchEnabled: false,
  );

  bool isStarted = true;
  double _zoomFactor = 0.0;
  final double zoomSpeed = 0.01;


 


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: scanAppBar(context),


      body: scanBody(context),
    
    );
  }

  AppBar scanAppBar(BuildContext context) {
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




  Container scanBody(BuildContext context) {
    return Container(
      width: double.infinity,
      color: ownSecondary,

      child: GestureDetector(
        onScaleUpdate: (ScaleUpdateDetails details) {
        // Handle pinch-to-zoom here
          setState(() {
            _zoomFactor = (_zoomFactor * details.scale * zoomSpeed).clamp(0.0, 1.0);
            controller.setZoomScale(_zoomFactor);

          });
        },
        child: Stack(
          children: [
            Expanded(
              flex: 6,
              child: MobileScanner(
                controller: controller,
                
        
                onDetect: (capture) {
                  final List<Barcode> barcodes = capture.barcodes;
                  for (final barcode in barcodes) {
                    debugPrint('Barcode found! ${barcode.rawValue}');
                    String code = barcode.rawValue ?? '---';
                    isScanCompleted = true;
                    
        
                    Navigator.push(
                      context, 
                      MaterialPageRoute(
                        builder: (context) => ScanResult(
                          code: code,
                          barcode: barcode,
                        )
                      )
                    );
                  }
                },
              ),
            ),
            Positioned(
              bottom: 10,
              left: 10,
              right: 10,
              child: Container(
                padding: EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Color.fromARGB(83, 26, 25, 25), 
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    IconButton(
                    color: Colors.white,
                    icon: ValueListenableBuilder(
                        valueListenable: controller.torchState,
                        builder: (context, state, child) {
                          switch (state) {
                            case TorchState.off:
                              return const Icon(Icons.flash_off, color: Colors.grey);
                            case TorchState.on:
                              return const Icon(Icons.flash_on, color: Colors.yellow);
                          }
                        },
                    ),
                   
        
                    
                    iconSize: 32.0,
                    onPressed: () => controller.toggleTorch(),
                    ),
                    Slider(
                      max: 100.0,
                      divisions: 100,
                      value: _zoomFactor,
                      
                      onChanged: (value) {
                        setState(() {
                          _zoomFactor = value;
                          controller.setZoomScale(value/100);
                        });
                      },

                      activeColor: Color(0xFFA5D8FF),
                    ),
        
        
        
                    IconButton(
                    color:  Colors.grey,
                    icon: ValueListenableBuilder(
                        valueListenable: controller.cameraFacingState,
                        builder: (context, state, child) {
                          switch (state) {
                            case CameraFacing.front:
                              return const Icon(Icons.camera_front);
                            case CameraFacing.back:
                              return const Icon(Icons.camera_rear);
                          }
                        },
                    ),
                    iconSize: 32.0,
                    onPressed: () => controller.switchCamera(),
                    ),
                    SizedBox(height: 10),
                    
                  ],
                ),
        
        
        
                
              ),
            ),
          ],
        ),
      ),
    );
  }  

}

