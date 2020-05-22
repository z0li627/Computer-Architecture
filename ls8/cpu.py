import sys
import re

PUSH = 0b01000101
POP = 0b01000110
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
CALL = 0b01010000
RET = 0b00010001
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
AND = 0b10101000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    def __init__(self):
        self.registers = [0, 0, 0, 0, 0, 0, 0, 0]
        self.registers[7] = 0xf4
        self.memory = [0] * 256
        self.pc = 0
        self.mar = 0
        self.mdr = 0
        self.eax = 0
        self.ebx = 0
        self.fl = 0

        self.branchtable = {
            PUSH: self.PUSH,
            POP: self.POP,
            HLT: self.HLT,
            LDI: self.LDI,
            PRN: self.PRN,
            CALL: self.CALL,
            RET: self.RET,
            JMP: self.JMP,
            JEQ: self.JEQ,
            JNE: self.JNE,
            MUL: self.alu,
            ADD: self.alu,
            SUB: self.alu,
            AND: self.alu,
            CMP: self.alu
        }

    def load(self, program):
        address = 0
        for i in program:
            self.memory_write(address, i)
            address += 1

    def alu(self, op, eax, ebx):
        if op == ADD:
            self.registers[eax] += self.registers[ebx]
        elif op == SUB:
            self.registers[eax] -= self.registers[ebx]    
        elif op == MUL:
            self.registers[eax] *= self.registers[ebx]
        elif op == AND:
            self.registers[eax] = self.registers[eax] & self.registers[ebx]
        elif op == CMP:
            if self.registers[eax] == self.registers[ebx]:
                self.fl = 0b00000001
            if self.registers[eax] > self.registers[ebx]:
                self.fl = 0b00000010
            if self.registers[eax] < self.registers[ebx]:
                self.fl = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")

    def memory_read(self, mar):
        mdr = self.memory[mar]
        return mdr

    def memory_write(self, mar, mdr):
        self.memory[mar] = mdr

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.memory_read(self.pc),
            self.memory_read(self.pc + 1),
            self.memory_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        while True:
            command = self.memory_read(self.pc)
            alpha = self.memory_read(self.pc + 1)
            beta = self.memory_read(self.pc +2)
            #self.trace()

            if command in self.branchtable:
                if command & 0b00100000 != 0:
                    self.branchtable[command](command, alpha, beta)
                elif command >> 6 == 0:
                    self.branchtable[command]()
                elif command >> 6 == 1:
                    self.branchtable[command](alpha)
                elif command >> 6 == 2:
                    self.branchtable[command](alpha, beta)
            else:
                print(f"Command {bin(command)} not found!")
                sys.exit(1)
            
            if command & 0b00010000 == 0:
                self.pc += (command >> 6) + 1
                
    def PUSH(self, eax):
        self.registers[7] -= 1
        self.memory[self.registers[7]] = self.registers[eax]
    
    def POP(self, eax):
        self.registers[eax] = self.memory[self.registers[7]]
        self.registers[7] += 1
    
    def HLT(self):
        sys.exit(0)

    def LDI(self, eax, ebx):
        self.registers[eax] = ebx

    def PRN(self, eax):
        print(self.registers[eax])

    def CALL(self):
        self.PUSH(self.pc + 2)
        self.pc = self.registers[self.eax]

    def RET(self):
        self.pc = self.memory[self.registers[7]]
        self.registers[7] += 1
    
    def JMP(self, eax):
        self.pc = self.registers[eax]

    def JEQ(self, eax):
        if self.fl == 0b00000001:
            self.pc = self.registers[eax]
        else:
            self.pc += 2

    def JNE(self, eax):
        if self.fl != 0b00000001:
            self.pc = self.registers[eax]
        else:
            self.pc += 2


