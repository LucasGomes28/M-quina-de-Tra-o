from tkinter import*
import serial
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

fig = None
ax = None
line = None
canvas = None
global carga
global qnt_pulsos
global deformacao
global tensao
global x
global y
global count
global inicio
global espessura
global largura
global grip_separation
porta_aberta = False
teste_iniciado = False
x = list()
y = list()
count = 0.25
qnt_pulsos = 0
inicio = 0

def Salvar_Resultados():
    import tkinter
    from tkinter import ttk
    
    janela_salvar_prog = tkinter.Toplevel(app)
    janela_salvar_prog.title("Salvar Resultados")
    janela_salvar_prog.geometry("390x170+200+200")
    
    def salvarprog():
        global x
        global y
        global qnt_pulsos
        global numero_teste
        
        nome=str(NomeProg.get("1.0","end-1c"))
       
        x_txt=str(x)
        y_txt=str(y)
        qnt_pulsos_txt=str(qnt_pulsos)

        
        with open(nome + '.txt','w') as arquivo:
            arquivo.write(numero_teste + '\n')
            arquivo.write(qnt_pulsos_txt + '\n')
            arquivo.write(x_txt + '\n')
            arquivo.write(y_txt + '\n')
        
        janela_salvar_prog.destroy()
                
    def cancelarprog():
        janela_salvar_prog.destroy()
    
    text_salvar_prog=Label(janela_salvar_prog,text="Nome do arquivo: ",foreground="#000000")
    text_salvar_prog.place(x=1,y=30,width=170,height=15)
    
    NomeProg=Text(janela_salvar_prog,width=40,height=1)
    NomeProg.place(x=30,y=55)
    
    bt_salvarprog=Button(janela_salvar_prog,text="Salvar",background="#FFE4B5", command=salvarprog)
    bt_salvarprog.place(x=115,y=110,width=60,height=30)
    
    bt_cancelarprog=Button(janela_salvar_prog,text="Cancelar",background="#FFE4B5", command=cancelarprog)
    bt_cancelarprog.place(x=200,y=110,width=60,height=30)

def Abrir_Resultados():
    import tkinter
    from tkinter import ttk    
    janela_abrir_prog = tkinter.Toplevel(app)
    janela_abrir_prog.title("Abrir Resultados")
    janela_abrir_prog.geometry("390x170+200+200")
    
    def abrirprog():
        global x
        global y
        global qnt_pulsos
        global numero_teste
        
        plt.clf()
        plt.cla()
        plt.close()
        x.clear()
        y.clear()

        
        nome=str(NomeProg.get("1.0","end-1c"))
        
        with open(nome + '.txt','r') as arquivo:  
            numero_teste=arquivo.readline()
            qnt_pulsos_txt=arquivo.readline()
            x_txt=arquivo.readline()
            y_txt=arquivo.readline()

        #Removendo Caracteres Indesejados
        disallowed_characters = "[ ]\n"
        for character in disallowed_characters:
            numero_teste = numero_teste.replace(character, "")
            qnt_pulsos_txt = qnt_pulsos_txt.replace(character, "")
            x_txt = x_txt.replace(character, "")
            y_txt = y_txt.replace(character, "")


        #Separando as posições no vetor de posições    
        x=x_txt.split(',')             
        y=y_txt.split(',')  
        
        #Convertendo strings para float
        for g in range(0,len(x)):
            x[g] = float(x[g])
        for g in range(0,len(y)):
            y[g] = float(y[g])
        qnt_pulsos = float(qnt_pulsos_txt)
        numero_teste = int(numero_teste)
        
        tension_number.configure(text=numero_teste)
        val_max_load.configure(text=qnt_pulsos)
        criar_grafico()
        val_tempo.configure(text=x[len(x)-1])
        
        janela_abrir_prog.destroy()
                
    def cancelarabrir():
        janela_abrir_prog.destroy()
     
    text_abrir_prog=Label(janela_abrir_prog,text="Nome do arquivo: ",foreground="#000000")
    text_abrir_prog.place(x=1,y=30,width=170,height=15)
    
    NomeProg=Text(janela_abrir_prog,width=40,height=1)
    NomeProg.place(x=30,y=55)
    
    bt_abrirprog=Button(janela_abrir_prog,text="Abrir",background="#FFE4B5", command=abrirprog)
    bt_abrirprog.place(x=115,y=110,width=60,height=30)
    
    bt_cancelarabrir=Button(janela_abrir_prog,text="Cancelar",background="#FFE4B5", command=cancelarabrir)
    bt_cancelarabrir.place(x=200,y=110,width=60,height=30)
    
