import 'package:flutter/material.dart';
import 'package:flutter_qr_scanner/pages/home.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0.0,
        )
      ),

      home: const MyHomePage(),
      title: 'Qr Scanner',
      debugShowCheckedModeBanner: false,
    );
  }
}


