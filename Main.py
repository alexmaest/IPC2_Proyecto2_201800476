import xml.etree.cElementTree as ET
from xml.dom import minidom
from tkinter import *
import tkinter as t
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from allReport import allReport
from singleReport import singleReport
from timeReport import timeReport
from PIL import Image, ImageTk
import time
import re

def menu():
    print("****************************************************")
    print("*                  Menú Principal                  *")
    print("****************************************************")
    print("*  1) Cargar archivo de maquina                    *")
    print("*  2) Cargar archivo de simulación                 *")
    print("*  3) Mostrar Lineas de producción                 *")
    print("*  4) Mostrar productos                            *")
    print("*  5) Simulación de un producto                    *")
    print("*  6) Simulación de todos los productos            *")
    print("*  7) Archivo de salida de un producto XML         *")
    print("*  8) Archivo de salida de todos los productos XML *")
    print("*  9) Reporte de un producto                       *")
    print("* 10) Reporte de todos los productos               *")
    print("* 11) Reporte de un producto en un tiempo t        *")
    print("* 12) Salir                                        *")
    print("****************************************************")

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
    
    def agregar(self, valueToAdd):
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

    def agregar(self, value):
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

class exitProducts:
    def __init__(self, name, totalTime, elaboration):
        self.name = name
        self.totalTime = totalTime
        self.elaboration = elaboration

class elaboration:
    def __init__(self, secNum, stepList):
        self.secNum = secNum
        self.stepList = stepList

class assemblyLine:
    def __init__(self, lineNum, action):
        self.lineNum = lineNum
        self.action = action

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
saveSingleSimulation = simulation("", "")
saveCompleteSimulation = simulation("", "")
valores = []
segundos = []

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
            productionLines.agregar(productionLine(number, components, time, 0))
            #print("Linea: " + str(number) + ", No.Componentes: " + str(components) + ", tiempo: " + str(time))

        products = list()    
        productList = lowerRoot.getElementsByTagName("listadoproductos")[0]
        productListLen = len(productList.getElementsByTagName("producto")) 
        for num2 in range(productListLen):
            product1 = productList.getElementsByTagName("producto")[num2]
            name = product1.getElementsByTagName("nombre")[0].firstChild.data
            process = product1.getElementsByTagName("elaboracion")[0].firstChild.data
            cleaned = stepsDetector(process)
            products.agregar(product(name, cleaned))
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
            productsList.agregar(productName)
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
        steps.agregar(step)
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