def conectar():
    import tkinter
    from tkinter import ttk
    
    def conect():
        global comunicacao
        global porta_aberta
        try:
            comunicacao = serial.Serial(comboBox_porta_COM.get(), comboBox_selecao_baudrate.get())
            time.sleep(2)  # espera o Arduino reiniciar
            comunicacao.reset_input_buffer()
            comunicacao.reset_output_buffer()
            try:
                _ = comunicacao.readline()
            except:
                pass
            bt_Conect.configure(text="CONECTADO",background="#028A0F", foreground="white", font=('Calibri', 11, 'bold'))
            porta_aberta = True
        except:
            messagebox.showerror('Conexão Serial', 'Erro: Não foi possível conectar!')
        janela_conectar.destroy()            
    
    def cancelar():
        janela_conectar.destroy()
        
    janela_conectar = tkinter.Toplevel(app)
    janela_conectar.title("Conectar")
    janela_conectar.geometry("270x170+200+200")

    
    text=Label(janela_conectar,text="Configuração da Porta Serial:",foreground="#000000")
    text.place(x=45,y=13,width=170,height=15)
    
    text_porta=Label(janela_conectar,text="Porta: ",foreground="#000000")
    text_porta.place(x=60,y=43,width=50,height=15)
    
    text_baud=Label(janela_conectar,text="Baudrate: ",foreground="#000000")
    text_baud.place(x=60,y=78,width=50,height=15)
    
    bt_conect=Button(janela_conectar,text="OK",background="#FFE4B5", command=conect)
    bt_conect.place(x=65,y=120,width=60,height=30)
    
    bt_cancelar=Button(janela_conectar,text="Cancelar",background="#FFE4B5", command=cancelar)
    bt_cancelar.place(x=140,y=120,width=60,height=30)
    
    COM_list=["COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9","COM10"]
    comboBox_porta_COM = ttk.Combobox(janela_conectar,values=COM_list, width=8)
    comboBox_porta_COM.place(x=115, y=41)
    comboBox_porta_COM.current(5)
    baud_list=[9600,19200,38400,57600,115200]
    comboBox_selecao_baudrate = ttk.Combobox(janela_conectar,values=baud_list, width=8)
    comboBox_selecao_baudrate.place(x=115, y=75)
    comboBox_selecao_baudrate.current(4)

        
def desconectar():
    global porta_aberta
    global teste_iniciado
    if teste_iniciado == True:
        messagebox.showerror('Desconectar', 'Erro: É necessário finalizar o teste!')
    elif porta_aberta == False:
        messagebox.showinfo('Desconectar', 'Desconectado!')
    else:
        porta_aberta = False
        comunicacao.close()
        bt_Conect.configure(text="Conectar",background="#98FB98", foreground="black", font=('Calibri', 10))
        val_cel.configure(text="****")
        messagebox.showinfo('Desconectar', 'Desconectado!')

def inicializar_grafico():
    """
    Cria a figura e o canvas uma única vez. Chamar quando o app iniciar
    ou quando iniciar um novo teste (após limpar x/y).
    """
    global fig, ax, line, canvas

    # Se já existir canvas, destrua o widget para evitar duplicatas
    try:
        if canvas is not None:
            canvas.get_tk_widget().destroy()
    except:
        pass

    # Cria figura e axes (sem usar plt)
    fig = Figure(figsize=(6.74, 3.58), dpi=100)  # tamanho aproximado ao area do widget
    ax = fig.add_subplot(111)
    ax.set_xlabel('Deformação (%)', fontsize=8)
    ax.set_ylabel('Tensão (MPa)', fontsize=8)
    ax.set_title('Tensão x Deformação', fontsize=12)

    # Cria a linha vazia que iremos atualizar
    line, = ax.plot([], [], linestyle='-', marker=None)

    # Cria o canvas uma vez e coloca no Tk
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=330, y=90, width=674, height=358)

    # força um primeiro desenho
    canvas.draw_idle()


