from enum import Enum



license_terms = {
    1: ("Distribute", "Distribute original or modified derivative works", "Rights"),
    2: ("Modify", "Modify the software and create derivatives", "Rights"),
    3: ("Commercial Use", "Use the software for commercial purposes", "Rights"),
    4: ("Relicense", "Add other licenses with the software", "Rights"),
    5: ("Hold Liable", "Hold the author responsible for subsequent impacts", "Rights"),
    6: ("Use Patent Claims", "Practice patent claims of contributors to the code", "Rights"),
    7: ("Sublicense", "Incorporate the work into something that has a more restrictive license", "Rights"),
    8: ("Statically Link", "The library can be compiled into the program linked at compile time rather than runtime", "Rights"),
    9: ("Private Use", "Use or modify software freely without distributing it", "Rights"),
    10: ("Use Trademark", "Use contributors’ names, trademarks or logos", "Rights"),
    11: ("Place Warranty", "Place warranty on the software licensed", "Rights"),
    12: ("Include Copyright", "Retain the copyright notice in all copies or substantial uses of the work.", "Obligations"),
    13: ("Include License", "Include the full text of license in modified software", "Obligations"),
    14: ("Include Notice", "Include that NOTICE when you distribute if the library has a NOTICE file with attribution notes", "Obligations"),
    15: ("Disclose Source", "Disclose your source code when you distribute the software and make the source for the library available", "Obligations"),
    16: ("State Changes", "State significant changes made to software", "Obligations"),
    17: ("Include Original", "Distribute copies of the original software or instructions to obtain copies with the software", "Obligations"),
    18: ("Give Credit", "Give explicit credit or acknowledgement to the author with the software", "Obligations"),
    19: ("Rename", "Change software name as to not misrepresent them as the original software", "Obligations"),
    20: ("Contact Author", "Get permission from author or contact the author about the module you are using", "Obligations"),
    21: ("Include Install Instructions", "Include the installation information necessary to modify and reinstall the software", "Obligations"),
    22: ("Compensate for Damages", "Compensate the author for any damages caused by your work", "Obligations"),
    23: ("Pay Above Use Threshold", "Pay the licensor after a certain amount of use", "Obligations")
}


class Attitude(Enum):
    MUST = 1
    CAN = 2
    CANNOT = 3 
    NOMENTIONED = 4