def singleSimulation():
    global alphaSimulation
    saveProducts = list()
    current = alphaSimulation.products.first
    print("Nombre de la simulación: " + str(alphaSimulation.name))
    print("Productos cargados para simulación: ")
    while current != None:
        print("\t- " + str(current.value))
        current = current.next
    #print("\n")
    prod = input("Seleccione un producto para empezar la simulación: ")
    global alphaMachine
    current2 = alphaMachine.productList.first
    while current2 != None:
        tempName = str(current2.value.name)
        Encontrado = False
        if tempName.lower() == prod.lower():
            elaborationProd = list()
            Encontrado = True
            print("\n")
            print("Procedimiento de ensamblaje: " + str(current2.value.steps))
            print("\n")
            contLine = 0
            contComp = 0
            
            current3 = current2.value.steps.first
            matches = list()
            while current3 != None:
                #current3 = "L2pC3p" 
                stringStep = str(current3.value)
                regex = "[0-9]+"
                m = re.findall(regex, stringStep)
                matches.agregar(stepPassed(m[0], m[1], False))
                current3 = current3.next

            lineCurrent = alphaMachine.productionList.first
            lineSeconds = alphaMachine.productionList.first
            lineSeconds2 = alphaMachine.productionList.first
            secLoop = int(alphaMachine.lineNum)
            resetCont = 0
            reset = alphaMachine.productionList.first
            while resetCont != secLoop:
                resetComp = reset.value.setactComp(0)
                resetCont += 1
                reset = reset.next
            
            secLoop = 1
            while lineSeconds.next != lineSeconds2:
                secLoop += 1
                lineSeconds = lineSeconds.next

            contBool = 1
            clock = 1
            contSec = int(alphaMachine.lineNum)
            Assembly = False
            linePass = 0
            alphaCont = 0
            whileBreak = 0
            addCont = 0
            while lineCurrent != None:
                #if whileBreak == 12:
                #    break
                #whileBreak += 1
                action = ""
                if secLoop == contSec:
                    print("------ Segundo " + str(contBool) + " ------")
                    stepList = list()
                    secLoop = 0
                    alphaCont = 0
                    contBool += 1
                secLoop += 1
                addCont += 1
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
                    action = "Mover brazo - Componente " + str(lineCurrent.value.getactComp())
                    stepList.agregar(assemblyLine(lineNum, action))
                    lineCurrent = lineCurrent.next
                    if addCont == contSec:
                        elaborationProd.agregar(elaboration(contBool - 1, stepList))
                        addCont = 0
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
                                action = "Mover brazo - Componente " + str(lineCurrent.value.getactComp())
                                stepList.agregar(assemblyLine(lineNum, action))
                                contActions += 1
                                break
                            elif int(stepComp) < int(actComp):
                                actComp -= 1
                                lineCurrent.value.setactComp(actComp)
                                print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()))
                                action = "Mover brazo - Componente " + str(lineCurrent.value.getactComp())
                                stepList.agregar(assemblyLine(lineNum, action))
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
                                            action = "Ensamblar - Componente " + str(lineCurrent.value.getactComp())
                                            stepList.agregar(assemblyLine(lineNum, action))
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
                                            action = "Ensamblar - Componente " + str(lineCurrent.value.getactComp())
                                            stepList.agregar(assemblyLine(lineNum, action))
                                            contActions += 1
                                            break
                                        else:
                                            clock += 1
                                            Assembly = True
                                            alphaCont += 1
                                            print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()) + " ensamblandolo")
                                            action = "Ensamblar - Componente " + str(lineCurrent.value.getactComp())
                                            stepList.agregar(assemblyLine(lineNum, action))
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
                    action = "No hace nada"
                    stepList.agregar(assemblyLine(lineNum, action))

                contUltimate = 0
                while booleanTrue != None:
                    stepBoolean = booleanTrue.value.getBoolean()
                    #print("stepLine2: " + str(stepLine2) + ", stepBoolean: " + str(stepBoolean) + ", contUltimate: " + str(contUltimate))
                    if stepBoolean == False:
                        contUltimate += 1
                    booleanTrue = booleanTrue.next

                if addCont == contSec:
                    elaborationProd.agregar(elaboration(contBool - 1, stepList))
                    addCont = 0
                    
                if contUltimate == 0:
                    if secLoop == contSec:
                        print("\n")
                        print("Simulación terminada")
                        print("\n")
                        break
                lineCurrent = lineCurrent.next

            break
        else:
            current2 = current2.next

    if Encontrado == False:
        print("\n")
        print("Producto no encontrado")
        print("\n")
    else:
        saveProducts.agregar(exitProducts(tempName,contBool - 1,elaborationProd))
        global saveSingleSimulation
        saveSingleSimulation = simulation(alphaSimulation.name, saveProducts)