def atualizar_plot():
    """
    Atualiza os dados da linha sem recriar a figura.
    Chame essa função periodicamente (ex.: app.after(100, atualizar_plot))
    """
    global x, y, fig, ax, line, canvas

    if fig is None or ax is None or line is None or canvas is None:
        # Se ainda nao inicializou, inicializa aqui
        inicializar_grafico()

    if teste_iniciado:
        # Proteja contra valores None ou NaN
        try:
            # Copia para evitar modificação concorrente (não é threading mas por segurança)
            xs = list(x)
            ys = list(y)
        except:
            xs = x
            ys = y

        if len(xs) > 0 and len(ys) > 0:
            # Atualiza dados da linha
            line.set_data(xs, ys)

            # Ajusta limites automaticamente
            ax.relim()
            ax.autoscale_view()

            # Desenha de forma eficiente
            canvas.draw_idle()

    # chamar de novo depois de 100 ms (10 fps). ajuste para 100-300 ms conforme precisar
    app.after(100, atualizar_plot)
    
def start():
    if porta_aberta == True:
        import tkinter
        from tkinter import ttk    
        janela_start = tkinter.Toplevel(app)
        janela_start.title("Iniciar Teste")
        janela_start.geometry("300x170+200+200")
        
        def inicia_teste():
            global count
            global teste_iniciado
            global inicio
            global numero_teste
            global qnt_pulsos
            global largura
            global espessura
            global grip_separation
            inicio = time.time()
            teste_iniciado = True
            espessura=str(Num_espessura.get())
            largura=str(Num_largura.get())
            grip_separation=str(Num_grip_separation.get())
            plt.clf()
            plt.cla()
            plt.close()
            x.clear()
            y.clear()
            inicializar_grafico()
            janela_start.destroy()
            codigo = 's'
            comunicacao.write(codigo.encode())
            
        def cancelarabrir():
            janela_start.destroy()
         
        text_espessura=Label(janela_start,text="Espessura (mm): ",foreground="#000000")
        text_espessura.place(x=48,y=15,width=170,height=15)
        
        Num_espessura=Entry(janela_start, width=10)
        Num_espessura.insert(0, "0.5")
        Num_espessura.place(x=190,y=15)
        
        text_largura=Label(janela_start,text="Largura (mm): ",foreground="#000000")
        text_largura.place(x=54,y=45,width=170,height=15)
        
        Num_largura=Entry(janela_start, width=10)
        Num_largura.insert(0, "20")
        Num_largura.place(x=190,y=45)
        
        text_grip_separation=Label(janela_start,text="Distância entre as garras (mm): ",foreground="#000000")
        text_grip_separation.place(x=10,y=75,width=170,height=15)
        
        Num_grip_separation=Entry(janela_start, width=10)
        Num_grip_separation.insert(0, "150")
        Num_grip_separation.place(x=190,y=75)
        
        bt_ok=Button(janela_start,text="OK",background="#FFE4B5", command=inicia_teste)
        bt_ok.place(x=70,y=110,width=60,height=30)
        
        bt_cancelar=Button(janela_start,text="Cancelar",background="#FFE4B5", command=cancelarabrir)
        bt_cancelar.place(x=165,y=110,width=60,height=30)
        
    else:
        messagebox.showerror('Iniciar Teste', 'Erro: Sem conexão!')
    
def stop():
    global teste_iniciado
    global x
    global y
    fim = time.time()
    tempo_decorrido = fim - inicio
    teste_iniciado = False
    print(f"Tempo decorrido: {tempo_decorrido} segundos")
    if porta_aberta == True:
        codigo = 'p'
        comunicacao.write(codigo.encode())

