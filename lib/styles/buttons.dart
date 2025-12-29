import 'package:flutter/material.dart';
import 'package:flutter_qr_scanner/styles/colors.dart';

final ButtonStyle homeButton = ElevatedButton.styleFrom(
  backgroundColor: ownPrimary,
  minimumSize: const Size(327, 50),   
  shape: const RoundedRectangleBorder(
    borderRadius: BorderRadius.all(Radius.circular(15)),
  ),
  elevation: 5,
  shadowColor: ownBlack,
);

TextStyle homeButtonText = TextStyle(
  color: ownBlack,
  fontSize: 18,
  fontWeight: FontWeight.bold,
);