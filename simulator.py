import re
from Type_Code import gen_16twoCom, gen_32twoCom, sign_extend32,twoCom_ToInt
from assembler import Assembler
from printState import printState

def simulate(PC, reg, mem):                                                                                                         #เอา mem มาอ่านแต่ละ PC เพื่อเอามาดูการทำงานในแต่ละคำสั่ง
    count = 1                                                                                                                           #นับจำนวนคำสั่่งที่ทำ
    for i in range(0, 8):           
        reg[i] = 0                                                                                                                   #เคลียร์ reg ให้เป็น 0 เพื่อทำการ simulate ใหม่ได้
    firstRange = 31
    lastRange = 32
    while PC < len(mem):                                                            

        printState(PC,reg,mem)                                                                                                          #go to printState.py //ปริ้น state ก่อนที่จะทำ แต่ละ instruction
        machineCode = gen_32twoCom(int(mem[PC]))                                                                                    #go to Type_Code.py  //จะได้ machineCode มาเป็น string  
        opcode = machineCode[firstRange-24:lastRange-22]                                                                                     #เก็บ opcode ที่ได้มาของแต่ละบรรทัด
        A = int(machineCode[firstRange-21:lastRange-19], 2)                                                                                  #ใช้อ้างตำแหน่ง regA ,regB ,Des
        B = int(machineCode[firstRange-18:lastRange-16], 2)
        Des = int(machineCode[firstRange-2:lastRange-0], 2)      
        offset = int(twoCom_ToInt(sign_extend32( machineCode[firstRange-15:lastRange-0])))     
        count+=1
        
        if opcode == '110':  #halt                                                                                                                  #เช็ค opcode ว่าเป็นคำสั่งไหน ?
            PC = PC + 1
            count-=1
            break
        elif opcode == '000': #add
            reg[Des] = int(reg[A]) + int(reg[B])
        elif opcode == '001': #nand
            AandB = twoCom_ToInt( gen_32twoCom( twoCom_ToInt(gen_32twoCom(reg[A])) &  twoCom_ToInt(gen_32twoCom(reg[B]))))
            AnandB = gen_32twoCom(~AandB)
            reg[Des] = twoCom_ToInt(AnandB)
        elif opcode == "010": #lw
            reg[B] = int(mem[int(reg[A])+offset])
        elif opcode == '011': #sw
            mem[int(reg[A])+offset] = int(reg[B])
        elif opcode == '100': #beq
            if int(reg[A]) == int(reg[B]):
                PC = PC + 1 + offset
                continue
        elif opcode == '101': #jalr
            if A == B:
                reg[B] = PC + 1
                PC = PC + 1
                reg[0] = 0                                                                                                               #reg[0] ต้องเป็น 0 ตลอด 
                continue
            else:
                reg[B] = PC + 1
                PC = reg[A]
                reg[0] = 0
                continue 
        elif opcode == '111': #noop
            pass
                  


        PC += 1
        

    print("machine halted ")
    print("total of "+str(count)+ " instructions executed")
    print()
    print("final state of machine:")
    print()
    printState(PC,reg,mem)  
    


