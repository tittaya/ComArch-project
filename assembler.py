from Type_Code import Jtype,Itype,Otype,Rtype,gen_32twoCom

def Assembler(lineSplit,mem,PC,label_addr):                                  
        if lineSplit[1] == 'add' or lineSplit[1] == 'nand'  :                          #เช็คตาม Type 
            mem[PC] = int(Rtype(lineSplit),2)                                 #go to Type_code.py ได้เลขฐานสองมาทำเป็นเลขฐานสิบเก็บใน mem
        elif  lineSplit[1] == 'lw' or lineSplit[1] == 'sw' or lineSplit[1] == 'beq' :   
            mem[PC] = int(Itype(lineSplit,PC,label_addr),2)
        elif lineSplit[1] == 'halt' or lineSplit[1] == 'noop' :
            mem[PC] = int(Otype(lineSplit),2)
        elif lineSplit[1] == 'jalr':
            mem[PC] = int(Jtype(lineSplit),2)
        elif lineSplit[1] == '.fill':
            
            if lineSplit[2].lstrip('-').isdigit():                             #ถ้าตัวหลังจาก .fill เป็นเลข เอามาใส่เลย
                mem[PC] = int(lineSplit[2])                                            
            else:                                     
                mem[PC] = int(label_addr[lineSplit[2]])                        #ถ้าเป็น (symbolic address)string เอาไปเช็คกับ (int)label_addr ที่ map ไว้
        else:
            print("Invalid instruction >> label " + str(PC+1) )
            exit(1)