def completeSimulation():
    global alphaSimulation
    saveProducts = list()
    current = alphaSimulation.products.first
    alphacurrent = alphaSimulation.products.first
    print("Nombre de la simulación: " + str(alphaSimulation.name))
    print("Productos cargados para simulación: ")
    while current != None:
        print("\t- " + str(current.value))
        current = current.next
    #print("\n")
    while alphacurrent != None:
        simName = alphacurrent.value
        global alphaMachine
        current2 = alphaMachine.productList.first
        while current2 != None:
            tempName = str(current2.value.name)
            if tempName.lower() == simName.lower():
                Encontrado = True
                elaborationProd = list()
                print("\n")
                print("Simulación del producto: " + str(tempName.lower()))
                print("Procedimiento de ensamblaje: " + str(current2.value.steps))
                print("\n")
                contLine = 0
                contComp = 0
                
                current3 = current2.value.steps.first
                matches = list()
                while current3 != None:
                    #current3 = "L2pC3p" 
                    stringStep = str(current3.value)
                    regex = "[0-9]+"
                    m = re.findall(regex, stringStep)
                    matches.agregar(stepPassed(m[0], m[1], False))
                    current3 = current3.next

                lineCurrent = alphaMachine.productionList.first
                lineSeconds = alphaMachine.productionList.first
                lineSeconds2 = alphaMachine.productionList.first
                secLoop = int(alphaMachine.lineNum)
                resetCont = 0
                reset = alphaMachine.productionList.first
                while resetCont != secLoop:
                    resetComp = reset.value.setactComp(0)
                    resetCont += 1
                    reset = reset.next
                
                secLoop = 1
                while lineSeconds.next != lineSeconds2:
                    secLoop += 1
                    lineSeconds = lineSeconds.next

                contBool = 1
                clock = 1
                contSec = int(alphaMachine.lineNum)
                Assembly = False
                linePass = 0
                alphaCont = 0
                whileBreak = 0
                addCont = 0
                while lineCurrent != None:
                    #if whileBreak == 12:
                    #    break
                    #whileBreak += 1
                    action = ""
                    if secLoop == contSec:
                        print("------ Segundo " + str(contBool) + " ------")
                        stepList = list()
                        secLoop = 0
                        alphaCont = 0
                        contBool += 1
                    secLoop += 1
                    addCont += 1
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
                        action = "Mover brazo - Componente " + str(lineCurrent.value.getactComp())
                        stepList.agregar(assemblyLine(lineNum, action))
                        lineCurrent = lineCurrent.next
                        if addCont == contSec:
                            elaborationProd.agregar(elaboration(contBool - 1, stepList))
                            addCont = 0
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
                                    action = "Mover brazo - Componente " + str(lineCurrent.value.getactComp())
                                    stepList.agregar(assemblyLine(lineNum, action))
                                    contActions += 1
                                    break
                                elif int(stepComp) < int(actComp):
                                    actComp -= 1
                                    lineCurrent.value.setactComp(actComp)
                                    print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()))
                                    action = "Mover brazo - Componente " + str(lineCurrent.value.getactComp())
                                    stepList.agregar(assemblyLine(lineNum, action))
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
                                                action = "Ensamblar - Componente " + str(lineCurrent.value.getactComp())
                                                stepList.agregar(assemblyLine(lineNum, action))
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
                                                action = "Ensamblar - Componente " + str(lineCurrent.value.getactComp())
                                                stepList.agregar(assemblyLine(lineNum, action))
                                                contActions += 1
                                                break
                                            else:
                                                clock += 1
                                                Assembly = True
                                                alphaCont += 1
                                                print("Brazo número " + str(lineNum) + " en componente " + str(lineCurrent.value.getactComp()) + " ensamblandolo")
                                                action = "Ensamblar - Componente " + str(lineCurrent.value.getactComp())
                                                stepList.agregar(assemblyLine(lineNum, action))
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
                        action = "No hace nada"
                        stepList.agregar(assemblyLine(lineNum, action))

                    contUltimate = 0
                    while booleanTrue != None:
                        stepBoolean = booleanTrue.value.getBoolean()
                        #print("stepLine2: " + str(stepLine2) + ", stepBoolean: " + str(stepBoolean) + ", contUltimate: " + str(contUltimate))
                        if stepBoolean == False:
                            contUltimate += 1
                        booleanTrue = booleanTrue.next

                    if addCont == contSec:
                        elaborationProd.agregar(elaboration(contBool - 1, stepList))
                        addCont = 0
                        
                    if contUltimate == 0:
                        if secLoop == contSec:
                            print("\n")
                            print("Simulación terminada")
                            print("\n")
                            break
                    lineCurrent = lineCurrent.next

                break
            else:
                current2 = current2.next

        if Encontrado == False:
            print("\n")
            print("Producto no encontrado")
            print("\n")
        else:
            saveProducts.agregar(exitProducts(tempName,contBool - 1,elaborationProd))
            global saveCompleteSimulation
            saveCompleteSimulation = simulation(alphaSimulation.name, saveProducts)

        alphacurrent = alphacurrent.next

