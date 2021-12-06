from tkinter import *
from tkinter import Menu
from tkinter import ttk
import tkinter.font as font
from binance_api import Binance
import threading
import time
import datetime


    #__Global variables (RU: Основные глобальные переменные)
    #__Button switch: button_Timer is Start or Stop
PS_BU = False #Timer button_Timer state is Start/Stop True/False

    #__Timer switch (Deamon threading) running/stoped True/False
should_run_BU = False #Timer BTC/USDT watch start/stop true/false

sys_msg = ''
TT0=0
grSmb = 'BTCUSDT' #Symbol (RU: Символ пары)

class timer_BTCUSDT:
    
    def __init__(self):
        global PS_BU
        global should_run_BU
        i=0
        while True:
            if PS_BU == False:
                sys_msg = '  BTC/USDT watcher stoped.' #RU: ' Наблюдатель BTC/USDT остановлен.'
                app.Sys_Msg(text1=sys_msg)
                break            
            if should_run_BU:
                if not should_run_BU:
                    ss_BU = 'Stopped...' + '\n BTC/USDT watcher'
                    app.label_BU.config(text = ss_BU)
                    app.label_BU['bg']='SystemButtonFace'
                    app.label_BU['fg']='SystemButtonText'
                    sys_msg = '  BTC/USDT watcher will be stoped.' #RU: ' Наблюдатель BTC/USDT будет остановлен.'
                    app.Sys_Msg(text1=sys_msg)
                    break
                if should_run_BU:
                    if i==0:
                        API_KEY_Str = str(app.text_AK.get(1.0,'end-1c'))
                        API_SECRET_Str = str(app.text_AS.get(1.0,'end-1c'))
                        if API_KEY_Str == '' or API_SECRET_Str == '':
                            sys_msg = '  API_KEY or API_SECRET is null.' #RU: ' Наблюдатель BTC/USDT будет остановлен.'
                            app.Sys_Msg(text1=sys_msg)
                            should_run_BU = False
                            PS_BU = False
                            app.button_Timer.config(text="Start", fg='green')                                
                            break
                        sys_msg = '  Start BTC/USDT watcher.' #RU: ' Наблюдатель BTC/USDT запущен.'
                        app.Sys_Msg(text1=sys_msg)
                        bot = Binance(API_KEY=API_KEY_Str, API_SECRET=API_SECRET_Str)
                            #start reading Binance account    
                        myListAcc = bot.account()
                        time_local_int = int(time.mktime(time.localtime()))
                        time_local_time = datetime.datetime.fromtimestamp(time_local_int)
                        time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
                        sys_msg = "\n" + str(time_local_str) + "  Binance SPOT account. Permissions: " + str(myListAcc['permissions']) + '. CanDeposit: ' + str(myListAcc['canDeposit'])
                        sys_msg += str(". canWithdraw: ") + str(myListAcc['canWithdraw'])
                        app.text_Sys.insert(END, sys_msg)

                    #__PAUSE WHILE RUNNING
                    if i > 0:
                        time.sleep(0.5)

                    #__Reading BTC/USDT SPOT klines info from Binance (last 5 minutes)
                    myTupSpK =('klines', bot.klines(symbol='BTCUSDT', interval='1m', limit=5)) #Tupl
                    myDicGr1Sp = myTupSpK[1] #dict

                    yI_Sp_0=0
                    yI_Sp_1=0
                    for ii in range(len(myDicGr1Sp)):
                        if ii == 0:
                            yI_Sp_1=float(myDicGr1Sp[ii][3])
                        if float(myDicGr1Sp[ii][2])>yI_Sp_0:
                            yI_Sp_0=float(myDicGr1Sp[ii][2])  #High Price
                        if float(myDicGr1Sp[ii][2])<yI_Sp_1:
                            yI_Sp_1=float(myDicGr1Sp[ii][3])  #Low Price

                    #__Reading BTC/USDT FUTURES klines info from Binance (last 5 minutes)
                    myTupFtK = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='1m', limit=5)) #tupl
                    myDicGr1Ft = myTupFtK[1]

                    yI_Ft_0=0
                    yI_Ft_1=1
                    for ii in range(len(myDicGr1Ft)):
                        if ii == 0:
                            yI_Ft_1=float(myDicGr1Ft[ii][3])
                        if float(myDicGr1Ft[ii][2])>yI_Ft_0:
                            yI_Ft_0=float(myDicGr1Ft[ii][2])  #High Price
                        if float(myDicGr1Ft[ii][2])<yI_Ft_1:
                            yI_Ft_1=float(myDicGr1Ft[ii][3])  #Low Price

                    ss_BU = 'SPOT: xx%, FUTURES xx%'
                        
                    myTup_DSp = ('depth', bot.depth(symbol='BTCUSDT', limit=5)) #tupl
                    #print('SPOT BTCUSDT Depth',myTup_DSp)
                    mylist3_Sp = myTup_DSp[1]  #dict
                    mylist4_Sp=mylist3_Sp['bids'] #list

                    myTup_DFt = ('FutDepth', bot.futuresDepth(symbol='BTCUSDT', limit=5)) #tupl
                    #print('Futures BTCUSDT Depth',myTup_DFt)                        
                    mylist3_Ft = myTup_DFt[1]  #dict
                    mylist4_Ft=mylist3_Ft['bids'] #list

                    time_local_int = int(time.mktime(time.localtime()))
                    time_local_time = datetime.datetime.fromtimestamp(time_local_int)
                    time_local_str=time_local_time.strftime("[%H:%M:%S] ")

                    xx1 = (float(mylist4_Sp[0][0])-yI_Sp_0)/(float(mylist4_Sp[0][0])/100)
                    ss_BU = time_local_str + 'SPOT: ' + "%.2f" % (xx1) + '%, '
                    xx2 = (float(mylist4_Ft[0][0])-yI_Ft_0)/(float(mylist4_Ft[0][0])/100)
                    ss_BU += 'FRS: ' + "%.2f" % (xx2) + '%, '
                    xx3 = (float(mylist4_Sp[0][0])-yI_Sp_1)/(float(mylist4_Sp[0][0])/100)
                    ss_BU += '\n' + time_local_str + 'SPOT: ' + "%.2f" % (xx3) + '%, '
                    xx4 = (float(mylist4_Ft[0][0])-yI_Ft_1)/(float(mylist4_Ft[0][0])/100)
                    ss_BU += 'FRS: ' + "%.2f" % (xx4) + '%, '
                        
                    app.label_BU.config(text = ss_BU)

                    #__Change bg color if price is low or high
                    if (xx3<0 and xx4<0) or ((xx1<-0.25 and xx2<-0.25) and (-xx1>xx3 and -xx2>xx4)):
                        if app.label_BU['bg']=='SystemButtonFace':
                            app.label_BU['bg']='pink'
                            app.label_BU['fg']='SystemButtonText'
                        else:
                            app.label_BU['bg']='SystemButtonFace'
                            app.label_BU['fg']='red'
                    elif (xx1>0 and xx2>0) or ((xx3>0.25 and xx4>0.25)and (xx3>(-xx1) and xx4>(-xx2))):
                        if app.label_BU['bg']=='SystemButtonFace':
                            app.label_BU['bg']='lightgreen'
                            app.label_BU['fg']='SystemButtonText'
                        else:
                            app.label_BU['bg']='SystemButtonFace'
                            app.label_BU['fg']='green'
                    else:
                        app.label_BU['bg']='SystemButtonFace'
                        app.label_BU['fg']='SystemButtonText'

                    #__Reading Binance SPOT account
                    BnAcc = bot.account()
                    BnAcc10 = BnAcc['balances']
                    ss = 'SPOT balance: '
                    #print(BnAcc10)
                    for mm in range(len(BnAcc10)):
                        BnAcc101 = BnAcc10[mm]        
                        if BnAcc101['asset'] =='USDT':
                            #print (BnAcc10[mm])
                            ss += str(BnAcc101['asset']) + "\nAvailable: " + str(BnAcc101['free']) + "USDT.\nNot available: " +  str(BnAcc101['locked']) + ' USDT.'
                            #RU: ss += str(BnAcc101['asset']) + "\nДоступно: " + str(BnAcc101['free']) + "USDT.\nНе доступно: " +  str(BnAcc101['locked']) + ' USDT.'
                    app.label_BlnsSpt.config(text = ss)

                    #__Reading Binance FUTURES balances
                    BnFAcc = bot.futuresBalance()
                    #print(BnFAcc)
                    ss = 'FUTURE balance: '
                    if len(BnFAcc)>0:
                        for mm in range (len(BnFAcc)):
                            BnFAcc1 = BnFAcc[mm]
                            if BnFAcc1['asset'] == 'USDT':
                                #print(BnFAcc[mm])
                                ss += str(BnFAcc1['asset']) + '.'
                                ss += "\nBalance: " + str(BnFAcc1['balance']) + ".\nAvailable: " +  str(BnFAcc1['withdrawAvailable'])
                                #RU: ss += "\nВсего: " + str(BnFAcc1['balance']) + ".\nДоступно: " +  str(BnFAcc1['withdrawAvailable'])
                    app.label_BlnsFts.config(text = ss)

                    #__Reading Binance FUTURES account
                    BnFAcc = bot.futuresAccount()
                    #print(BnFAcc)
                    ss = 'FUTURES positions:\n'
                    if len(BnFAcc)>0:
                        BnFAcc1 = BnFAcc['totalUnrealizedProfit']
                        ss += 'PnL: ' + str(BnFAcc1) + ' USDT'
                        app.label_PnL.config(text = ss)

                    #__Reading Binance FUTURES positions
                    BnFAcc=bot.userPositionInfo()

                    #__Remember Treeview yview
                    TrSc_P = app.Tree_Ord.yview()
                    #print(TrSc_P)
                    #__Clear List_Ord
                    app.List_Ord.delete(0,END)
                    #To clear Treeview use: app.Tree_Ord.delete(*app.Tree_Ord.get_children())
                    TP_CL = app.Tree_Ord.get_children()
                    TP_CC = len(TP_CL)
                    l = TP_CC+1
                    if len(BnFAcc)>0:
                        for mm in range (len(BnFAcc)):
                            BnFAcc1 = BnFAcc[mm]
                            sTmp=''
                            if float(BnFAcc1['positionAmt']) != 0:
                                sTmp += '\n userPositionInfo баланс: ' + str(BnFAcc1['symbol']) + ". PnL: " + str(BnFAcc1['unRealizedProfit']) + ". entryPrice: " +  str(BnFAcc1['entryPrice'])
                                sTmp += ". positionSide: " +  str(BnFAcc1['positionSide'])
                                sTmp = str(BnFAcc1['symbol']) + ". PnL: " + str(BnFAcc1['unRealizedProfit']) + ". entryPrice: " +  str(BnFAcc1['entryPrice'])
                                sTmp += ". positionSide: " +  str(BnFAcc1['positionSide'])
                                app.List_Ord.insert(END, sTmp)
                                 
                            #print(BnFAcc1)
                            if len(BnFAcc1)>0:
                                TP_SCh = True
                                #__If Treeview is not empty Then update data
                                if TP_CC > 0:
                                    for nn in range(1,TP_CC+1):
                                        TP_It = app.Tree_Ord.item(nn)["values"]
                                        if TP_It[0] == str(BnFAcc1['symbol']) and TP_It[2] == str(BnFAcc1['positionSide']):
                                            app.Tree_Ord.item(nn, values=(str(BnFAcc1['symbol']),str(BnFAcc1['unRealizedProfit']),str(BnFAcc1['positionSide']),str(BnFAcc1['entryPrice']),
                                                                                                    str(float(BnFAcc1['positionAmt'])*float(BnFAcc1['entryPrice'])),str(BnFAcc1['liquidationPrice'])))
                                            TP_SCh = False
                                            #print(TP_It[0])
                                #__If Treeview don't have this position or empty Then add info about position
                                if TP_SCh == True and float(BnFAcc1['positionAmt']) != 0:
                                    #print(TP_It)
                                    #print(str(BnFAcc1['symbol']),str(BnFAcc1['unRealizedProfit']),str(BnFAcc1['positionSide']))
                                    app.Tree_Ord.insert(parent='',index='end',iid=l,text='',values=(str(BnFAcc1['symbol']),str(BnFAcc1['unRealizedProfit']),str(BnFAcc1['positionSide']),str(BnFAcc1['entryPrice']),
                                                                                                    str(float(BnFAcc1['positionAmt'])*float(BnFAcc1['entryPrice'])),str(BnFAcc1['liquidationPrice'])))
                                    l +=1
                    #__Making "copy" of Treeview items
                    TP_CL=app.Tree_Ord.get_children()
                    TP_CC=len(TP_CL)
                    TP_Tpl_Tmp=[]
                    for nn in range(1,TP_CC+1):
                        TP_It = app.Tree_Ord.item(nn)["values"]
                        TP_Tpl_Tmp.append(app.Tree_Ord.item(nn)["values"])
                        #print(TP_Tpl_Tmp[nn-1])
                    #__Remove items with positionAmt==0 from Treeview And update iid
                    kk=0
                    nm=False
                    for nn in range(1,TP_CC+1):
                        TP_It = app.Tree_Ord.item(nn)["values"]
                        if float(TP_It[3]) == 0 and float(TP_It[4]) == 0 and kk<=len(TP_Tpl_Tmp):
                            nm=True
                            km=False
                            for mm in range(kk,len(TP_Tpl_Tmp)):
                                #print(mm)
                                if float(TP_Tpl_Tmp[mm][3])!=0 and float(TP_Tpl_Tmp[mm][4])!=0 and km==False:
                                    app.Tree_Ord.item(nn, values=(TP_Tpl_Tmp[mm][0],TP_Tpl_Tmp[mm][1],TP_Tpl_Tmp[mm][2],TP_Tpl_Tmp[mm][3],TP_Tpl_Tmp[mm][4],TP_Tpl_Tmp[mm][5]))
                                    kk=mm+1
                                    #print(nn,kk,mm)
                                    km=True
                            if nm==True and km==False:
                                kk=len(TP_Tpl_Tmp)+1
                        else:
                            #print(nn,kk)
                            if nm==True and kk<TP_CC:
                                app.Tree_Ord.item(nn, values=(TP_Tpl_Tmp[kk][0],TP_Tpl_Tmp[kk][1],TP_Tpl_Tmp[kk][2],TP_Tpl_Tmp[kk][3],TP_Tpl_Tmp[kk][4],TP_Tpl_Tmp[kk][5]))
                            kk +=1
                        if kk>len(TP_Tpl_Tmp) and nn<=TP_CC+1:
                            app.Tree_Ord.delete(nn)

                    #__Set Treeview yview as before changes
                    app.Tree_Ord.yview_moveto((TrSc_P[0]))
                    
                    if i == 0:
                        i = 1

