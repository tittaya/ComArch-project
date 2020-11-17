import re
from Type_Code import J_type,I_type,O_type,R_type,gen_16twoCom,gen_32twoCom,sign_extend32,label
from assembler import Assembler
from simulator import simulate

fileName = "combination.txt"                          #อ่านไฟล์ Assembly.txt เข้ามา
filetext = open(fileName,"r")
#--------------------------------------------
label_addr = label(fileName)               #สร้าง labels ไป Type_Code.py 
#--------------------------------------------
line_arr = []
for line in filetext :
    line_arr.append(line)                      #store each line in array
#--------------------------------------------
mem = []


if len(line_arr) > 65536:
    print('Error: Overflow Memory')   
    exit(1)                                   
for i in range(0,len(line_arr)):                #สร้าง mem เท่ากับจำนวนบรรทัด 
    mem.append(0) 
reg = []                                        #สร้าง register 8 ตัว ไว้เก็บค่า  เอาไปใช้ใน simulator
for i in range(0,8):
    reg.append(0)
#--------------------------------------------
PC=0
while PC < len(line_arr):                           #วนจนกว่าจะหมดบรรทัด
    lineSplit = re.split(r"\s+", line_arr[PC],5)    #ตัด string ของแต่ละบรรทัดแบ่งช่องว่าง เป็น 5 index
    Assembler(lineSplit,mem,PC,label_addr)          #go to assembler.py
    PC += 1
#--------------------------------------------- 
    
for i in range(0,len(mem)):
    print('memory['+str(i)+']='+str(  mem[i]))
startPC = 0
simulate(startPC,reg,mem)
def combination(n,r):
    if n==r or r==0 :
        return 1
    else:
        return combination(n-1,r) + combination(n-1,r-1)

exit(0)