def graphicBrowser():
    win = Tk()
    win.geometry("1x1")
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select a File", filetypes=(("Xml files", "*.xml*"), ("All files", "*.*")))
    win.destroy()
    return filename

def singleXml():
    nameinput = str(xmlInOne.get())
    simName = saveCompleteSimulation.name
    alphaProd = saveCompleteSimulation.products.first
    simProd = saveCompleteSimulation.products.first
    while alphaProd != None:
        tempName = str(alphaProd.value.name)
        Encontrado = False
        if nameinput.lower() == tempName.lower():
            Encontrado = True
            try:
                salida = ET.Element("SalidaSimulacion")
                nameSimulation = ET.SubElement(salida, "Nombre").text = str(simName)
                productList = ET.SubElement(salida, "ListadoProductos")
                while simProd != None:
                    product = ET.SubElement(productList, "Producto")
                    nameProd = ET.SubElement(product, "Nombre").text = str(simProd.value.name)
                    timeProd = ET.SubElement(product, "TiempoTotal").text = str(simProd.value.totalTime)
                    elabProd = ET.SubElement(product, "ElaboracionOptima")
                    elab = simProd.value.elaboration.first
                    while elab != None:
                        currentSec = ET.SubElement(elabProd, "Tiempo", NoSegundo = str(elab.value.secNum))
                        currentList = elab.value.stepList.first
                        while currentList != None:
                            action = ET.SubElement(elabProd, "LineaEnsamblaje", NoLinea = str(currentList.value.lineNum)).text = str(currentList.value.action)
                            currentList = currentList.next
                        elab = elab.next
                    break

                archivo = ET.ElementTree(salida)
                archivo.write("reportes/simulaciones/xml/" + str(tempName) + "salida.xml")
                print("\n")
                print("Archivo creado con exito")
                print("\n")
                messagebox.showinfo("Información","Archivo creado con exito")
                break
            except:
                print("\n")
                print("Ha ocurrido un error al crear el archivo, intentelo de nuevo")
                print("\n")
                break
        else:
            alphaProd = alphaProd.next

    if Encontrado == False:
        print("\n")
        print("Producto no encontrado")
        print("\n")

def allXml():
    try:
        simName = saveCompleteSimulation.name
        simProd = saveCompleteSimulation.products.first
        salida = ET.Element("SalidaSimulacion")
        nameSimulation = ET.SubElement(salida, "Nombre").text = str(simName)
        productList = ET.SubElement(salida, "ListadoProductos")
        while simProd != None:
            product = ET.SubElement(productList, "Producto")
            nameProd = ET.SubElement(product, "Nombre").text = str(simProd.value.name)
            timeProd = ET.SubElement(product, "TiempoTotal").text = str(simProd.value.totalTime)
            elabProd = ET.SubElement(product, "ElaboracionOptima")
            elab = simProd.value.elaboration.first
            while elab != None:
                currentSec = ET.SubElement(elabProd, "Tiempo", NoSegundo = str(elab.value.secNum))
                currentList = elab.value.stepList.first
                while currentList != None:
                    action = ET.SubElement(elabProd, "LineaEnsamblaje", NoLinea = str(currentList.value.lineNum)).text = str(currentList.value.action)
                    currentList = currentList.next
                elab = elab.next
            simProd = simProd.next

        archivo = ET.ElementTree(salida)
        archivo.write("reportes/simulaciones/xml/" + str(simName) + "salida.xml")
        print("\n")
        print("Archivo creado con exito")
        print("\n")
        messagebox.showinfo("Información","Archivo creado con exito")
    except:
        print("\n")
        print("Ha ocurrido un error al crear el archivo, intentelo de nuevo")
        print("\n")

def browserMachine():
    path = graphicBrowser()
    readMachine(path)
    messagebox.showinfo("Información","Carga de maquina realizada correctamente")

