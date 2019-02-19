# ABOUT

A work-around for AppleEvents sandboxing preventing Glyphs from running Mekkablue's 'Steal kerning from InDesign' script.

# INSTALLATION

Put both these python files into the Glyphs scripts folder. Any subdirectory is fine, as long as both are in the same directory.

# USAGE

Set everything up as you would for Mekkablue's script, with an optically-kerned text frame in InDesign.

Then launch 'Steal InDesign Kerning Data.py' as a standalone script – not from the Glyphs macro window. This will extract the kerning data from InDesign and save it in a txt file.

Next, run 'Apply Stolen Kerning Data.py' through Glyphs, as you would for any other Glyphs script – it will apply the kerning data stored in the txt file.
