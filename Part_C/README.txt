K=12 calculation:
Start row = 12
Height = 20 rows
Width = 16 * ((12 mod 4)+1) = 16 pixels (one 16-bit word)
First screen word address = 16384 + 32*12 = 16768
Run: python ../Part_B/assembler.py Box.asm (or copy assembler.py into this folder).
The generated Box.hack is included.
