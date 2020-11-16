import re
import CodeType as c 
import  assembler as a
import simulator  as s

fileName = "combination.txt"                          #อ่านไฟล์ Assembly.txt เข้ามา
filetext = open(fileName,"r")
#--------------------------------------------
label_addr = c.label(fileName)               #create labels ไป Type_Code.py 
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
    a.Assembler(lineSplit,mem,PC,label_addr)          #go to assembler.py
    PC += 1
#--------------------------------------------- 
    
for i in range(0,len(mem)):
    print('Address['+str(i)+']='+str(  mem[i])+' (hex '+str(hex(int(mem[i]) & (2**32-1)))+' )')
startPC = 0
s.simulate(startPC,reg,mem)
exit(0)



