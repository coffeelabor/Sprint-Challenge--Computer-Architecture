"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111

CMP = 0b10100111  # This is an instruction handled by the ALU
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

AND = 0b10101000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255    # 256 bytes of memory
        self.pc = 0             # properties for any internal registers
        self.reg = [0] * 8      # 8 general-purpose registers
        self.fl = [0]*3         # Flag set to 3 zeros for three options
    # accept the address to read and return the value stored there
    def ram_read(self, mar):
        return self.ram[mar]
    # accept a value to write, and the address to write it to
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        filename = sys.argv[1]

        address = 0
        # Open the file
        with open(filename) as f:
            # Read all the lines
            for line in f:
                # Parse out comments
                value = line.split('#')
                # Change to ints
                value[0] = value[0].strip()
                # Ignore blank lines
                if value[0] == '':
                    continue
                val = int(value[0], 2)
                self.ram[address] = val
                address += 1       

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'CMP':
            set_cmp = self.reg[reg_a]-self.reg[reg_b]
            # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
            if set_cmp < 0:
                self.fl[0] = 1 #  Less than flag
                self.fl[1] = 0 #  Greater than flag
                self.fl[2] = 0 #  Equal to flag
            # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
            elif set_cmp > 0:
                self.fl[0] = 0  # Less than flag
                self.fl[1] = 1  # Greater than flag
                self.fl[2] = 0  # Equal to flag
            # If they are equal, set the Equal E flag to 1, otherwise set it to 0
            else:
                self.fl[0] = 0  # Less than flag
                self.fl[1] = 0  # Greater than flag
                self.fl[2] = 1  # Equal to flag
            
        # elif op == 'AND':

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            ir = self.ram[self.pc]
            # read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # Set the value of a register to an integer.
            if ir == LDI:
                # self.ram_write(operand_b, operand_a)
                self.reg[operand_a] = operand_b
                print('writing')
                self.pc += 3
            # Print numeric value stored in the given register.
            elif ir == PRN:
                print('print')
                # Print to the console the decimal integer value that is stored in the given register.
                print(self.reg[operand_a])
                self.pc += 2
            # Halt the CPU.
            elif ir == HLT:
                print('halting')
                # exit the emulator
                sys.exit(0)
            # Compare the values in two registers.
            elif ir == CMP:
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3
            # Jump to the address stored in the given register. 
            elif ir == JMP:
                # Set the PC to the address stored in the given register.
                self.pc = self.reg[operand_a]
            # jump to the address stored in the given register.
            elif ir == JEQ:
                # If greater-than flag or equal flag is set (true),
                if self.fl[2] == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            # jump to the address stored in the given register.
            elif ir == JNE:
                # If E flag is clear(false, 0),
                if self.fl[2] == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            # elif ir == AND:
