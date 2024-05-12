from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicProvider
import random
from math import pi
from qiskit.visualization import plot_histogram, plot_bloch_multivector, plot_state_qsphere




def circuit_1():
    
    cr_result = ClassicalRegister(6,name ='result_')
    qr_doors = QuantumRegister(3,name='door')
    qr_choices = QuantumRegister(3,name='choice')
    qr_open= QuantumRegister(1,name='open_q')

    circuit = QuantumCircuit(qr_doors,qr_choices,qr_open,cr_result)

    
    print("----------------------------------------------------------")
    
    
    #Random winning door=====================================
    circuit.ry(1.910633, 0)
    circuit.ch(0, 1)
    circuit.cx(1, 2)
    circuit.cx(0, 1)
    circuit.x(0)


    #Random choice door======================================
    circuit.ry(1.910633, 3)
    circuit.ch(3, 4)
    circuit.cx(4, 5)
    circuit.cx(3, 4)
    circuit.x(3)
    
    circuit.barrier()
    
    
    #open door======================================
    circuit.ry(pi/4,6)
    circuit.ccx(0,0+3,6)
    circuit.ry(pi/-4,6)
    
    circuit.ry(pi/4,6)
    circuit.ccx(1,1+3,6)
    circuit.ry(pi/-4,6)
    
    circuit.ry(pi/4,6)
    circuit.ccx(2,2+3,6)
    circuit.ry(pi/-4,6)
    
    
    circuit.ccx(0,4,6)
    circuit.ccx(1,5,6)
    circuit.ccx(2,3,6)
    
    circuit.barrier()
    circuit.measure([0,1,2,3,4,5],[0,1,2,3,4,5])
    
    
    
    provider = BasicProvider()
    backend = provider.get_backend('basic_simulator')
    
    result2= backend.run(transpile(circuit,backend)).result().get_counts()
    
    plot_histogram(result2)
    
    circuit.draw('mpl')
    
    
    
    
    

def circuit_2():
    
    
    cr_result = ClassicalRegister(6,name ='result_')
    cr_open = ClassicalRegister(1,name ='open_c')
    cr_wining = ClassicalRegister(1,name ='wining_')
    qr_doors = QuantumRegister(3,name='door')
    qr_choices = QuantumRegister(3,name='choice')
    qr_open= QuantumRegister(1,name='open_q')
    qr_wining = QuantumRegister(1,name='wining')

    circuit = QuantumCircuit(qr_doors,qr_choices,qr_open,qr_wining,cr_result,cr_open,cr_wining)



    print("------------------------------------------------------------")
    
    #Random winning door=====================================
    circuit.ry(1.910633, 0)
    circuit.ch(0, 1)
    circuit.cx(1, 2)
    circuit.cx(0, 1)
    circuit.x(0)
    

    chosen_door= int(input('Choose a door (0,1,2) :'))

    circuit.x(chosen_door+3)
    
    circuit.barrier()

    #cch gate================================================
    circuit.ry(pi/4,6)
    circuit.ccx(chosen_door,chosen_door+3,6)
    circuit.ry(pi/-4,6)


    list_of_doors_options=[0,1,2]
    list_of_doors_options.remove(chosen_door)
    print('The host will open one of these doors:',list_of_doors_options)


    #open door===============================================
    ControlX= random.choice(list_of_doors_options)
    print('Control X:', ControlX)
    
    circuit.cx(ControlX,6)
    
    circuit.measure(qr_open,cr_open)
    circuit.barrier()
    
    print("------------------------------------------------------------")
    
    
    stay_or_swap_button=int(input('The host opened the door which the goats behind it.. \nDo you want to stay with your first choice or swap to the other remaining door?\n\nto stay enter (0) | to swap enter (1) :'))


    print("------------------------------------------------------------")
    
    
    #stay
    if stay_or_swap_button==0:
        circuit.ccx(chosen_door,chosen_door+3,7)
    #swap    
    if stay_or_swap_button==1:
        
        list_of_doors_options.remove(ControlX)
        dd=int(list_of_doors_options[0])
        
        circuit.swap(chosen_door+3,ControlX+3).c_if(cr_open,1)
        circuit.swap(chosen_door+3,dd+3).c_if(cr_open,0)
        circuit.barrier()
        
        circuit.ccx(ControlX,ControlX+3,7).c_if(cr_open,1)
        circuit.ccx(dd,dd+3,7).c_if(cr_open,1).c_if(cr_open,0)
        
      
    circuit.measure(qr_wining,cr_wining)

    circuit.barrier()

    circuit.measure([0,1,2,3,4,5],[0,1,2,3,4,5])


    provider = BasicProvider()
    backend = provider.get_backend('basic_simulator')
    result = list(backend.run(transpile(circuit,backend)).result().get_counts().keys())[0]


    if result[0]=='1':
        print('\n        Congrats! You opened the prize door')
    else:
        print('\n        hard luck.. You opened the goat door')


    
    
    print("\n \n------------------------------------------------------------")
    
    print('\n    Through the quantum circuits output, you may confirm that \n                the games outcomes are accurate \n\n                         ',result, '\n\n       Qubit (7) decides win/loss, while qubit (6) determines \n                 which door the host will open.')

    print("\n \n------------------------------------------------------------")
     
    
    #circuit.draw('mpl')

#===================================================================================================


def main():

    circuit_1or2=int(input('Enter (0) to run the quantum circuit to randomly select all possibilities. \nEnter (1) if you want to choose one of the doors yourself in the quantum circuit.'))
    if circuit_1or2 == 0:
        circuit_1()
        
    elif circuit_1or2 ==1:
        circuit_2()
        
    else:
        print('You have entered an incorrect option')
               
main()