def browserSimulation():
    path = graphicBrowser()
    readSimulation(path)
    completeSimulation()
    global alphaSimulation
    currentAppend = alphaSimulation.products.first
    global valores
    valores = []
    while currentAppend != None:
        valores.append(str(currentAppend.value))
        currentAppend = currentAppend.next
    ttk.Combobox(tab2, textvariable=data, width=15, values=valores).place(x=20, y=95)
    ttk.Combobox(tab3, textvariable=htmlInOne, values=valores).place(x=55, y=190)
    ttk.Combobox(tab3, textvariable=xmlInOne, values=valores).place(x=325, y=190)
    ttk.Combobox(tab3, textvariable=htmlInTwo, width=25, values=valores).place(x=45, y=320)
    messagebox.showinfo("Información","Carga de simulación realizada correctamente")

def simulationTable():
    #try:
    nameinput = str(data.get())
    global saveCompleteSimulation
    simName = saveCompleteSimulation.name
    alphaProd = saveCompleteSimulation.products.first
    dataProd = saveCompleteSimulation.products.first
    Encontrado = False

    global alphaMachine
    cantLines = int(alphaMachine.lineNum)
    columnas = []
    for col in range(cantLines + 1):
        columnas.append(col + 1)

    while alphaProd != None:
        tempName = str(alphaProd.value.name)
        if nameinput.lower() == tempName.lower():
            simProd = alphaProd
            timeProd = alphaProd
            global wrapper1
            wrapper1.destroy()
            wrapper1 = LabelFrame(tab2)
            wrapper1.pack(fill="both",expand="yes", padx=100, pady=200)
            trv = ttk.Treeview(wrapper1, columns=columnas, show="headings", height="6")
            style = ttk.Style(trv)
            style.configure("Treeview", rowheight=30)
            trv.pack(side=LEFT)
            trv.place(x=0, y=0)
            trv.heading(1, text="Segundo")
            trv.column(1, anchor="center", width=50, minwidth=60)

            Encontrado = True
            contHead = 2
            while simProd != None:
                elab = simProd.value.elaboration.first
                while elab != None:
                    currentList = elab.value.stepList.first
                    while currentList != None:
                        tempText = ""
                        NoLinea = str(currentList.value.lineNum)
                        tempText = "Linea " + NoLinea
                        trv.heading(contHead, text=tempText)
                        trv.column(contHead, anchor="center", width=150, minwidth=200)
                        contHead += 1
                        currentList = currentList.next
                    break
                break
            contData = 0
            while alphaProd != None:
                elab2 = alphaProd.value.elaboration.first
                cont = 1
                while elab2 != None:
                    row = []
                    currentSec = str(elab2.value.secNum)
                    row.append(currentSec)
                    currentList2 = elab2.value.stepList.first
                    while currentList2 != None:
                        action = str(currentList2.value.action)
                        row.append(action)
                        currentList2 = currentList2.next
                    trv.insert(parent='', index=contData, iid=contData, values=row)
                    #time.sleep(1)
                    cont += 1
                    contData += 1
                    elab2 = elab2.next
                break

            #Vertical ScrollBar
            yScroll = ttk.Scrollbar(wrapper1, orient="vertical", command=trv.yview)
            yScroll.pack(side=RIGHT, fill="y")
            #Horizontal ScrollBar
            xScroll = ttk.Scrollbar(wrapper1, orient="horizontal", command=trv.xview)
            xScroll.pack(side=BOTTOM, fill="x")
            trv.configure(yscrollcommand=yScroll.set, xscrollcommand=xScroll.set)

            liveSec =  str(timeProd.value.totalTime)
            limit = int(liveSec)
            for sec in range(limit):
                #time.sleep(1)
                global liveSeconds
                #liveSeconds.destroy()
                liveSeconds = Label(tab2, text=str(sec + 1), width=4, fg="#fcba03", bg ="#010030", font = "Helvetica 32 bold italic").place(x=610, y=445)

            print("\n")
            print("Tabla creada con exito")
            print("\n")
            break
        else:
            alphaProd = alphaProd.next
    #except:
     #   print("\n")
      #  print("Ha ocurrido un error al crear la tabla, intentelo de nuevo")
       # print("\n")

