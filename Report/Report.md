# Nand2Tetris Capstone Report

Name: Palakshi Kapoor
Roll number: 2501730012  
K (last two digits):12


## 1. Introduction

The aim of this project is to understand the working of the Hack computer by testing its hardware components, using a Python assembler, and developing a box-drawing program in Hack Assembly Language.

The project consists of three parts. Part A focuses on testing the CPU, Memory, and Computer chips. Part B involves converting assembly language programs into machine code using a Python assembler. Part C involves creating a program that displays a black box when a key is pressed and clears it when the key is released.

## 2. Part A – Building and Testing the Hack Computer

In Part A, I tested the CPU, Memory, and Computer chips using the Nand2Tetris Hardware Simulator.

The CPU executes instructions and performs arithmetic and logical operations. The Memory chip provides access to RAM, screen memory, and keyboard input. The Computer chip connects the CPU, Memory, and ROM32K to form the complete Hack computer.

The following test scripts were run:

- `CPU.tst`
- `Memory.tst`
- `ComputerAdd.tst`
- `ComputerMax.tst`
- `ComputerRect.tst`

All five tests completed successfully.

## 3. Part B – Python Assembler

In Part B, I used a Python program named `assembler.py` to convert Hack Assembly Language programs into 16-bit binary machine code.

The assembler uses two passes. The first pass identifies labels and stores their addresses in a symbol table. The second pass translates assembly instructions into binary machine code. It also handles predefined symbols and assigns RAM addresses to new variables.

The assembler was used with `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm` to generate their corresponding `.hack` files.

Since my assigned value is K = 12:

`12 mod 3 = 0`

Therefore, the additional requirement is to save labels and variables with their addresses in `symbols.txt`.

The assembler was also used to convert `Box.asm` into `Box.hack`.

## 4. Part C – Keyboard-Controlled Box

In Part C, I created `Box.asm`, a Hack Assembly Language program that draws a black box when a key is pressed and clears it when the key is released.

The box dimensions are based on my assigned value, K = 12.

- Starting row: 12
- Height: 20 pixels
- Width: 16 pixels

The width is calculated using the formula:

`Width = 16 × ((K mod 4) + 1)`

Since `12 mod 4 = 0`:

`Width = 16 × (0 + 1) = 16 pixels`

The screen memory starts at address 16384. Each row contains 32 words. Therefore, the starting address is:

`16384 + (32 × 12) = 16768`

The program continuously checks the keyboard using the predefined `KBD` address. When a key is pressed, it writes `-1` to the required screen memory locations to display black pixels. When the key is released, it writes `0` to clear the same locations.

The program uses a screen pointer and a row counter to process 20 rows. It advances the pointer by 32 words after each row and returns to check the keyboard again.

The program was assembled using my Python assembler and executed in the Nand2Tetris CPU Emulator.

## 5. Mistake Encountered and Correction

While assembling `Pong.asm`, the Python assembler initially reported an invalid destination instruction, `DM`. The destination handling in the assembler was corrected to support the valid destination combination. After the correction, I ran the assembler again.

This helped me understand the importance of correct instruction mappings and testing the assembler with different programs.

## 6. Conclusion

This project helped me understand the basic working of the Hack computer, hardware testing, assembly language, and machine-code generation. I learned how a two-pass assembler uses labels and symbols to translate instructions and how keyboard input and screen memory can be used to create a simple graphical program.

The final box program demonstrates the use of memory-mapped input and output, conditional jumps, and loops in Hack Assembly Language.

## 7. Project Files

The project contains the following important files:

- `CPU.hdl`
- `Memory.hdl`
- `Computer.hdl`
- `assembler.py`
- `Box.asm`
- `Box.hack`
- `symbols.txt`
- `report.md`
