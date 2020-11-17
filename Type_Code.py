import re

def label(fileName):                                         #labelAddr ใช้อ้างอิงบรรทัดที่จะ jump
    label_addr = {}                                              #เก็บบรรทัด และเลขบรรทัด
    f2 = open(fileName, "r")
    pc = 0
    for line in f2:
        show = re.split(r"\s+", line,2)                         #ตัดเป็น index [start,{45,234}]
        if show[0] != '' :                                      #เช็คไม่มี label
            if show[0] not in label_addr:                       #เช็คไม่ให้ใช้ label ซ้ำ
                label_addr[show[0]] = pc                         #เก็บ label map กับเลขบรรทัด(บรรทัดที่จะ jump ไป)
            else:
                print('Duplicate label >> ' + test1[0])
                exit(1)                                          #ทำงานเมื่อมี label ซ้ำ 
        pc+=1                                                    #บรรทัด ++
    return label_addr


#GenCode 
#-------------------------------------------------------------------------------------
def gen_16twoCom(intNumber):#2's complement 16bits
    if intNumber < 0:#ถ้าเป็นเลขลบ
        if intNumber >= -32768:
            negNum = intNumber*-1
            top = bin(32767)[2:].zfill(15)
            bi = bin(negNum)[2:].zfill(15)
            negate =  int(top,2) - int(bi,2) + int('1',2)
            result = '1'+bin(negate)[2:].zfill(15)
            return result #ได้เลขฐานสอง
        else:#ถ้าน้อยกว่า -32768 = overflow
            print("Overflow Number OffsetField")
            exit(1)
    else:#ถ้าไม่เป็นเลขลบ
        result = bin(intNumber)[2:].zfill(16)
        if intNumber < 32768:
            return result
        else:#ถ้ามากกว่าหรือเท่ากับ 32768 = overflow
            print("Overflow Number OffsetField")
            exit(1)

def gen_32twoCom(intNum): #2's complement 32bits 
    if intNum < 0: #ถ้าเป็นเลขลบ
        if intNum >= -2147483648:
            negNum = intNum*-1
            top = bin(2147483647)[2:].zfill(31)
            bi = bin(negNum)[2:].zfill(31)
            negate =  int(top,2) - int(bi,2) + int('1',2)
            result = '1'+bin(negate)[2:].zfill(31)
            return result #ได้เลขฐานสอง
        else: #ถ้าน้อยกว่า -2147483648 = overflow
            print("Overflow Number OffsetField")
            exit(1)
    else: #ถ้าไม่เป็นเลขลบ
        result = bin(intNum)[2:].zfill(32)
        if intNum < 2147483648 :
            return result
        else: #ถ้ามากกว่าหรือเท่ากับ 2147483648 = overflow
            print("Overflow Number OffsetField")
            exit(1)

#--------------------------------------------------------------------------------------

#Type_Code 
def R_type(line_split):
    inst = line_split[1]
    regA = line_split[2]
    regB = line_split[3]
    regDes = line_split[4]
    opcode = ''
    bi_regA = bin(int(regA))[2:].zfill(3) #เปลี่ยนค่าใน regA เป็นเลขฐานสอง
    bi_regB = bin(int(regB))[2:].zfill(3) #เปลี่ยนค่าใน regฺB เป็นเลขฐานสอง
    bi_regDes = bin(int(regDes))[2:].zfill(3) #เปลี่ยนค่าใน desReg เป็นเลขฐานสอง
    if inst == 'add':
        opcode+='000' #add opcode = 000
    elif inst == 'nand':
        opcode+='001' #nand opcode = 001
    machineCodeInst = '0000000'+opcode+bi_regA+bi_regB+'0000000000000'+bi_regDes #R-type format
    return machineCodeInst




def I_type(line_split,PC,label_addr):
    inst = line_split[1]
    regA = line_split[2]
    regB = line_split[3]
    off = line_split[4]
    opcode = ''
    bi_regA = bin(int(regA))[2:].zfill(3) #เปลี่ยนค่าใน regA เป็นเลขฐานสอง
    bi_regB = bin(int(regB))[2:].zfill(3) #เปลี่ยนค่าใน regฺB เป็นเลขฐานสอง
    bi_offset = ''
    if inst == 'lw':
        opcode+='010' #lw opcode = 010
    elif inst == 'sw':
        opcode+='011' #sw opcode = 011
    elif inst == 'beq':
        opcode+='100' #beq opcode = 100
    
    if off.lstrip('-').isdigit() :
        bi_offset+=gen_16twoCom(int(off))
    else:
        sym_addr = off
        intOffset = label_addr[sym_addr] - (PC+1)
        if intOffset < -32768 or intOffset > 32767:
            print('overflow reference address')
        if sym_addr in label_addr:
            if inst == 'beq':
                bi_offset+=gen_16twoCom(intOffset)
            else:
                bi_offset+=bin(int(label_addr[sym_addr]))[2:].zfill(16)
    I_code = '0000000' + opcode + bi_regA + bi_regB + bi_offset#I-type format
    
    return I_code


def J_type(line_split):
    
    regA = line_split[2]
    regB = line_split[3]
    opcode = '101' #Jtype opcode = 101
    bi_regA = bin(int(regA))[2:].zfill(3) #เปลี่ยนค่าใน regA เป็นเลขฐานสอง
    bi_regB = bin(int(regB))[2:].zfill(3) #เปลี่ยนค่าใน regB เป็นเลขฐานสอง
    return '0000000'+opcode+bi_regA+bi_regB+'0000000000000000' #J-type format

def O_type(line_split):
    opcode = ''
    if line_split[1] == 'halt':
        opcode+='110' #halt opcode = 110
    elif line_split[1] == 'noop':
        opcode+='111' #noop opcode = 111
        
    return '0000000'+opcode+'0000000000000000000000' #O-type format



def sign_extend32(offset16):
    if int(offset16,2) & (1<<15):
        for n in range(0,16) :
            offset16 = "1" + offset16 #extend ด้วย 1
    else:
        for n in range(0,16) :
            offset16 = "0" + offset16 #extend ด้วย 0
    
    offset32 = offset16
    return offset32

def sign_extend(value, bits):
    if len(value) <= bits :
        x = list(value)
        if x[0] == "0": #ถ้า sign bit เป็น 0 (เป็นเลขบวก)
            for n in range(bits - len(value)) :
                value = "0" + value #extend ด้วย 0
        else: #ถ้า sign bit เป็น 1 (เป็นเลขลบ)
            for n in range(bits - len(value)) :
                value = "1" + value #extend ด้วย 1
    return value




def twoCom_ToInt(biNumber32):#แปลง 2's complement เป็นฐานสิบ
    if biNumber32[0] == '0': #ถ้า sign bit เป็น 0 (เป็นเลขบวก)
        return int(biNumber32,2) 
    else: #ถ้า sign bit เป็น 1 (เป็นเลขลบ)
        return int('-'+str(int(bin(4294967296-int(biNumber32,2))[2:].zfill(32),2)))


        

