import re
import Type_Code as c 
import  assembler as a
import printState  as p


def simulate(PC, reg, mem): #เอา mem มาอ่านแต่ละ PC เพื่อเอามาดูการทำงานในแต่ละคำสั่ง
    count = 1 #นับจำนวนคำสั่่งที่ทำ
    for i in range(0, 8):           
        reg[i] = 0 #เคลียร์ reg ให้เป็น 0 เพื่อทำการ simulate ใหม่ได้
    firstRange = 31
    lastRange = 32
    while PC < len(mem):                                                            

        p.printState(PC,reg,mem)                                                                                                          #go to printState.py //ปริ้น state ก่อนที่จะทำ แต่ละ instruction
        machineCode = c.gen_32twoCom(int(mem[PC]))                                                                                    #go to Type_Code.py  //จะได้ machineCode มาเป็น string  
        opcode = machineCode[firstRange-24:lastRange-22] #bit 22-24 เป็น opcode                                                                                    #เก็บ opcode ที่ได้มาของแต่ละบรรทัด
        A = int(machineCode[firstRange-21:lastRange-19], 2) #ให้ bit 19-21 เป็น A                                                                                #ใช้อ้างตำแหน่ง regA ,regB ,Des
        B = int(machineCode[firstRange-18:lastRange-16], 2) #ให้ bit 16-18 เป็น B  
        Des = int(machineCode[firstRange-2:lastRange-0], 2) #bit 0-2 เป็น destReg (R-type)    
        offset = int(c.twoCom_ToInt(c.sign_extend32( machineCode[firstRange-15:lastRange-0]))) #bit 0-15 เป็น 0 (J-type,O-type)    
        count+=1
        
        if opcode == '110':  #halt opcode = 110                                                                                                                  #เช็ค opcode ว่าเป็นคำสั่งไหน ?
            PC = PC + 1 #เพิ่มค่า PC
            count-=1
            break
        elif opcode == '000': #add opcode = 000
            reg[Des] = int(reg[A]) + int(reg[B]) #ค่าใน regA บวก ค่าใน regB แล้วเก็บผลลัพธ์ใน destReg
        elif opcode == '001': #nand opcode = 001
            AandB = c.twoCom_ToInt( c.gen_32twoCom( c.twoCom_ToInt(c.gen_32twoCom(reg[A])) &  c.twoCom_ToInt(c.gen_32twoCom(reg[B]))))
            AnandB = c.gen_32twoCom(~AandB)
            reg[Des] = c.twoCom_ToInt(AnandB) #ค่าใน regA NAND ค่าใน regB แล้วเก็บผลลัพธ์ใน destReg
        elif opcode == "010": #lw opcode = 010
            reg[B] = int(mem[int(reg[A])+offset]) #load regB โดย address หาจาก offestField + ค่าใน regA
        elif opcode == '011': #sw opcode = 011
            mem[int(reg[A])+offset] = int(reg[B]) #store regB โดย address หาจาก offestField + ค่าใน regA
        elif opcode == '100': #beq opcode = 100
            if int(reg[A]) == int(reg[B]): #ถ้าค่าใน regA เท่ากับ ค่าใน regB
                PC = PC + 1 + offset #กระโดดไปที่ PC+1+offsetField
                continue
        elif opcode == '101': #jalr opcode = 101
            if A == B: #ถ้า regA กับ regB เป็นตัวเดียวกัน
                reg[B] = PC + 1 #เก็บค่า PC+1 ใน regB
                PC = PC + 1 #กระโดดไปที่ PC+1
                reg[0] = 0 #reg[0] ต้องเป็น 0 ตลอด 
                continue
            else: #ถ้า regA กับ regB ไม่ใช่ตัวเดียวกัน
                reg[B] = PC + 1 #เก็บค่า PC+1 ใน regB
                PC = reg[A] #กระโดดไปที่ address ที่ถูกเก็บใน regA
                reg[0] = 0
                continue 
        elif opcode == '111': #noop opcode = 111
            pass
                  


        PC += 1 #เพิ่มค่า PC
        

    print("machine halted ")
    print("total of "+str(count)+ " instructions executed")
    print()
    print("final state of machine:")
    print()
    p.printState(PC,reg,mem)  
    


