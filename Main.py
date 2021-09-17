import xml.etree.cElementTree as ET
from xml.dom import minidom
from tkinter import filedialog
from tkinter import *
import re

def menu():
    print("***********************************")
    print("*          Menú Principal         *")
    print("***********************************")
    print("* 1) Cargar archivo de maquina    *")
    print("* 2) Cargar archivo de simulación *")
    print("* 3) Mostrar Lineas de producción *")
    print("* 4) Mostrar productos            *")
    print("* 5) Iniciar simulación           *")
    print("* 6) -------------                *")
    print("* 7) -------------                *")
    print("* 8) -------------                *")
    print("* 9) Salir                        *")
    print("***********************************")

class node:
    def __init__(self, value):
        self.value = value
        self.next = None
    
    def __str__(self):
        return str(self.value)

class circularNode:
    def __init__(self, value = None, next = None):
        self.value = value
        self.next = next

class list:
    def __init__(self):
        self.first = None
        self.size = 0
    
    def append(self, valueToAdd):
        MyNode = node(valueToAdd)
        if self.size == 0:
            self.first = MyNode
        else:
            Current = self.first
            while Current.next != None:
                Current = Current.next
            Current.next = MyNode
        self.size += 1
        return MyNode
    
    def remove(self, valuetoRemove):
        if self.size == 0:
            return False
        else:
            Current = self.first
            while Current.next.value != valuetoRemove:
                if Current.next == None:
                    return False
                else:
                    Current = Current.next
                
            deletedNode = Current.next
            Current.next = deletedNode.next
        self.size -= 1
        return deletedNode
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        String = "["
        Current = self.first
        while Current != None:
            String += str(Current)
            if Current.next != None:
                String += str(",")
            Current = Current.next
        String += "]"
        
        return String

class circularList:
    def __init__(self):
        self.first = None
        self.size = 0

    def append(self, value):
        if self.first is None:
            self.first = circularNode(value = value)
            self.first.next = self.first    
        else:
            actual = circularNode(value = value, next = self.first.next)
            self.first.next = actual
            self.size += 1

    def recorrer(self):
        if self.first is None:
            return
        actual = self.first
        while actual != None:
            print(actual.value.num)
            actual = actual.next
            
    def __len__(self):
        return self.size
        
class machine:
    def __init__(self, lineNum, productionList, productList):
        self.lineNum = lineNum
        self.productionList = productionList
        self.productList = productList

class productionLine:
    def __init__(self, num, componentNum, time, actComp):
        self.num = num
        self.componentNum = componentNum
        self.time = time
        self.actComp = actComp

    def setactComp(self, value):
        self.actComp = value

    def getactComp(self):
        return self.actComp

class product:
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

class simulation:
    def __init__(self, name, products):
        self.name = name
        self.products = products

class stepPassed:
    def __init__(self, line, comp, boolean):
        self.line = line
        self.comp = comp
        self.boolean = boolean

    def setBoolean(self, value):
        self.boolean = value

    def getBoolean(self):
        return self.boolean

alphaMachine = machine(0, "", "")
alphaSimulation = simulation("", "")

def lowerTree(tree):
    t = ET.tostring(tree)
    t = t.lower()
    return minidom.parseString(t)

def readMachine(ruta):
    try:
        #Parse
        mytree = ET.parse(ruta)
        root = mytree.getroot()
        lowerRoot = lowerTree(root)

        lineNum = lowerRoot.getElementsByTagName("cantidadlineasproduccion")[0].firstChild.data
        
        productionLines = circularList()
        production = lowerRoot.getElementsByTagName("listadolineasproduccion")[0]
        prodLineLen = len(production.getElementsByTagName("lineaproduccion")) 
        for num in range(prodLineLen):
            prodLine = production.getElementsByTagName("lineaproduccion")[num]
            number = prodLine.getElementsByTagName("numero")[0].firstChild.data
            components = prodLine.getElementsByTagName("cantidadcomponentes")[0].firstChild.data
            time = prodLine.getElementsByTagName("tiempoensamblaje")[0].firstChild.data
            productionLines.append(productionLine(number, components, time, 0))
            #print("Linea: " + str(number) + ", No.Componentes: " + str(components) + ", tiempo: " + str(time))

        products = list()    
        productList = lowerRoot.getElementsByTagName("listadoproductos")[0]
        productListLen = len(productList.getElementsByTagName("producto")) 
        for num2 in range(productListLen):
            product1 = productList.getElementsByTagName("producto")[num2]
            name = product1.getElementsByTagName("nombre")[0].firstChild.data
            process = product1.getElementsByTagName("elaboracion")[0].firstChild.data
            cleaned = stepsDetector(process)
            products.append(product(name, cleaned))
            #print("Producto: " + str(name) + ", Proceso de ensamblaje: " + str(process))
        
        global alphaMachine
        alphaMachine = machine(lineNum, productionLines, products)

        print("\n")
        print("Carga realizada correctamente")
        print("\n")   
    except:
        print("\n")
        print("Ha ocurrido un error, intentalo nuevamente")
        print("\n")