def click_button_Timer():
    global PS_BU
    global should_run_BU
    myFont = font.Font(size=10)
    app.button_Timer['font'] = myFont
    #print (PS_BU, should_run_BU)
    if PS_BU == True and should_run_BU == True:
        PS_BU = False
        should_run_BU = False
        app.button_Timer.config(text="Start", fg='green')
    elif PS_BU == False and should_run_BU == False:
        PS_BU = True
        should_run_BU = True
        timer_BU = threading.Thread(target=timer_BTCUSDT,daemon=True)
        timer_BU.start()
        app.button_Timer.config(text="Stop", fg='red')
 
class gui:

    def __init__(self, window):
        # Empty background label - just white background
        self.label_bg = Label(root, text="", bg="white")
        self.label_bg.place(height=10,width=10,x=10,y=10)
        #______________LEFT TOP SIDE BEGIN
        # Label for Spot balances USDT
        self.label_BlnsSpt = Label(root, text="SPOT balance = 0 USDT", anchor=NW, justify=LEFT)
        self.label_BlnsSpt.place(height=50,width=190,x=10,y=10)
        # Label for Futures balances USDT 
        self.label_BlnsFts = Label(root, text="FUTURES balance = 0 USDT", anchor=NW, justify=LEFT)
        self.label_BlnsFts.place(height=50,width=190,x=10,y=60)
        #_______________LEFT TOP SIDE END
        #_______________RIGHT TOP SIDE BEGIN
        # Label BTC/USDT watch - grow/fall
        self.label_BU = Label(root, text="BTC/USDT +0 %", anchor=NW, justify=LEFT)
        self.label_BU.place(height=40,width=200,x=510,y=10)
        # start/stop button - start/stop timer
        self.button_Timer = Button(root, text="START", command=click_button_Timer)
        self.button_Timer.place(height=40,width=50,x=460,y=10)

        # Label for Futures total PnL
        self.label_PnL = Label(root, text="FUTURES positions:\nPnL: +0 %", anchor=NW, justify=LEFT)
        self.label_PnL.place(height=60,width=250,x=460,y=60)
        #_______________RIGHT TOP SIDE END
        #_______________MIDDLE TOP SIDE BEGIN
        # Text boxes for API-Key and API-Secret
        self.label_AK = Label(root, text="API-Key: ", anchor=NW, justify=LEFT)
        self.label_AK.place(height=30,width=70,x=200,y=10)
        self.text_AK = Text(root)
        self.text_AK.place(height=20,width=370,x=270,y=10)
        self.label_AS = Label(root, text="API-Secret: ", anchor=NW, justify=LEFT)
        self.label_AS.place(height=30,width=70,x=200,y=40)
        self.text_AS = Text(root)
        self.text_AS.place(height=20,width=370,x=270,y=40)
        
        #_______________MIDDLE TOP SIDE END        
        #_______________MIDDLE SIDE BEGIN
        # Listbox current Futures orders
        self.List_Ord=Listbox(selectmode=SINGLE)
        self.List_Ord.place(height=150,width=300,x=210,y=10)
        
        self.List_Ord_Scrl = Scrollbar(root,command=self.List_Ord.yview)
        self.List_Ord_Scrl.place(height=150,width=10,x=510,y=10)
        
        self.List_Ord.config(yscrollcommand=self.List_Ord_Scrl.set)
        # Treeview for current Futures positions
        self.Tree_Ord=ttk.Treeview(selectmode='none')
        self.Tree_Ord['columns']=('Side','Symbol','Leverage','PnL','Margin','Price', 'Qty', 'QtyM', 'QtyW','Liquid')
        self.Tree_Ord.column("#0",width=0,stretch=NO)
        self.Tree_Ord.column("Side",anchor=W,width=80)
        self.Tree_Ord.column("Symbol",anchor=W,width=80)
        self.Tree_Ord.column("Leverage",anchor=W,width=80)
        self.Tree_Ord.column("PnL",anchor=W,width=80)
        self.Tree_Ord.column("Margin",anchor=W,width=80)
        self.Tree_Ord.column("Price",anchor=W,width=80)
        self.Tree_Ord.column("Qty",anchor=W,width=80)
        self.Tree_Ord.column("QtyM",anchor=W,width=80)
        self.Tree_Ord.column("QtyW",anchor=W,width=80)
        self.Tree_Ord.column("Liquid",anchor=W,width=80)
        self.Tree_Ord.heading("#0",text="",anchor=CENTER)
        self.Tree_Ord.heading("Side",text="Side",anchor=CENTER)
        self.Tree_Ord.heading("Symbol",text="Symbol",anchor=CENTER)
        self.Tree_Ord.heading("Leverage",text="Leverage",anchor=CENTER)
        self.Tree_Ord.heading("PnL",text="PnL",anchor=CENTER)
        self.Tree_Ord.heading("Margin",text="Margin",anchor=CENTER)
        self.Tree_Ord.heading("Price",text="Price",anchor=CENTER)
        self.Tree_Ord.heading("Qty",text="Qty",anchor=CENTER)
        self.Tree_Ord.heading("QtyM",text="QtyM",anchor=CENTER)
        self.Tree_Ord.heading("QtyW",text="QtyW",anchor=CENTER)
        self.Tree_Ord.heading("Liquid",text="Liquid",anchor=CENTER)      
        self.Tree_Ord.place(height=150,width=300,x=210,y=10)

        self.Tree_Ord_VScrl = Scrollbar(root,command=self.Tree_Ord.yview)
        self.Tree_Ord_VScrl.place(height=150,width=10,x=510,y=10)
        
        self.Tree_Ord.config(yscrollcommand=self.Tree_Ord_VScrl.set)
        #_______________MIDDLE SIDE END        
        #_______________BOTTOM SIDE BEGIN
        # Text Box for System messages
        self.text_Sys = Text(root, wrap=WORD)
        self.text_Sys.place(height=150,width=600,x=10,y=660)
        self.text_Sys.insert('end','')
        self.text_Sys_Scrl = Scrollbar(root,command=self.text_Sys.yview)
        self.text_Sys_Scrl.place(height=150,width=10,x=600,y=660)
        self.text_Sys.config(yscrollcommand=self.text_Sys_Scrl.set)
        #_______________BOTTOM SIDE END