def buttonAllReport():
    lineNum = int(alphaMachine.lineNum)
    allReport(lineNum, saveCompleteSimulation)

def singleHtmlReport():
    singleProduct = str(htmlInOne.get())
    print(singleProduct)
    lineNum = int(alphaMachine.lineNum)
    singleReport(lineNum, singleProduct, saveCompleteSimulation)

def timeHtmlReport():
    singleProduct = str(htmlInTwo.get())
    second = int(htmlInTwoSec.get())
    print(singleProduct + ", " + str(second))
    lineNum = int(alphaMachine.lineNum)
    timeReport(lineNum, singleProduct, second, saveCompleteSimulation)

def updateData():
    nameinput = str(data.get())
    mach = alphaMachine.productList.first
    stepsText = ""
    while mach != None:
        tempName = mach.value.name
        if nameinput.lower() == tempName.lower():
            stepsText = str(mach.value.steps)
            break
        else:
            mach = mach.next
    stepsClean = stepsText.replace("p", "")
    t.Label(tab2, text=stepsClean, width=25, fg="#FFFFFF", bg ="#162742", font = "Helvetica 14 bold italic").place(x=200, y=90)

def updateSeconds():
    nameinput = str(htmlInTwo.get())
    alphaProd = saveCompleteSimulation.products.first
    simProd = saveCompleteSimulation.products.first
    timeProd = 0
    while alphaProd != None:
        tempName = str(alphaProd.value.name)
        if nameinput.lower() == tempName.lower():
            timeProd = int(alphaProd.value.totalTime)
            break
        else:
            alphaProd = alphaProd.next

    global segundos
    segundos = []
    for sec in range(timeProd):
        segundos.append(sec + 1)
    
    ttk.Combobox(tab3, width=2, textvariable=htmlInTwoSec, values=segundos).place(x=67, y=353)

v = t.Tk()
v.geometry("800x600")
v.resizable(False, False)
v.title("Digital Intelligence, S.A.")

tabControl = ttk.Notebook(v)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Cargar')
tabControl.add(tab2, text ='Procesos')
tabControl.add(tab3, text ='Reportes')
tabControl.add(tab4, text ='Ayuda')
tabControl.pack(expand = 1, fill ="both")

#TAB1
t.Label(tab1, text="", width=200, height=36, bg = "#162742").place(x=0, y=0)
t.Label(tab1, text="DIGITAL INTELLIGENCE, S.A.", fg="#fcba03", width=30, height=10, bg = "#162742", font = "Helvetica 24 bold italic").place(x=105, y=30)
t.Button(tab1, text="Cargar Maquina", width=25, font = "Arial 14", command=browserMachine).place(x=90, y=280)
t.Button(tab1, text="Cargar Simulación", width=25, font = "Arial 14", command=browserSimulation).place(x=430, y=280)
t.Label(tab1, text = "", width=130, height=20, bg = "dark gray").place(x=0, y=550)
t.Label(tab1, text = "   2021 - Proyecto 2 de Introducción a la programación 2", fg="black", bg = "dark gray").place(x=0, y=550)