def readSimulation(ruta):
    try:
        #Parse
        mytree = ET.parse(ruta)
        root = mytree.getroot()
        lowerRoot = lowerTree(root)

        name = lowerRoot.getElementsByTagName("nombre")[0].firstChild.data
        
        productsList = list()
        products = lowerRoot.getElementsByTagName("listadoproductos")[0]
        productsLen = len(products.getElementsByTagName("producto")) 
        for num in range(productsLen):
            productName = products.getElementsByTagName("producto")[num].firstChild.data
            productsList.append(productName)
        global alphaSimulation
        alphaSimulation = simulation(name, productsList)
        
        print("\n")
        print("Carga realizada correctamente")
        print("\n")   
    except:
        print("\n")
        print("Ha ocurrido un error, intentalo nuevamente")
        print("\n")

def stepsDetector(process):
    #process = "L1pC1p L2pC2p L1pC3p"
    regex = "[Ll][0-9]+p[Cc][0-9]+p"
    reSteps = re.findall(regex, process)
    steps = list()
    for step in reSteps:
        steps.append(step)
    return steps

def printProdLines():
    print("Maquina cargada:")
    print("\n")

    global alphaMachine
    print("--------------- Lineas de producción ---------------")
    print("Cantidad de lineas de producción cargadas: " + str(alphaMachine.lineNum))
    print("\n")
    current = alphaMachine.productionList.first
    currentFirst = alphaMachine.productionList.first
    while current.next != currentFirst:
        print("\tNúmero de linea: " + str(current.value.num))
        print("\tCantidad de componentes: " + str(current.value.componentNum))
        print("\tTiempo de ensamblaje: " + str(current.value.time))
        print("\n")
        current = current.next
    
    print("--------------- Listado de productos ---------------")
    current2 = alphaMachine.productList.first
    current3 = alphaMachine.productList.first
    cont = 0
    while current2 != None:
        cont += 1
        current2 = current2.next
    print("Cantidad de productos cargados: " + str(cont))
    print("\n")
    while current3 != None:
        print("\tNombre del producto: " + str(current3.value.name))
        print("\tElaboración: " + str(current3.value.steps))
        print("\n")
        current3 = current3.next
    
def printProducts():
    print("Simulación cargada:")
    print("\n")

    global alphaSimulation
    print("Nombre de la simulación: " + str(alphaSimulation.name))
    print("\n")
    print("--------------- Listado de productos ---------------")
    current = alphaSimulation.products.first
    while current != None:
        print("\tNombre del producto: " + str(current.value))
        current = current.next
    print("\n")

