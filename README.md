# Puccia Perfetta

Puccia perfetta is a program created by PoggioLevante for Valle Fiorita. It detects **Burned Puccias**.

## Requirements

sudo apt install libatlas-base-dev  

Python 3

Move to project's folder and use `pip install -r requirements.txt` to install the required dependencies.

## Configuration

Run *Picker.py* to start configuring the program.

`python Picker.py`

Select the source etc.etc.

Run *main.py* to start program

## Run

`python3 main.py` or `py -3 main.py`

# Puccia-Perfetta
Un sistema in grado di riconoscere, grazie ad una videocamera, delle pucce **bruciate** in fase di produzione e che notifica tramite un **attuatore** (sonoro o visivo) l'arrivo di quest'ultime. Il sistema è anche in grado di scrivere i dati raccolti su un foglio di calcolo google al fine di effettuare **analisi sulla produzione** ed è in grado di caricare foto su **Google Drive** con il fine di effettuare test e studi per migliorare il **riconoscimento** delle pucce da **scartare** in produzione. ![Puccia-perf](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/puccia-perf.png)

# Specifiche del progetto:
Il progetto è nato dall'esigenza di un'azienda che produce prodotti alimentari, di **facilitare** la vita al suo addetto al confezionamento. Quest'ultimo vedendosi arrivare moltissime pucce da impacchettare, necessitava di un **segnale** che lo avvisasse dell'arrivo di una puccia **"non buona",** in modo tale da prepararsi a scartarla. Per risolvere questo problema, abbiamo pensato ad un sistema costituito da da pochissimi componenti, come un **RaspBerryPi** che, attraverso una **telecamera** individua e segnala le pucce (per il momento solo quelle **bruciate**) da scartare. Per testare il codice scritto ***ad-hoc*** per il progetto abbiamo costruito un **nastro trasportatore** per *"simulare"* il nastro sul quale le pucce vengono portate dal forno alla zona di confezionamento, presente in azienda.
![Puccia-Demonstrator](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/demonstrator.jpg)

> *Il **processo** di ***costruzione*** del dimostratore non è descritto in questa documentazione, ma nel caso si volesse riprodurre, l'importante è avere bene in mente **l'idea** che serve un **nastro** che *scorre* (sul quale andranno adagiate le pucce) e una **videocamera** che *punta* proprio sul telo o nastro. In più basta un po' ***pazienza***, di ***creatività*** e un po' di ***olio di gomito***.

> Il nostro **dimostratore** è cosi composto:
> - 2 **tubi** di **plastica**
> - 3 **aste filettate** (per il supporto alla videocamera)
> - **Telo di stoffa**
> >**!IMPORTANTE**: Il telo sul quale poi dovranno scorrere le pucce è ***indispensabile*** che sia di un colore *unico e omogeneo* (e ovviamente diverso rispetto al colore delle pucce) in quanto, farà da **sfondo** alle immagini che catturerà la videocamera. (Un **maggiore** *contrasto di colori* permetterà un riconoscimento ottimale delle pucce) 
> - **Base di legno**
> - 4 **raccordi** stampati in **3d** (per le aste filettate)
> - **Shell** di **PLA** stampata in 3d dove riporre la telecamera
> - 10 **dadi**
> - 10 **rondelle**
> - 28 **viti** con le corrispettive ** farfalle**
> - **Manovella** per muovere il rullo stampata in **3d**
> - 6 **cuscinetti a sfera**
> - **Guarnizione di gomma** 

## Come funziona?
Dopo per aver configurato il tutto con uno **script** per la **configurazione**, un algoritmo analizza ***frame*** per ***frame*** le immagini che arrivano dalla videocamera e le da in pasto ad alcune funzioni **open-cv** come:
>- **cv2.cvtColor**(frame, cv2.COLOR_BGR2HSV): che converte il frame da **BGR** (*Blue, Green, Red*) a **HSV** (*Hue*, *Saturation*, *Lightness*) per la ***Color Detection*** delle Pucce.
> ![HSV_BGR](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/HSV_BGR_frame.png)
> - **cv2.findContours**(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE): che serve per la ricerca, all'interno dell' **frame-hsv**, *curve* che uniscono *linee continue di punti*. (Nello specifico cerca ***semi-archi*** che poi successivamente completa affinchè diventino **circonferenze**)

Grazie a queste funzioni  l'algoritmo riconosce le pucce presenti nell'immagine e gli assegna un **ID** (*univoco* per distinguere una puccia da un'altra durante *l'analisi dei frame*), poi effettua la **media colore** delle *circonferenze* (nello specifico la media colore del ***rettangolo iscritto nella circonferenze***). Se le medie rientrano in un determinato **range** di colori la puccia è *buona*, se invece rientra in un altro range è *bruciata*. A quel punto lo script **attiva**, attraverso un ***segnale digitale*** ed un Relè, la luce o una eventuale sirena (**l'attuatore**) per ogni puccia bruciata presente nel **frame**. Nel mentre l'algoritmo raccoglie **dati** (es. numero pucce buone, non buone etc.) e li scrive periodicamente su un *foglio Google*; parallelamente effettua ***l'upload*** di alcuni frame di pucce bruciate e *non* su ***Google Drive*** in *cartelle specifiche* (come già descritto nell'introduzione).
![Puccia-Conf](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/Sample_mdebug.png)


## Open Source e Documentazione:
Questo progetto è open source: chiunque può scaricare i file necessari, ricreare il progetto e contribuire al suo miglioramento. Non ci sono restrizioni di licenza d'uso, ma si invita a citare che è stato realizzato dagli studenti [ASIRID.](http://asirid.it)

