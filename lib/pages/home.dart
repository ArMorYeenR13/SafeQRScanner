import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:flutter_qr_scanner/pages/scan.dart';


//own styles
import 'package:flutter_qr_scanner/styles/colors.dart';
import 'package:flutter_qr_scanner/styles/buttons.dart';


class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBar(),


      body: homeBody(context),
    
    );
  }

  AppBar appBar() {
    return AppBar(
      toolbarHeight: 70,
      centerTitle: true,
      backgroundColor: ownSecondary,
      elevation: 0,


      //-- .. button in app bar
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


  Container homeBody(BuildContext context) {
    return Container(
      width: double.infinity,
      color: ownSecondary,
      
      child: Column(
        children: [
          //main page icon ----
          Expanded(
            flex: 4,
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SvgPicture.asset(
                    'assets/icons/qr_code_home.svg',
                    width: 250,
                    height: 250,
                    color: ownBlack,
                  ),

                  Text(
                    'QR Scan',
                    style: TextStyle(
                      fontSize: 38,
                      fontWeight: FontWeight.bold,
                      color: ownBlack,
                    ),
                  ),
                ],
              ),

            ),
          ), 

          //elevated button of home start here ----
          Expanded(
            child: Container(
              padding: const EdgeInsets.all(50),
              alignment: Alignment.center,
              child: ElevatedButton(  
                style: homeButton,
                onPressed: (){
                  debugPrint('[Button] Home -> Scan || Pressed');
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const MyScanPage()),
                  );
                },

                child: Row(
                  children: [
                    Expanded( 
                      child: Text(
                        'Let\'s Start', 
                        style: homeButtonText,
                        textAlign: TextAlign.center,
                      )
                    ),
                    
                    SvgPicture.asset(
                        'assets/icons/arrow_right.svg',
                        height: 25,
                        width: 25,
                    ),
                  ],
                )
              ),

            )
          ),  
      ],)

      
    );
  }
}