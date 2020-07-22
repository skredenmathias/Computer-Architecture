"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, ram=None, reg=None, pc=0):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = pc
        self.branch_table = {
            0b10000010:self.LDI,
            0b01000111:self.PRN,
            0b00000001:self.HLT,
            0b10100010:self.MUL
        }


    def load(self, filename):
        """Load a program into memory."""
        with open(filename) as f:
            address = 0

            for line in f:
                line = line.split('#')

                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue

                self.ram[address] = v
                address += 1


    def LDI(self, op_a, op_b):
        reg_num = op_a
        value = op_b
        self.reg[reg_num] = value
        self.pc += 3

    def PRN(self, op_a, op_b=None):
        reg_num = op_a
        print(self.reg[reg_num])
        self.pc += 2

    def HLT(self, op_a=None, op_b=None):
        exit()
        self.pc += 1

    def MUL(self, op_a, op_b):
        reg_num_a = op_a
        reg_num_b = op_b
        self.reg[reg_num_a] *= self.reg[reg_num_b]
        self.pc += 3


    def ram_read(self, MAR):
        '''reads RAM value at pc index'''
        return self.ram[MAR]


    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

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
        running = True
        while running:
            self.trace()
            IR = self.ram[self.pc]
            op_a, op_b = self.ram_read(self.pc+1), self.ram_read(self.pc+2)

            if IR in self.branch_table:
                action = self.branch_table[IR]
                action(op_a, op_b)

            else:
               self.pc += 1


            # # LDI:
            # if IR == 0b10000010:
            #     reg_num = operand_a
            #     value = operand_b
            #     self.reg[reg_num] = value
            #     self.pc += 3
            # # PRN:
            # elif IR == 0b01000111:
            #     reg_num = operand_a
            #     print(self.reg[reg_num])
            #     self.pc += 2

            # elif IR == 0b00000001:
            #     running = False
            #     self.pc += 1

            # else:
            #     self.pc += 1

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram_write(instruction, address)
        #     address += 1