def ler_serial():
    global carga, qnt_pulsos, deformacao, tensao, espessura, largura, grip_separation

    if porta_aberta:
        try:
            linha = comunicacao.readline().decode(errors="ignore").strip()
            if linha:
                partes = linha.split(";")
                if len(partes) == 2:
                    carga = float(partes[0])
                    val_cel.configure(text=partes[0])
                    qnt_pulsos = float(partes[1])
                    if teste_iniciado:
                        tensao = float(carga)/(float(espessura) * float(largura)) #calcula a tensão para uma área do corpo de prova
                        tension_number.configure(text=round(tensao,2))
                        deformacao = round(((int(qnt_pulsos)*0.00125)/float(grip_separation))*100,2)
                        val_max_load.configure(text=deformacao)
                        tempo_decorrido = round((time.time() - inicio),2)
                        val_tempo.configure(text=tempo_decorrido)
                        x.append(deformacao)
                        y.append(tensao)
        except:
            pass

    app.after(1, ler_serial)

def down_pressed(event):
    if porta_aberta == True:
        if teste_iniciado == False:
            codigo = 'd'
            comunicacao.write(codigo.encode())
        else:
            messagebox.showerror('Descer', 'Erro: É necessário finalizar o teste!')
    else:
        messagebox.showerror('Descer', 'Erro: Sem conexão!')

def down_released(event):
    bt_down.config(relief="raised")
    if (porta_aberta == True) and (teste_iniciado == False):
        codigo = 'p'
        comunicacao.write(codigo.encode())

def up_pressed(event):
    if porta_aberta == True:
        if teste_iniciado == False:
            codigo = 's'
            comunicacao.write(codigo.encode())
        else:
            messagebox.showerror('Subir', 'Erro: É necessário finalizar o teste!')
    else:
        messagebox.showerror('Subir', 'Erro: Sem conexão!')
        
def up_released(event):
    bt_up.config(relief="raised")
    if (porta_aberta == True) and (teste_iniciado == False):
        codigo = 'p'
        comunicacao.write(codigo.encode())
    
app=Tk()
app.title("Máquina de Ensaio de Tração")
app.geometry("1024x768")
app.configure(background="#ECE9D8")

                   
Teste=Label(app,background="#ECE9D8", borderwidth=1, relief="solid")
Teste.place(x=10,y=60,width=300,height=398)
text_Teste=Label(app,text="TESTE",background="#ECE9D8",foreground="#000000")
text_Teste.place(x=20,y=70,width=30,height=15)

Dados=Label(app,background="#ECE9D8", borderwidth=1, relief="solid")
Dados.place(x=10,y=468,width=1004,height=228)
text_Dados=Label(app,text="DADOS",background="#ECE9D8",foreground="#000000")
text_Dados.place(x=20,y=478,width=45,height=15)

cel=Label(app,background="#000000", borderwidth=1, relief="sunken")
cel.place(x=20,y=508,width=238,height=178)
title_cel=Label(app,text="CÉLULA DE CARGA",background="#000000",foreground="#00FF40", font = ('Helvetica', 12, 'bold'), justify='center')
title_cel.place(x=20,y=520,width=237,height=20)
val_cel=Label(app,text="****",background="#000000",foreground="#00FF40", font = ('Helvetica', 26, 'bold'), justify='center')
val_cel.place(x=20,y=560,width=237,height=40)
und_cel=Label(app,text="N",background="#000000",foreground="#00FF40", font = ('Helvetica', 14, 'bold'), justify='center')
und_cel.place(x=20,y=610,width=237,height=24)

tempo=Label(app,background="#000000", borderwidth=1, relief="sunken")
tempo.place(x=765,y=508,width=238,height=178)
title_tempo=Label(app,text="TEMPO",background="#000000",foreground="#00FF40", font = ('Helvetica', 12, 'bold'), justify='center')
title_tempo.place(x=765,y=520,width=237,height=20)
val_tempo=Label(app,text="****",background="#000000",foreground="#00FF40", font = ('Helvetica', 26, 'bold'), justify='center')
val_tempo.place(x=765,y=560,width=237,height=40)
und_tempo=Label(app,text="s",background="#000000",foreground="#00FF40", font = ('Helvetica', 14, 'bold'), justify='center')
und_tempo.place(x=765,y=610,width=237,height=24)

