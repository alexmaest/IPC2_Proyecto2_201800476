from tkinter import messagebox
class timeReport:
    def __init__(self, lineNum, producto, numBreak, simulation):
        self.lineNum = lineNum
        self.producto = producto
        self.numBreak = numBreak
        self.simulation = simulation

        simProd = simulation.products.first
        alphaProd = simulation.products.first
        while alphaProd != None:
            tempName = str(alphaProd.value.name)
            timeProd = str(alphaProd.value.totalTime)

            Encontrado = False
            if producto.lower() == tempName.lower():
                Generar = True
                if numBreak > int(timeProd) or numBreak <= 0:
                    Generar = False
                Encontrado = True
                if Generar == True:
                    html = open("reportes/simulaciones/html/reporteProducto_" + tempName + ".html", "w")
                    html.write("""<!DOCTYPE html>
                    <html lang="en">

                    <head>

                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <meta name="description" content="">
                        <meta name="author" content="TemplateMo">
                        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700" rel="stylesheet">

                        <title>Reporte</title>

                        <!-- Bootstrap core CSS -->
                        <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

                        <!-- Additional CSS Files -->
                        <link rel="stylesheet" href="assets/css/fontawesome.css">
                        <link rel="stylesheet" href="assets/css/templatemo-host-cloud.css">
                        <link rel="stylesheet" href="assets/css/owl.css">
                    <!--

                    Host Cloud Template

                    https://templatemo.com/tm-541-host-cloud

                    -->
                    </head>

                    <body>
                        <!-- Header -->
                        <header class="">
                        <nav class="navbar navbar-expand-lg">
                            <div class="container">
                            <a class="navbar-brand" href="reporte.html"><h2>Reportes<em>IPC2</em></h2></a>
                            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                                <span class="navbar-toggler-icon"></span>
                            </button>
                            <div class="collapse navbar-collapse" id="navbarResponsive">
                                <ul class="navbar-nav ml-auto">
                                </ul>
                            </div>
                            <div class="functional-buttons">
                            </div>
                            </div>
                        </nav>
                        </header>

                        <!-- Page Content -->
                        <!-- Banner Starts Here -->
                        <div class="banner">
                        <div class="container">
                            <div class="row">
                            <div class="col-md-8 offset-md-2">
                                <div class="header-text caption">
                                <h2 style=>Reporte de</h2>
                                <h1 style="color: white; font-size:120px; text-align: center; font-style: italic; font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; text-transform:uppercase">""" + tempName + """</h1>
                                </div>
                            </div>
                            </div>
                        </div>
                        </div>
                        <!-- Banner Ends Here -->""")

                    while simProd != None:
                        nameProd = str(simProd.value.name)
                        timeProd = str(simProd.value.totalTime)

                        html.write("""
                        <!-- Producto Starts Here -->
                        <hr>
                        <div style="padding-bottom: 100px;" class="services-section">
                            <div class="container">
                                <div class="row">
                                    <div class="col-md-8 offset-md-2">
                                        <div class="section-heading">
                                        <h2 style="text-transform:uppercase; text-align: center;">Proceso</h2>
                                        </div>
                                        <table class="table">
                                        <thead style="color:white; background-color: rgb(0, 50, 199); text-transform:uppercase; text-align: center;">
                                        <tr>
                                        <th scope="col">Segundo</th>""")

                        for i in range(lineNum):
                                html.write("""<th scope="col">Linea """ + str(i + 1) + """</th>""")

                        html.write("""</tr>
                            </thead>
                            <tbody>""")

                        elab = simProd.value.elaboration.first
                        while elab != None:
                            currentSec = str(elab.value.secNum)
                            currentList = elab.value.stepList.first
                            if int(currentSec) == int(int(numBreak) + 1):
                                break
                            html.write("""<tr>
                            <td>""" + currentSec + """</td>""")
                            while currentList != None:
                                NoLinea = str(currentList.value.lineNum)
                                action = str(currentList.value.action)            
                                html.write("""<td style="text-align: center;">""" + action + """</td>""")
                                currentList = currentList.next

                            html.write("""</tr>""")
                            elab = elab.next

                        html.write("""</tbody>
                                </table>
                                <h6 style="text-transform:uppercase; text-align: center; margin-top: 50px;">El producto """ + nameProd + """ se puede elaborar optimamente en """ + timeProd + """ segundos</h6>
                            </div>
                            </div>
                        </div>
                        </div>
                        <!-- Ascendente Ends Here -->""")
                        break

                    html.write("""<!-- Bootstrap core JavaScript -->
                        <script src="vendor/jquery/jquery.min.js"></script>
                        <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

                        <!-- Additional Scripts -->
                        <script src="assets/js/custom.js"></script>
                        <script src="assets/js/owl.js"></script>
                        <script src="assets/js/accordions.js"></script>


                    <script language = "text/Javascript"></script>
                    </body>
                    </html>
                
                    """)            
                    html.close()
                    print("\n")
                    print("Reporte creado con exito")
                    print("\n")
                    messagebox.showinfo("Información","Reporte creado con exito")
                    break
            else:
                alphaProd = alphaProd.next

        if Encontrado == False:
            print("\n")
            print("Producto no encontrado")
            print("\n")
