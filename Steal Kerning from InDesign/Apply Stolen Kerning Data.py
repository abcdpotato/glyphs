#MenuTitle: Apply Stolen kerning Data
# based on Mekkablue's Steal kerning from InDesign.py
# -*- coding: utf-8 -*-
__doc__="""
"""

import io

from Foundation import NSAppleScript, NSAppleEventDescriptor

thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
thisFontMasterID = thisFontMaster.id # active master id
listOfSelectedLayers = thisFont.selectedLayers # active layers of selected glyphs

# brings macro window to front and clears its log:
Glyphs.clearLog()
Glyphs.showMacroWindow()

def glyphNameForLetter( letter ):
	glyphName = False
	if len(letter) > 0:
		#letter = letter[0]
		utf16value = "%.4X" % ord(letter)
		glyphName = Glyphs.glyphInfoForUnicode( utf16value ).name
	return glyphName




# Load kern strings and report:
kernInfo = io.open('Stolen Kerning Data.txt', 'r', encoding='utf8').read()
print "Applying kerning to: %s, Master: %s\n" % (thisFont.familyName, thisFontMaster.name)

# Parse kern strings and set kerning in the font:
for thisline in kernInfo.splitlines():
	if len(thisline) > 3:
		leftSide = glyphNameForLetter(thisline[0])
		rightSide = glyphNameForLetter(thisline[1])
		try:
			kernValue = float(thisline[3:])
			if kernValue:
				thisFont.setKerningForPair(thisFontMasterID, leftSide, rightSide, kernValue)
				print "  Kerning for %s-%s set to %i." % (leftSide, rightSide, kernValue)
			else:
				print "  No kerning between %s-%s. Ignored." % (leftSide, rightSide)
		except Exception as e:
			print "  ERROR: Could not set kerning for %s-%s (%i)." % (leftSide, rightSide, kernValue)