Tutto il materiale necessario si trova [su GitLab.](https://gitlab.com/poggiolevante/puccia-perfetta)

## Requisiti HW:
![Puccia-RaspBox](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/rasp_box.jpg)
- **RaspBerryPi** [3B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/) con SD *(almeno da 16GB)* (o qualsiasi tipo di mini pc, che possa supportare Linux)
-  1 **Cavo di alimentazione** per RaspBerryPi
- 1 **Relè** (es. [questo](https://www.amazon.it/Elegoo-Channel-Accoppiatore-Arduino-Raspberry/dp/B06XRJ6XBJ/ref=asc_df_B06XRJ6XBJ/?tag=googshopit-21&linkCode=df0&hvadid=85509549383&hvpos=&hvnetw=g&hvrand=13632326945115656382&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1008080&hvtargid=pla-381339750175&psc=1) o simili)
- 3 **Jumper Femmina-Femmina** per collegare il Relè al Rasp. (5V-GND-SIGNAL)
- 1 **Videocamera USB** (di seguito viene riportata la [nostra](https://gitlab.com/poggiolevante/puccia-perfetta/-/blob/master/Resource/Doc/ELP-USB100W04H-KL139IR.pdf))
- 1 **ciabatta** con almeno **2 prese** (1 per l'attuatore e 1 per il cavo di alimentazione del Rasp.)
- 1 **cavo di alimentazione Maschio-Femmina** (con cui collegheremo la sirena o luce alla corrente)
- 1 **Sirena** o **Luce** 
> ***!Indispensabili*** per la configurazione iniziale ed una ***prima fase*** di **test** si consiglia di utilizzare:
> - 1 **mouse** (da collegare al **RaspBerryPi** tramite **USB**)
> - 1 **tastiera** (da collegare al **RaspBerryPi** tramite **USB**)
> - 1 **monitor** (da collegare al **RaspBerryPi** tramite un **cavo** **HDMI**)

>## Topologia:
>![Rasp_topology](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/TopologiaHW.png)
>***Vocabulary***:
>- **ATT_P**: cavo di alimentazione dell'attuatore (andrà spellato per collegare Fase, Neutro e Massa)
>- **RASP_P**: cavo di alimentazione del RaspBerryPi (nel caso di 3B+ il connettore sarà micro-usb)
>- **GPIO** (*General Purpose Input/Output*):  i PIN che la board di RaspBerryPi mette a disposizione per i segnali (Nel nostro caso quelli utilizzate saranno 3, utilizziamo il GPIO21 per attivare il relè, 5V e GND per fornire alimentazione al modulo del Relè)
>- **GND**: Massa
>- **NA**: Normalmente aperto
>- **NC**: Normalmente chiuso
>- **COM**: Comune
>- **VCC**: tensione di alimentazione
>- **IN1**: PIN del modulo del relè che serve per l'attivazione dell'attuatore (collegato tramite jumper al GPIO21 del Rasp.)
>- **POWER HUB**: la nostra ciabatta
>- **USB** (*Universal Serial Bus*): gli attacchi usb type-A femmina che la board RaspberryPi mette a disposizione (per collegare videocamera, monitor, tastiera e mouse)
>- **ATTUATORE**: la luce o sirena
>- **CONNETTORE**: connettore elettrico che congiungerà i cavi dell'attuatore (nello specifico NEUTRO e GND)
>>![Conn_Ele](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/Conn_ele.png)

## Requisiti SW:
- **Python3**
- Python3 **modules** 
- **Linux** (Debian)
- **Repository GitLab**: {[puccia-perfetta](https://gitlab.com/poggiolevante/puccia-perfetta)}
> ## Rep-Tree:
> La repository **è cosi composta**:
![Puccia-RaspBox](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/Rep_tree_img.png)
>- ***braccio-robotico***/: ***submodule*** alla [*repository*](https://gitlab.com/poggiolevante/braccio-robotico) del braccio-robotico, che attualmente *non è utilizzato* in questo progetto, ma verrà implementato in futuro.
>- ***Lib***/: contiene tutte le *librerie e classi* python utilizzate dai 3 script principali e la cartella **Creds/** per le *credenziali* (nel caso si voglia utilizzare le feature con **Google Drive**).
>- ***Config***/: contiene i file di salvataggio della configurazione fatta con ***Picker.py*** e ***main_debug.py***.
>- ***Resource***/: contiene cartelle che al loro interno contengono file **utili** a *questa documentazione* e al *progetto*.
>- ***Image_drive***/: conterrà **immagini**, *prese a campione (effettuate ad intervalli regolari)*, delle pucce.
>- ***Burned_Pucce***/: conterrà le **immagini** delle pucce ***bruciate rilevate***.
>- ***Main_scripts.py***: è l'insieme degli **script** *"principali"* (main.py, main_debug.py, Picker.py)

## Passi da seguire per l'implementazione:

## Stato attuale del progetto:
Il progetto è stato pubblicato a Maggio 2022, nella sua **prima versione** ed è **attualmente funzionante**.

> **Sviluppi futuri**:
>  - Implementare ***IA*** e ***ML*** per il riconoscimento delle pucce da scartare
>  - Riconoscimento delle **pucce crude**
>  - Riconoscimento delle **pucce** con una forma "***strana***"
>  - Implementare **braccio robotico** per scartare le pucce "*non buone*" 

## Autori:
**Software**: 
Tommaso Orlando, Rei Doda, Davide Palma e Nicola nargiso.
**Hardware** & **Dimostratore**:
Carmine Capece, Francesco Muccilli e Giovanni Pompigna.
>**Maggio 2022**