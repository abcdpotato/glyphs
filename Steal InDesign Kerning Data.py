# Steal kerning data from InDesign: based on Mekkablue's Steal kerning from InDesign.py
# -*- coding: utf-8 -*-
__doc__="""
Use the font in InD (set up a document with one text box on the first page, set the kerning method to Optical), then run this script.
"""

import io

from Foundation import NSAppleScript, NSAppleEventDescriptor


def glyphNameForLetter( letter ):
	glyphName = False
	if len(letter) > 0:
		#letter = letter[0]
		utf16value = "%.4X" % ord(letter)
		glyphName = Glyphs.glyphInfoForUnicode( utf16value ).name
	return glyphName

def runAppleScript(scriptSource, args=[]):
	s = NSAppleScript.alloc().initWithSource_(scriptSource)
	result, error = s.executeAndReturnError_(None)
	if error:
		print "AppleScript Error:"
		print error
		print "Tried to run:"
		for i, line in enumerate(scriptSource.splitlines()):
			print "%03i"%(i+1), line
		return False
	if result:
		return result.stringValue()
	else:
		return True

# Determine InDesign application name (for use in the AppleScripts):

getInDesign = """
set InDesign to choose application with title "Please choose Adobe InDesign"
InDesign as string
"""

#indesign = "Adobe InDesign CC"
indesign = runAppleScript(getInDesign)
print "Accessing: %s" % indesign

# Define AppleScripts to be run later:

getKernValuesFromInDesign = """
set kernvalues to ""
tell application "%s"
	tell front document
		tell parent story of first text frame
			repeat with i from 1 to (count characters) - 1
				try
					set kernvalue to (kerning value of insertion point 2 of character i) as integer
					set kernvalueline to character i & character (i + 1) & " " & kernvalue
					set kernvalues to kernvalues & kernvalueline & "\n"
				end try
			end repeat
		end tell
	end tell
end tell
kernvalues
""" % indesign

getNameOfDocument = """
tell application "%s"
	tell front document
		name
	end tell
end tell
""" % indesign

getTextOfFrame = """
tell application "%s"
	tell front document
		contents of first text frame
	end tell
end tell
""" % indesign

getNameOfFont = """
tell application "%s"
	tell front document
		tell first text frame
			tell character 1 of parent story
				name of applied font
			end tell
		end tell
	end tell
end tell
""" % indesign


# Execute AppleScripts and store results in variables:

# Extract document name and report:
docName = runAppleScript( getNameOfDocument )
docName = docName.strip()
print "Extracting kerning from doc: %s" % docName

# Extraxt text and report:
frameText = runAppleScript( getTextOfFrame )
#frameText = "%.60s..." % frameText.strip()
frameText = frameText.strip()
print "Found text: %s" % frameText

# Extract font name and report:
fontName = runAppleScript( getNameOfFont )
fontName = fontName.replace("\t", " ").replace("font ","").strip()
print "Found font: %s" % fontName



# Extract kern strings and report:
print "Getting kerning values from inDesign..."
kernInfo = runAppleScript( getKernValuesFromInDesign )
print kernInfo

with io.open("Stolen Kerning Data.txt", "w", encoding='utf8') as outputfile:
  outputfile.write(kernInfo)