#TAB2
t.Label(tab2, text="", width=200, height=36, bg = "#162742").place(x=0, y=0)
t.Label(tab2, text="Procesos", width=10, fg="#fcba03", bg = "#162742", font = "Helvetica 24 bold italic").place(x=600, y=30)
data = t.StringVar(tab2)
t.Button(tab2, width=1, text="⟳", font = "Helvetica 10 bold", bg='#fcba03', command=updateData).place(x=135, y=90)
t.Label(tab2, text="Productos", width=20, fg="#fcba03", bg = "#162742", font = "Helvetica 12").place(x=-35, y=65)
t.Label(tab2, text="Componentes necesarios", width=20, fg="#fcba03", bg = "#162742", font = "Helvetica 12").place(x=270, y=65)
t.Label(tab2, width=107, height=26, bg = "#010030").place(x=20, y=130)
t.Button(tab2, text="Iniciar simulación", width=15, font = "Arial 10", command=simulationTable).place(x=100, y=160)
t.Label(tab2, text="Segundos:", width=10, fg="#FFFFFF", bg = "#010030", font = "Helvetica 12").place(x=600, y=420)
liveSeconds = Label(tab2, text = "0", width=4, fg="#fcba03", bg ="#010030", font = "Helvetica 32 bold italic").place(x=610, y=445)
wrapper1 = LabelFrame(tab2)
wrapper1.pack(fill="both",expand="yes", padx=100, pady=200)
clockImage = Image.open("images/clock2.png")
photo = ImageTk.PhotoImage(clockImage)
clockLabel = Label(tab2, width=50, image=photo, bg = "#010030").place(x=560, y=442)
t.Label(tab2, text = "", width=130, height=20, bg = "dark gray").place(x=0, y=550)
t.Label(tab2, text = "   2021 - Proyecto 2 de Introducción a la programación 2", fg="black", bg = "dark gray").place(x=0, y=550)

#TAB3
t.Label(tab3, width=200, height=36, bg = "#162742").place(x=0, y=0)
t.Label(tab3, width=30, height=26, bg = "#010030").place(x=20, y=130)
t.Label(tab3, width=30, height=26, bg = "#010030").place(x=290, y=130)
t.Label(tab3, width=30, height=26, bg = "#010030").place(x=560, y=130)
t.Label(tab3, text="Reportes", width=10, fg="#fcba03", bg = "#162742", font = "Helvetica 24 bold italic").place(x=600, y=30)
#HTML
t.Label(tab3, text="HTML", width=20, fg="#fcba03", bg = "#162742", font = "Helvetica 12").place(x=35, y=100)
t.Label(tab3, text="Producto específico", width=20, fg="#FFFFFF", bg = "#010030", font = "Helvetica 12").place(x=35, y=160)
htmlInOne = t.StringVar(tab3)
htmlBOne = t.Button(tab3, text="Generar", width=10, font = "Arial 10", command=singleHtmlReport).place(x=80, y=220)
t.Label(tab3, text="Producto en un tiempo t", width=20, fg="#FFFFFF", bg = "#010030", font = "Helvetica 12").place(x=35, y=290)
t.Label(tab3, text="t", width=5, fg="#fcba03", bg = "#010030", font = "Helvetica 12 bold italic").place(x=27, y=351)
htmlInTwo = t.StringVar(tab3)
htmlBTwo = t.Button(tab3, text="Generar", width=10, font = "Arial 10", command=timeHtmlReport).place(x=133, y=350)
htmlInTwoSec = t.StringVar(tab3)
t.Button(tab3, width=1, text="⟳", font = "Helvetica 10 bold", bg='#fcba03', command=updateSeconds).place(x=102, y=350)
t.Label(tab3, text="Todos los productos", width=20, fg="#FFFFFF", bg = "#010030", font = "Helvetica 12").place(x=35, y=420)
t.Button(tab3, text="Generar", width=10, font = "Arial 10", command=buttonAllReport).place(x=80, y=450)
#XML
t.Label(tab3, text="XML", width=20, fg="#fcba03", bg = "#162742", font = "Helvetica 12").place(x=305, y=100)
t.Label(tab3, text="Producto específico", width=20, fg="#FFFFFF", bg = "#010030", font = "Helvetica 12").place(x=305, y=160)
xmlInOne = t.StringVar(tab3)
xmlBOne = t.Button(tab3, text="Generar", width=10, font = "Arial 10", command=singleXml).place(x=350, y=220)
t.Label(tab3, text="Todos los productos", width=20, fg="#FFFFFF", bg = "#010030", font = "Helvetica 12").place(x=305, y=290)
t.Button(tab3, text="Generar", width=10, font = "Arial 10", command=allXml).place(x=350, y=320)
#Graphviz
t.Label(tab3, text="Graphviz", width=20, fg="#fcba03", bg = "#162742", font = "Helvetica 12").place(x=576, y=100)
t.Label(tab3, text="Producto específico", width=20, fg="#FFFFFF", bg = "#010030", font = "Helvetica 12").place(x=576, y=160)
ttk.Combobox(tab3, values=["January", "February","March","April"]).place(x=596, y=190)
t.Button(tab3, text="Generar", width=10, font = "Arial 10").place(x=621, y=220)
t.Label(tab3, text = "", width=130, height=20, bg = "dark gray").place(x=0, y=550)
t.Label(tab3, text = "   2021 - Proyecto 2 de Introducción a la programación 2", fg="black", bg = "dark gray").place(x=0, y=550)

