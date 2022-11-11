from servey import transer
def hashport(give):
    #1024~49151
    return (24063+hash(give.strip().lower())%23038)

ONLINE = True
while True:
    ans = input("1.连接者 2.服务端: ")
    try:
        if ans == "1":
            while True:
                try:
                    tan = transer("CONNECTER",input("Input ip address: "),hashport(input("Input port: ")))
                except:
                    continue
        elif ans == "2":
            while True:
                try:
                    tan = transer("SERVEY",port=hashport(input("Input port: ")))
                except:
                    continue
        else:
            raise 
    except BaseException as err:
        print(err)
    else:
        tan.start()
        break