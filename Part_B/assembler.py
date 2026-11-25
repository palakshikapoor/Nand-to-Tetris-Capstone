
import sys
from pathlib import Path

DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|A": "0010101",
    "A|D": "0010101",
    "D|M": "1010101",
    "M|D": "1010101"
}

PREDEFINED = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

PREDEFINED.update({f"R{i}": i for i in range(16)})


def clean_lines(path):
    result = []

    for line_no, raw in enumerate(
        Path(path).read_text(encoding="utf-8").splitlines(), 1
    ):
        line = raw.split("//", 1)[0].strip()

        if line:
            result.append((line_no, line))

    return result


def assemble(source):
    lines = clean_lines(source)
    symbols = dict(PREDEFINED)
    labels = {}
    variables = {}
    rom = 0

    # PASS 1: Find label addresses.
    for line_no, line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()

            if not label or label in symbols:
                raise ValueError(
                    f"Line {line_no}: invalid or duplicate label '{label}'"
                )

            symbols[label] = rom
            labels[label] = rom
        else:
            rom += 1

    # PASS 2: Translate instructions into binary.
    next_var = 16
    machine_code = []

    for line_no, line in lines:
        if line.startswith("(") and line.endswith(")"):
            continue

        if line.startswith("@"):
            symbol = line[1:].strip()

            if not symbol:
                raise ValueError(
                    f"Line {line_no}: empty A-instruction"
                )

            if symbol.isdigit():
                value = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_var
                    variables[symbol] = next_var
                    next_var += 1

                value = symbols[symbol]

            if not 0 <= value <= 32767:
                raise ValueError(
                    f"Line {line_no}: A-instruction value out of range"
                )

            machine_code.append(format(value, "016b"))

        else:
            instruction = "".join(line.split())

            if instruction.count(";") > 1:
                raise ValueError(
                    f"Line {line_no}: invalid jump instruction"
                )

            if ";" in instruction:
                left, jump = instruction.split(";", 1)
            else:
                left, jump = instruction, ""

            if left.count("=") > 1:
                raise ValueError(
                    f"Line {line_no}: invalid destination instruction"
                )

            if "=" in left:
                dest, comp = left.split("=", 1)
            else:
                dest, comp = "", left

            # Accept valid destination letters in any order:
            # DM, MD, AD, DA, AMD, ADM, and so on.
            if any(register not in "ADM" for register in dest):
                raise ValueError(
                    f"Line {line_no}: invalid dest '{dest}'"
                )

            if len(set(dest)) != len(dest):
                raise ValueError(
                    f"Line {line_no}: duplicate register in dest '{dest}'"
                )

            # Convert destination to canonical A-D-M order.
            dest = "".join(
                register for register in "ADM"
                if register in dest
            )

            if comp not in COMP:
                raise ValueError(
                    f"Line {line_no}: invalid comp '{comp}'"
                )

            if dest not in DEST:
                raise ValueError(
                    f"Line {line_no}: invalid dest '{dest}'"
                )

            if jump not in JUMP:
                raise ValueError(
                    f"Line {line_no}: invalid jump '{jump}'"
                )

            machine_code.append(
                "111" + COMP[comp] + DEST[dest] + JUMP[jump]
            )

    return machine_code, labels, variables


def write_lines(path, lines):
    # Write one item per line with real newline characters.
    Path(path).write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
        newline="\n"
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py filename.asm")
        sys.exit(1)

    source = Path(sys.argv[1])

    try:
        machine_code, labels, variables = assemble(source)

        # Save the machine code beside the source file.
        hack_file = source.with_suffix(".hack")
        write_lines(hack_file, machine_code)

        # K = 12: save all labels and variables with their addresses.
        symbol_file = source.parent / "symbols.txt"

        symbol_lines = [
            f"{name}={address}"
            for name, address in sorted(
                {**labels, **variables}.items(),
                key=lambda item: (item[1], item[0])
            )
        ]

        write_lines(symbol_file, symbol_lines)

        # Validate every generated machine instruction.
        for line_no, instruction in enumerate(machine_code, 1):
            if len(instruction) != 16 or any(
                bit not in "01" for bit in instruction
            ):
                raise ValueError(
                    f"Invalid machine code on output line {line_no}"
                )

        print(
            f"Assembly successful: {hack_file.name} "
            f"({len(machine_code)} instructions)"
        )
        print(f"Symbol table saved to: {symbol_file.name}")

    except (ValueError, OSError) as error:
        print(f"Assembly error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