#_______________DEF Sys_Msg BEGIN (System message): insert text in to text_Sys Label
    def Sys_Msg(self,text1):
        time_local_int = int(time.mktime(time.localtime()))
        time_local_time = datetime.datetime.fromtimestamp(time_local_int)
        time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
        sys_msg = '\n' + str(time_local_str) + text1
        app.text_Sys.insert(END, sys_msg)
        app.text_Sys.yview(END)
    
#_______________SET GUI BEGIN
root = Tk()
app = gui(root)
root.title('Binance Futures watcher')
root.geometry("1400x850+150+100")

time_local_int = int(time.mktime(time.localtime()))
time_local_time = datetime.datetime.fromtimestamp(time_local_int)
time_local_str = time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
sys_msg = str(time_local_str) + '  Start Programm.'
app.text_Sys.insert(END, sys_msg)
#_______________SET GUI END
#_______________SET BOT AS BINANCE
bot=Binance(API_KEY='',API_SECRET='')

#_______________READING BINANCE TIME BEGIN
myListST = bot.time()
sss23 = myListST['serverTime']/1000
sss24 = datetime.datetime.fromtimestamp(sss23)
sss25=sss24.strftime("[%d.%m.%Y %H:%M:%S] ")

time_local_int = int(time.mktime(time.localtime()))
time_local_time = datetime.datetime.fromtimestamp(time_local_int)
time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
sss00 = '\n' + str(time_local_str) + '  Binance time: ' + str(sss25)
sys_msg += sss00
app.text_Sys.insert(END, sss00)
#_______________READING BINANCE TIME END
#_______________PROGRAMM READY (LOADING GUI FINISHED) BEGIN
time_local_int = int(time.mktime(time.localtime()))
time_local_time = datetime.datetime.fromtimestamp(time_local_int)
time_local_str=time_local_time.strftime("[%d.%m.%Y %H:%M:%S] ")
sys_msg = '\n' + str(time_local_str) + '  Programmm ready to work!'
app.text_Sys.insert(END, sys_msg)
#_______________PROGRAMM READY (LOADING GUI FINISHED) END
#_______________RESIZE GUI BEGIN
def config(event):
    global grH
    global grW
    if event.widget == root:
        app.label_bg.place(x=10, y=10, width=event.width-20, height=event.height-20)
        app.label_BU.place(x=event.width-210, y=10, width=200, height=40)
        app.button_Timer.place(x=event.width-260, y=10, width=50, height=40)
        app.label_PnL.place(x=event.width-260, y=60, width=250, height=50)
        app.text_AK.place(height=20,width=event.width-550,x=270,y=10)
        app.text_AS.place(height=20,width=event.width-550,x=270,y=40)
        app.List_Ord.place(x=10, y=120, width=event.width-40, height=130)
        app.List_Ord_Scrl.place(height=130,width=10,x=event.width-30,y=120)
        app.Tree_Ord.place(x=10, y=270, width=event.width-40, height=event.height-450)
        app.Tree_Ord_VScrl.place(height=event.height-450,width=10,x=event.width-30,y=270)
        app.text_Sys.place(height=150,width=event.width-30,x=10,y=event.height-160)
        app.text_Sys_Scrl.place(height=150,width=10,x=event.width-20,y=event.height-160)
        grH = event.height-320
        grW = event.width-340
#_______________RESIZE GUI END
root.bind("<Configure>", config)

root.mainloop()
