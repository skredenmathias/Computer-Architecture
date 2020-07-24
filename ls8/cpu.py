"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self, ram=None, reg=None, pc=0, SP=None, FL=0, FL_L=0, FL_G=0):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = pc
        self.SP = 7
        self.reg[self.SP] = 244
        self.FL = FL
        self.FL_L = FL_L
        self.FL_G = FL_G
        self.branch_table = {
            # ALU
            0b10100000:self.ADD,
            # SUB  0b10100001 
            0b10100010:self.MUL,
            # DIV  0b10100011
            # MOD  0b10100100

            # INC  0b01100101
            # DEC  0b01100110

            0b10100111:self.CMP,

            # AND  0b10101000
            # NOT  0b01101001
            # OR   0b10101010
            # XOR  0b10101011
            # SHL  0b10101100
            # SHR  0b10101101

            # PC mutators
            0b01010000:self.CALL,
            0b00010001:self.RET,

            # 0b01010010:self.INT,
            # 0b00010011:self.IRET,

            0b01010100:self.JMP,
            0b01010101:self.JEQ,
            0b01010110:self.JNE,
            # 0b01010111:self.JGT,
            # 0b01011000:self.JLT,
            #  0b01011001:self.JLE,
            # 0b01011010:self.JGE,

            # Other
            # 0b00000000:self.NOP,

            0b00000001:self.HLT,

            0b10000010:self.LDI,

            # 0b10000011:self.LD,
            # 0b10000100:self.ST,

            0b01000101:self.PUSH,
            0b01000110:self.POP,

            0b01000111:self.PRN,
            # 0b01001000:self.PRA
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


    def ADD(self, op_a, op_b):
        reg_num_a = op_a
        reg_num_b = op_b
        self.reg[reg_num_a] += self.reg[reg_num_b]
        self.pc += 3


    def PUSH(self, op_a, op_b=None):
        # Decrement SP
        self.reg[self.SP] -= 1
        # Get the value from RAM instruction
        reg_num = op_a
        value = self.reg[reg_num]
        # Find the index in the register
        top_of_stack_addr = self.reg[self.SP]
        # Store it
        self.ram[top_of_stack_addr] = value
        self.pc += 2


    def POP(self, op_a, op_b=None):
        reg_num = op_a
        self.reg[reg_num] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        self.pc += 2


    def CALL(self, op_a, op_b=None):
        return_addr = self.pc + 2
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = return_addr
        reg_num = op_a
        self.pc = self.reg[reg_num]


    def RET(self, op_a=None, op_b=None):
        self.pc = self.ram[self.reg[self.SP]]


    def CMP(self, op_a, op_b):
        reg_num1 = op_a
        reg_num2 = op_b
        registerA = self.reg[reg_num1]
        registerB = self.reg[reg_num2]

        # if registerA < registerB:
        #     self.FL_L = 1
        # elif registerA > registerB:
        #     self.FL_G = 1
        if registerA == registerB:
            self.FL = 1
        self.pc += 3


    def JMP(self, op_a, op_b=None):
        reg_num = op_a
        self.pc = self.reg[reg_num]


    def JEQ(self, op_a, op_b=None):
        if self.FL == 1:
            self.JMP(op_a)
        else:
            self.pc += 2


    def JNE(self, op_a, op_b=None):
        if self.FL == 0:
            self.JMP(op_a)
        else:
            self.pc += 2


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