#TAB4
t.Label(tab4, width=200, height=36, bg = "#162742").place(x=0, y=0)
t.Label(tab4, width=107, height=26, bg = "#010030").place(x=20, y=130)
t.Label(tab4, text="Ayuda", width=10, fg="#fcba03", bg = "#162742", font = "Helvetica 24 bold italic").place(x=620, y=30)
t.Label(tab4, text="Acerca de la aplicación", width=20, fg="#fcba03", bg = "#010030", font = "Helvetica 12 italic").place(x=35, y=160)

info = """Esta aplicación simula los procesos de una máquina capaz de 
ensamblar las partes de cualquier producto en el mercado en un tiempo óptimo.
La máquina creada por Digital Intelligence, S.A. puede construir cualquier 
producto ensamblando automáticamente los componentes (partes) que lo conforman.
Para esto, la máquina desarrollada consta de una o varias líneas de ensamblaje y
un brazo robótico para cada una de éstas, además, cada línea de ensamblaje posee
un mecanismo que le permite acceder a uno o varios componentes distintos para ir
completando el proceso y hacer simulaciones optimizando el tiempo y recursos,
pudiendo ver estos procesos en tiempo real como también poder generar reportes
sobre estos procesos."""

datos = """Marvin Alexis Estrada Florian
3007201810101
201800476"""

t.Label(tab4, text=info, width=66, fg="#FFFFFF", bg = "#010030", font = "Helvetica 12", anchor="e", justify=LEFT).place(x=35, y=200)
t.Label(tab4, text="Datos del estudiante", width=20, fg="#fcba03", bg = "#010030", font = "Helvetica 12 italic").place(x=25, y=400)
t.Label(tab4, text=datos, width=23, fg="#FFFFFF", bg = "#010030", font = "Helvetica 12", anchor="e", justify=LEFT).place(x=35, y=440)
t.Label(tab4, text = "", width=130, height=20, bg = "dark gray").place(x=0, y=550)
t.Label(tab4, text = "   2021 - Proyecto 2 de Introducción a la programación 2", fg="black", bg = "dark gray").place(x=0, y=550)

v.mainloop()

"""
Ejecucion = True
while Ejecucion:
    menu()

    opcion = input("Elige una opción: ")

    if opcion == "1":
        #name = graphicBrowser()
        name = "C:/Users/alexi/Downloads/maquina.xml"
        readMachine(name)

    elif opcion == "2":
        name2 = graphicBrowser()
        #name2 = "C:/Users/alexi/Downloads/simulacion.xml"
        readSimulation(name2)
    
    elif opcion == "3":
        printProdLines()
    
    elif opcion == "4":
        printProducts()
    
    elif opcion == "5":
        singleSimulation()
    
    elif opcion == "6":
        completeSimulation()
    
    elif opcion == "7":
        createDoc(1)
    
    elif opcion == "8":
        createDoc(2)
    
    elif opcion == "9":
        lineNum = int(alphaMachine.lineNum)
        singleReport(lineNum, saveCompleteSimulation)

    elif opcion == "10":
        lineNum = int(alphaMachine.lineNum)
        allReport(lineNum, saveCompleteSimulation)
    
    elif opcion == "11":
        lineNum = int(alphaMachine.lineNum)
        timeReport(lineNum, saveCompleteSimulation)

    elif opcion == "12":
        print("Has salido del programa")
        Ejecucion = False

    else:
        print("Intenta de nuevo")
"""