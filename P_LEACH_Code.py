
import matplotlib.pyplot as plt
from random import random
import math

class Sensor:
    def __init__(self,number):
        self.ids=number
        self.x=random()*100
        self.y=random()*100	
        self.E= 2   #Eo
        self.cond=1
        self.dts=0    
        self.role=0  
        self.pos=0
        self.closest=0
        self.prev=0
        self.dis=0	
        self.dis2=0   
        self.order=0
        self.sel=0   
        self.rop=0    
        self.tel=0
        self.Esink=0

def main_Pegasis(n):
    xm=100
    ym=100
    x=0
    y=0
    dead_nodes=0

    sinkx=50
    sinky=200

    Eo=2                    #initial energy

    Eelec=50*10**(-9)
    ETx=50*10**(-9)
    ERx=50*10**(-9)
    Eamp=100*10**(-12)
    Eda=5*10**(-9)

    k=4000


    transmission=0
    temp_dead=0
    selected=0
    flag1stdead=0
    count=0
    turn=0
    temp_val=0
    order=[]
    T=[]
    op=[]
    nrg=[]
    cl_pos=0
    operating_nodes=n
    sensor_obj=[]
    dist=[]

    for i in range(0,n):
        sensor_obj.append(Sensor(i))

    for i in range(0,n):
        sensor_obj[i].dts=math.sqrt((sinkx-sensor_obj[i].x)**2 + (sinky-sensor_obj[i].y)**2)
        sensor_obj[i].Esink=Eelec*k+Eamp*k*(sensor_obj[i].dts)**2
        T.append(sensor_obj[i].dts)

    A=sorted(T,reverse=True)
    #print(A)
    A_id=[]

    for i in range(0,n):
        for j in range(0,n):
            if(A[i]==sensor_obj[j].dts):
                A_id.append(sensor_obj[j].ids)


    for i in range(0,n):
        sensor_obj[i].closest=0
        for j in range(0,n):
            q=math.sqrt((sensor_obj[i].x-sensor_obj[j].x)**2+(sensor_obj[i].y-sensor_obj[j].y)**2)
            if(q==0):
                q=9999
            dist.append((i,j,q))

    for i in range(0,n):
        m=min(dist,key=lambda t:t[2])


    rnd=0
    for i in range(0,n):
        if(sensor_obj[A_id[i]].E > 0 and sensor_obj[A_id[i]].sel==0 and sensor_obj[A_id[i]].cond==1):
            z=A_id[i]
            sensor_obj[z].sel=1
            sensor_obj[z].pos=1
            break
    order.append(z)

    temp=1
    while selected <n:
        min_dist=9999
        for i in range(0,n):
            if(sensor_obj[i].sel==0):
                d=math.sqrt((sensor_obj[i].x-sensor_obj[z].x)**2+(sensor_obj[i].y-sensor_obj[z].y)**2)
                if d <min_dist:
                    min_dist=d
                    next_node=i

        selected+=1
        sensor_obj[z].closest=next_node
        sensor_obj[z].dis=min_dist
        sensor_obj[z].sel=1
        sensor_obj[z].prev=z
        sensor_obj[z].dis2=math.sqrt((sensor_obj[z].x-sensor_obj[next_node].x)**2 + (sensor_obj[z].y-sensor_obj[next_node].y)**2)
        z=next_node
        temp+=1
        order.append(z)
    #print(order) 


    order.append(0)

    sensor_obj[z].pos=2
    sensor_obj[z].dis=0
    sensor_obj[z].closest=0

    for i in range(0,n):
        if(sensor_obj[i].closest==z and sensor_obj[i].pos==0):
            sensor_obj[z].prev=i
            sensor_obj[z].dis2=math.sqrt((sensor_obj[i].x-sensor_obj[z].x)**2 + (sensor_obj[i].y-sensor_obj[z].y)**2)
        
    
    k1=0
    while operating_nodes>0 :
        k1+=1
        if(k1==1000):
            break
        energy =0
        for i in range(0,n):
            sensor_obj[i].role=0

        cluster_head=int(math.fmod(turn,n))
    
        if(sensor_obj[cluster_head].cond==0):
            while(sensor_obj[cluster_head].cond==0):
                turn+=1
                cluster_head=int(math.fmod(turn,n))+1
        if(sensor_obj[cluster_head].cond==1):
            sensor_obj[cluster_head].role=1
            sensor_obj[cluster_head].tel=sensor_obj[cluster_head].tel+1


        for i in range(0,n):
            if(order[i]==cluster_head):
                cl_pos=i
                break

        for i in range(0,n):
            if(sensor_obj[order[i]].E>0 and sensor_obj[order[i]].cond==1):

                if(i<cl_pos):

                    if(sensor_obj[order[i]].pos==1 and sensor_obj[order[i]].role==0):
                        ETx=Eelec*k + Eamp *k*(sensor_obj[order[i]].dis)**2
                        sensor_obj[order[i]].E=sensor_obj[order[i]].E-ETx
                        energy=energy+ETx

                    if(sensor_obj[order[i]].pos==0 and sensor_obj[order[i]].role==0):
                        ERx=(Eda+Eelec)*k
                        ETx=(Eda+Eelec)*k + Eamp *k*(sensor_obj[order[i]].dis)**2
                        sensor_obj[order[i]].E=sensor_obj[order[i]].E-ETx-ERx
                        energy=energy+ETx+ERx

                if(i>cl_pos):

                    if(sensor_obj[order[i]].pos==2 and sensor_obj[order[i]].role==0):
                        ETx=Eelec*k + Eamp *k*(sensor_obj[order[i]].dis2)**2
                        sensor_obj[order[i]].E=sensor_obj[order[i]].E-ETx
                        energy=energy+ETx

                    if(sensor_obj[order[i]].pos==0 and sensor_obj[order[i]].role==0):
                        ERx=(Eda+Eelec)*k
                        ETx=(Eda+Eelec)*k + Eamp *k*(sensor_obj[order[i]].dis2)**2
                        sensor_obj[order[i]].E=sensor_obj[order[i]].E-ETx-ERx
                        energy=energy+ETx+ERx


                if(i==cl_pos):
                
                    if(sensor_obj[order[i]].pos==0 and sensor_obj[order[i]].role==1):
                        ERx=(Eda+Eelec)*k*2
                        ETx=(Eda+Eelec)*k + Eamp *k*(sensor_obj[order[i]].dts)**2
                        sensor_obj[order[i]].E=sensor_obj[order[i]].E-ETx-ERx
                        energy=energy+ETx+ERx

                    if(sensor_obj[order[i]].pos==1 and sensor_obj[order[i]].role==1):
                        ERx=(Eda+Eelec)*k
                        ETx=(Eda+Eelec)*k + Eamp *k*(sensor_obj[order[i]].dts)**2
                        sensor_obj[order[i]].E=sensor_obj[order[i]].E-ETx-ERx
                        energy=energy+ETx+ERx

                    if(sensor_obj[order[i]].pos==2 and sensor_obj[order[i]].role==1):
                        ERx=(Eda+Eelec)*k
                        ETx=(Eda+Eelec)*k + Eamp *k*(sensor_obj[order[i]].dts)**2
                        sensor_obj[order[i]].E=sensor_obj[order[i]].E-ETx-ERx
                        energy=energy+ETx+ERx

            if(sensor_obj[order[i]].E<=0 and sensor_obj[order[i]].cond==1):

                sensor_obj[order[i]].cond=0

                if (sensor_obj[order[i]].pos==1 and sensor_obj[order[i]].role==0):
                    if (operating_nodes==1):
                        done='OK'
                    else:
                        t=i
                        while (sensor_obj[order[i]].cond==0 and t<n):
                            t=t+1

                        sensor_obj[order[i]].pos=1
                        sensor_obj[order[i]].prev=0


                if (sensor_obj[order[i]].pos==2 and sensor_obj[order[i]].role==0):
                    if (operating_nodes==1):
                        done='OK'
                    else:
                        t=i
                        while (sensor_obj[order[i]].cond==0 and t>1):
                            t=t-1

                        sensor_obj[order[i]].pos=2
                        sensor_obj[order[i]].closest=0

                if (sensor_obj[order[i]].pos==0 and sensor_obj[order[i]].role==1):
                    sensor_obj[order[i]].role=0
                    after=i
                    for j in range(after,n):
                        if(sensor_obj[order[j]].cond==1):
                            break

                    bef=i
                    for k in range(1,bef,-1):
                        if(sensor_obj[order[k]].cond==1):
                            break
                
                    sensor_obj[order[k]].closest=order[j]
                    sensor_obj[order[j]].prev=order[k]
                    sensor_obj[order[k]].dis=math.sqrt((sensor_obj[k].x-sensor_obj[j].x)**2 + (sensor_obj[k].y-sensor_obj[j].y)**2)
                    sensor_obj[order[j]].dis2=sensor_obj[order[k]].closest




                    if (sensor_obj[order[j]].pos==1 and sensor_obj[order[j]].role==1):
                        sensor_obj[order[j]].role=0
                        t=i
                        while(sensor_obj[order[j]].cond==0 and t<n):
                            t+=1
                        sensor_obj[order[j]].pos=1

                    if (sensor_obj[order[j]].pos==2 and sensor_obj[order[j]].role==1):
                    
                     
                        sensor_obj[order[j]].role=0
                        t=i
                        while(sensor_obj[order[j]].cond==0 and t>1):
                         
                            t-=1
                        sensor_obj[order[j]].pos=2


                    if (sensor_obj[order[i]].pos==0 and sensor_obj[order[i]].role==0):
                        after=i
                        for j in range(after,n):
                            if(sensor_obj[order[j]].cond==1):
                                break

                        bef=i
                        for k in range(1,bef,-1):
                            if(sensor_obj[order[k]].cond==1):
                                break
                        sensor_obj[order[k]].closest=order[j]
                        sensor_obj[order[j]].prev=order[k]
                        sensor_obj[order[k]].dis=math.sqrt((sensor_obj[k].x-sensor_obj[j].x)**2 + (sensor_obj[k].y-sensor_obj[j].y)**2)
                        sensor_obj[order[j]].dis2=sensor_obj[order[k]].dis

                        operating_nodes-=1
                        dead_nodes+=1

                        sensor_obj[order[k]].closest=0
                        sensor_obj[order[k]].prev=0
                        sensor_obj[order[k]].dis=0
                        sensor_obj[order[k]].dis2=0
                        sensor_obj[order[k]].pos=101
                        sensor_obj[order[k]].rop=rnd


        if(operating_nodes<n and temp_val==0):
            temp_val=1
            flag1stdead=rnd

        rnd+=1
        turn+=1
        op.append(operating_nodes)

        if(energy>0):
            nrg.append(energy)


    s=0
    flag1stdead=rnd
    for i in range(0,flag1stdead):
        s+=nrg[i]

    temp1=s/flag1stdead
    temp2=temp1/n

    avg_node=[]

    for i in range(0,flag1stdead):
        avg_node.append(temp2)

    xc=[]
    yc=[]
    temp=[]
    for i in range(0,n):
        xc.append(sensor_obj[i].x)
        yc.append(sensor_obj[i].y)
    for i in range(1,1000):
        temp.append(i)

    plt.plot(xc,yc,'ro')
    plt.show()

    plt.plot(xc,yc,'ro-')
    plt.show()
    
    plt.plot(temp,avg_node)
    plt.show()
    
    plt.plot(temp,nrg)
    plt.show()


main_Pegasis(500)



                
        
            

            
                
            
            
            
        
    
    
