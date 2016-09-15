# coding: utf-8

''' 
bootstraping and accessment system 
作成日　2016/03/29-
このモジュールは F値,precision,recallについて検定を行うものです
input data style 
(actual_label , prediction1_label , prediction2_label)
Reference: P.Koehn 2004 Statistical significance tests for machine translation evaluation
'''
import pandas as pd
import numpy as np
import random
import pandas as pd
import tkinter.filedialog as tkfd


def initialize():
    #入力処理
    file = tkfd.askopenfilename()  
    print("please input the name of file ? :")
    data = pd.read_csv(file)
    print("Number of Bootstrap sample :")
    bootstrap = int(input())
    print("select measurement, 1:precision 2:recall 3:f-measure")
    t = int(input())


    #initionlizing 
    sys  = []
    for i in range(len(data)):
        #system1 = [t_p,t_n,f_p,f_n]
        if data["Actual"][i] == data["system1"][i] and data["Actual"][i] == 1: sys.append([1,0,0,0])
        elif data["Actual"][i] == data["system1"][i] and data["Actual"][i] == 0: sys.append([0,1,0,0])
        elif data["Actual"][i] != data["system1"][i] and data["Actual"][i] == 0: sys.append([0,0,1,0])
        elif data["Actual"][i] != data["system1"][i] and data["Actual"][i] == 1: sys.append([0,0,0,1])
        #system2 = [t_p,t_n,f_p,f_n]
        if data["Actual"][i] == data["system2"][i] and data["Actual"][i] == 1: sys[i] += [1,0,0,0]
        elif data["Actual"][i] == data["system2"][i] and data["Actual"][i] == 0: sys[i] += [0,1,0,0]
        elif data["Actual"][i] != data["system2"][i] and data["Actual"][i] == 0: sys[i] += [0,0,1,0]
        elif data["Actual"][i] != data["system2"][i] and data["Actual"][i] == 1: sys[i] += [0,0,0,1]
    
    #ここで検定結果を返す
    result = main(data,bootstrap,t,sys)
    
    
    print("system1",result.count(1),"system2",result.count(2),"draw",result.count(0),len(result))
    print("p = ",result.count(1)/bootstrap)
    
        
def evalation(newlist,t):
    if newlist[0] == 0 : pre1,re1,f1 = 0,0,0  
    else :
        pre1,re1 = newlist[0]/(newlist[2]+newlist[0]),newlist[0]/(newlist[0]+newlist[3])
        f1 = 2*pre1*re1/(pre1+re1)
    
    if newlist[4] == 0: pre2,re2,f2 = 0,0,0
    else :
        pre2,re2 = newlist[4]/(newlist[4]+newlist[6]),newlist[4]/(newlist[4]+newlist[7])
        f2 = 2*pre2*re2/(pre2+re2)
    
    #F- measureの勝ち負け
    #print(f1,f2)
    if t ==1 :
        if pre1 > pre2: kekka = 1
        elif pre1 < pre2 : kekka = 2
        else: kekka = 0
            
    elif t ==2 :
        if re1 > re2: kekka = 1
        elif re1 < re2 :kekka = 2 
        else: kekka = 0
            
    elif t ==3 :
        if f1 > f2 : kekka = 1
        elif f1 < f2 : kekka = 2
        else: kekka = 0
    
    return kekka

    
        
#ブートストラップをつくる部分
def main(data,bootstrap,t,sys) : 
    result = []
    for i in range(bootstrap):
        #ここで縦方向に可算していく--------------------
        newlist = np.array([0,0,0,0,0,0,0,0])
        for j in range(int(len(sys)/2)):
            k = random.randrange(len(data))
            newlist += np.array(sys[k])
            
        if i %100 == 0:
            print("calculation Left :",bootstrap-i)
        result.append(evalation(newlist,t))
        #-----------------------------------------
    return result


initialize()

