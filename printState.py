
def printState(PC,reg,mem):
    print("@@@")
    print("state:")
    print('          PC '+str(PC))
    print('          memory:')
    for i in range(0,len(mem)):
        print('                  mem[ '+str(i)+' ] '+str(mem[i]))
    print('          registers:')
    for i in range(0,len(reg)):
        print('                  reg[ '+str(i)+' ] '+str(reg[i]))
    print('end state')
    print('@@@')
        