def simulationlineCurrent():
    global alphaSimulation
    current = alphaSimulation.products.first
    print("Productos cargados para simulación: ")
    while current != None:
        print("\t- " + str(current.value))
        current = current.next
    print("\n")
    prod = input("Seleccione un producto para empezar la simulación: ")
    global alphaMachine
    current2 = alphaMachine.productList.first
    while current2 != None:
        tempName = str(current2.value.name)
        Encontrado = False
        if tempName.lower() == prod.lower():
            Encontrado = True
            print("Procedimiento de ensamblaje: " + str(current2.value.steps))
            contLine = 0
            contComp = 0
            step = "l" + str(contLine) + "pc" + str(contComp) + "p"
            
            current3 = current2.value.steps.first
            matches = list()
            while current3 != None:
                #current3 = "L2pC3p" 
                stringStep = str(current3.value)
                regex = "[0-9]+"
                m = re.findall(regex, stringStep)
                matches.append(stepPassed(m[0], m[1], False))
                current3 = current3.next

            lineCurrent = alphaMachine.productionList.first
            lineSeconds = alphaMachine.productionList.first
            lineSeconds2 = alphaMachine.productionList.first
            contSec = 1
            while lineSeconds.next != lineSeconds2:
                contSec += 1
                lineSeconds = lineSeconds.next

            contBool = 1
            clock = 1
            secLoop = int(alphaMachine.lineNum)
            Assembly = False
            linePass = 0
            alphaCont = 0
            whileBreak = 0
            while lineCurrent != None:
                #if whileBreak == 12:
                #    break
                #whileBreak += 1
                if secLoop == contSec:
                    print("------ Segundo " + str(contBool) + " ------")
                    secLoop = 0
                    alphaCont = 0
                    contBool += 1
                secLoop += 1
                #if contBool == 6:
                #    break
                lineNum = lineCurrent.value.num
                actComp = lineCurrent.value.getactComp()
                timeCont = lineCurrent.value.time
                timeAssembling = int(timeCont)
                if actComp == 0:
                    actComp += 1
                    lineCurrent.value.setactComp(actComp)
                    print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()))
                    lineCurrent = lineCurrent.next
                    continue

                #print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()))
                currentStep = matches.first # [1, 1], [2, 2], [1, 3]
                booleanTrue = matches.first # [1, 1], [2, 2], [1, 3]
                contActions = 0
                contOrder = 0
                while currentStep != None:
                    stepBoolean = currentStep.value.getBoolean()
                    if stepBoolean == False:
                        contOrder += 1
                    stepLine = currentStep.value.line
                    if int(stepLine) == int(lineNum):
                        if stepBoolean == False:
                            stepComp = currentStep.value.comp
                            if int(stepComp) > int(actComp):
                                actComp += 1
                                lineCurrent.value.setactComp(actComp)
                                print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()))
                                contActions += 1
                                break
                            elif int(stepComp) < int(actComp):
                                actComp -= 1
                                lineCurrent.value.setactComp(actComp)
                                print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()))
                                contActions += 1
                                break
                            else:
                                if contOrder > 1:
                                    contActions = 0
                                    break
                                else:
                                    if Assembly == False:
                                        if alphaCont == 0:
                                            linePass = lineNum
                                            Assembly = True
                                            print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()) + " ensamblandolo")
                                            contActions += 1
                                            clock += 1
                                            break
                                        else:
                                            contActions = 0
                                            break

                                    elif linePass == lineNum:
                                        if clock == timeAssembling:
                                            clock = 1
                                            currentStep.value.setBoolean(True)
                                            Assembly = False
                                            alphaCont += 1
                                            print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()) + " ensamblandolo")
                                            contActions += 1
                                            break
                                        else:
                                            clock += 1
                                            Assembly = True
                                            alphaCont += 1
                                            print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()) + " ensamblandolo")
                                            contActions += 1
                                            break
                                    else:
                                        contActions = 0
                                        break
                        else:
                            currentStep = currentStep.next
                    else:
                        currentStep = currentStep.next
                
                if contActions == 0:
                    print("Brazo número " + str(lineNum) + " no hace nada")

                contUltimate = 0
                while booleanTrue != None:
                    stepBoolean = booleanTrue.value.getBoolean()
                    #print("stepLine2: " + str(stepLine2) + ", stepBoolean: " + str(stepBoolean) + ", contUltimate: " + str(contUltimate))
                    if stepBoolean == False:
                        contUltimate += 1
                    booleanTrue = booleanTrue.next
                    
                if contUltimate == 0:
                    if secLoop == contSec:
                        print("\n")
                        print("Simulación terminada")
                        print("\n")
                        break
                lineCurrent = lineCurrent.next

            """
            while lineCurrent != None:
                compCont = 0
                lineNum = lineCurrent.value.num
                actComp = lineCurrent.value.actComp

                if actComp == 0:
                    actComp += 1
                    lineCurrent.value.actComp = actComp
                lineCurrent = lineCurrent.next
            """
            
            #alphaMachine.productionList.recorrer()
            #while contBool != 3:
            """
            currentStep = matches.first # [1, 1], [2, 2], [1, 3]
            while currentStep != None:
                stepBoolean = currentStep.value.boolean
                if stepBoolean == False:
                    contBool += 1

                    stepLine = currentStep.value.line
                    stepComp = currentStep.value.comp



            current2 = alphaMachine.productionList.first
            while current2 != None:
                print("Brazo número " + str(current2.value.num) + " en componente 1")
                current2 = current2.next
            """
            break
        else:
            current2 = current2.next
    if Encontrado == False:
        print("\n")
        print("Producto no encontrado")
        print("\n")

def graphicBrowser():
    win = Tk()
    win.geometry("1x1")
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select a File", filetypes=(("Xml files", "*.xml*"), ("All files", "*.*")))
    win.destroy()
    return filename

Ejecucion = True
while Ejecucion:
    menu()

    opcion = input("Elige una opción: ")

    if opcion == "1":
        #name = graphicBrowser()
        name = "C:/Users/alexi/Downloads/maquina.xml"
        readMachine(name)

    elif opcion == "2":
        #name2 = graphicBrowser()
        name2 = "C:/Users/alexi/Downloads/simulacion.xml"
        readSimulation(name2)
    
    elif opcion == "3":
        printProdLines()
    
    elif opcion == "4":
        printProducts()
    
    elif opcion == "5":
        simulationlineCurrent()

    elif opcion == "9":
        print("Has salido del programa")
        Ejecucion = False

    else:
        print("Intenta de nuevo")