max_load=Label(app,background="#000000", borderwidth=1, relief="sunken")
max_load.place(x=517,y=508,width=238,height=178)
title_max_load=Label(app,text="DEFORMAÇÃO",background="#000000",foreground="#00FF40", font = ('Helvetica', 12, 'bold'), justify='center')
title_max_load.place(x=517,y=520,width=237,height=20)
val_max_load=Label(app,text="****",background="#000000",foreground="#00FF40", font = ('Helvetica', 26, 'bold'), justify='center')
val_max_load.place(x=517,y=560,width=237,height=40)
und_max_load=Label(app,text="%",background="#000000",foreground="#00FF40", font = ('Helvetica', 14, 'bold'), justify='center')
und_max_load.place(x=517,y=610,width=237,height=24)

tension=Label(app,background="#000000", borderwidth=1, relief="sunken")
tension.place(x=268,y=508,width=238,height=178)
title_tension=Label(app,text="TENSÃO",background="#000000",foreground="#00FF40", font = ('Helvetica', 12, 'bold'), justify='center')
title_tension.place(x=268,y=520,width=237,height=20)
tension_number=Label(app,text="****",background="#000000",foreground="#00FF40", font = ('Helvetica', 26, 'bold'), justify='center')
tension_number.place(x=268,y=560,width=237,height=40)
und_tension=Label(app,text="MPa",background="#000000",foreground="#00FF40", font = ('Helvetica', 14, 'bold'), justify='center')
und_tension.place(x=268,y=610,width=237,height=24)

Resultados=Label(app,background="#ECE9D8", borderwidth=1, relief="solid")
Resultados.place(x=320,y=60,width=694,height=398)
text_Resultados=Label(app,text="RESULTADOS",background="#ECE9D8",foreground="#000000")
text_Resultados.place(x=330,y=70,width=70,height=15)

bt_Conect=Button(app,text="Conectar",background="#98FB98",command=conectar)
bt_Conect.place(x=10,y=10,width=145,height=40)
bt_Disconect=Button(app,text="Desconectar",background="#F0E68C",command=desconectar)
bt_Disconect.place(x=165,y=10,width=145,height=40)
bt_Salvar=Button(app,text="Salvar Resultados",background="#F0E68C",command=Salvar_Resultados)
bt_Salvar.place(x=320,y=10,width=145,height=40)
bt_Abrir=Button(app,text="Abrir Resultados",background="#F0E68C",command=Abrir_Resultados)
bt_Abrir.place(x=475,y=10,width=145,height=40)

image_up = PhotoImage(file=r"C:\Maquina_Tracao\up.png")
bt_up=Button(app,background="#ECE9D8", image= image_up)
bt_up.place(x=30,y=130,width=125,height=125)
image_start = PhotoImage(file=r"C:\Maquina_Tracao\start.png")
bt_start=Button(app,background="#ECE9D8", image= image_start, command=start)
bt_start.place(x=165,y=130,width=125,height=125)
image_down = PhotoImage(file=r"C:\Maquina_Tracao\down.png")
bt_down=Button(app,background="#ECE9D8", image= image_down)
bt_down.place(x=30,y=268,width=125,height=125)
image_stop = PhotoImage(file=r"C:\Maquina_Tracao\stop.png")
bt_stop=Button(app,background="#ECE9D8", image= image_stop, command=stop)
bt_stop.place(x=165,y=268,width=125,height=125)


bt_down.bind("<ButtonPress-1>", down_pressed)
bt_down.bind("<ButtonRelease-1>", down_released)

bt_up.bind("<ButtonPress-1>", up_pressed)
bt_up.bind("<ButtonRelease-1>", up_released)

app.after(1, ler_serial)
app.after(100, atualizar_plot)
app.mainloop()