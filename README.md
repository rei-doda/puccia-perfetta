# Puccia-Perfetta
Un sistema in grado di riconoscere, grazie ad una videocamera, delle pucce **bruciate** in fase di produzione e che notifica tramite un **attuatore** (sonoro o visivo) l'arrivo di quest'ultime. Il sistema è anche in grado di scrivere i dati raccolti su un foglio di calcolo google al fine di effettuare **analisi sulla produzione** ed è in grado di caricare foto su **Google Drive** con il fine di effettuare test e studi per migliorare il **riconoscimento** delle pucce da **scartare** in produzione. ![Puccia-perf](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/puccia-perf.png)

# Specifiche del progetto:
Il progetto è nato dall'esigenza di un'azienda che produce prodotti alimentari, di **facilitare** la vita al suo addetto al confezionamento. Quest'ultimo vedendosi arrivare moltissime pucce da impacchettare, necessitava di un **segnale** che lo avvisasse dell'arrivo di una puccia **"non buona",** in modo tale da prepararsi a scartarla. Per risolvere questo problema, abbiamo pensato ad un sistema costituito da pochissimi componenti, come un **RaspBerryPi** che, attraverso una **telecamera** individua e segnala le pucce (per il momento solo quelle **bruciate**) da scartare. Per testare il codice scritto ***ad-hoc*** per il progetto abbiamo costruito un **nastro trasportatore** per *"simulare"* il nastro sul quale le pucce vengono portate dal forno alla zona di confezionamento, presente in azienda.
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
>- ***Main_scripts.py***: è l'insieme degli **script** *"principali"* (*main.py, main_debug.py, Picker.py*)

## Passi da seguire per l'implementazione:
Dopo aver preparato e collegato tutti i dispositivi come riportato nella topologia *in figura*, avviare il **RaspBerryPi** e :
- Aprire il **terminale** Linux
- Lanciare i seguenti ***comandi*** (con i ***privilegi di amministratore***):

```console
rasp@puccia:~$ sudo apt install libatlas-base-dev
# per installare le librerie di base
rasp@puccia:~$ sudo apt-get update && sudo apt full-upgrade -y
# per aggiornare l'intero sistema
```
- Spostarsi tramite ***console*** nel percorso/cartella che più si preferisce e lanciare il comando:
```console
rasp@puccia:~$ git clone https://gitlab.com/poggiolevante/puccia-perfetta
# per scaricare la repository da Gitlab
```
- Spostarsi nella cartella della repository *appena scaricata*:
```console
rasp@puccia:~$ cd ../puccia-perfetta
```
- Installare le ***librerie necessarie*** per gli script del progetto, tramite *questo comando*:
```console
rasp@puccia:~$ pip3 install -r requirements.txt
# requirements.txt è un file presente nella repository che riporta tutte le librerie utilizzate
```
- A questo punto avviare **.\Picker.py** (*specifico per la configurazione iniziale*), lanciando questo comando:
```console
rasp@puccia:~$ python3 Picker.py
# questo script oltre alla configurazione, serve per impostare "l'ambiente di lavoro" creando anche alcune le cartelle viste nel Rasp-tree riportato qui sopra
```
>Questo è quello che vi si presenterà:
>![Picker_begin](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/Picker_begin.png)
>- Muovere lo slider ***Stream_Port*** fino a selezionare lo stream della videocamera che ci interessa e premere ***q*** per selezionarla e passare alla configurazione successiva.
> > Altrimenti è possibile cliccare **s** per *switchare* da *Stream_Mode* a ***Resource_Mode***, che è una modalità che permette di selezionare dei video da utilizzare per la *configurazione*. Video che devono essere messi in **.\Resource\Media** (i formati supportati sono: *".mp4", ".avi", ".wmv"*).
> 
> Successivamente di apriranno queste finestre:
> ![Picker_conf](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/Picker_conf.png)
>>**!ATTENZIONE**: nel caso non si riuscisse a visualizzare l'intera schermata degli slider, posizionatevi con il cursore sopra la finestra, cliccateci e contemporaneamente premete *Alt* e spostatela verso l'alto fino a scoprire il resto degli slider.
>
>  Vediamo la *funzionalità* degli ***slider***:
>  - **L-H, U-H, L-S, U-S, L-V, U-V**: questi slider servono ad isolare il soggetto da riconoscere (nel nostro caso ***le pucce***). Finestra a cui fare riferimento: **Bitwise/Color** (*BiancoNero/Colorata*).
>  - **Morph_op, Morph_cl**: questi slider  servono per eliminare ***"rumore"*** o ***"imprecisioni"*** dalla **maschera HSV** creata con gli *slider precedenti*. Finestra a cui fare riferimento: **Morph/Blurred** (si può notare l'effetto di questi slider mettendo a paragone la finestra *Bitwise* e la finestra *Morph*).
> - **Blur**: serve per mettere un ***effetto sfocatura*** alla ***maschera HSV***, nel caso fosse necessaria, al fine di isolare maggiormente la puccia. Finestra a cui fare riferimento: **Morph/Blurred**.
> - **Brightness**: serve per regolare la ***luminosità*** dell'immagine.
> - **Contrast**: serve per regolare il ***contrasto*** dell'immagine.
> - **Saturation**: serve per regolare la ***saturazione*** dell'immagine.
> - **Hue**: serve per regolare la ***tonalità*** dell'immagine.
> - **Gamma**: serve per regolare la ***correzione gamma*** dell'immagine.
> - **Auto_WB**: serve per attivare o meno il ***bilanciamento automatico dei bianchi***.
> - **Min_radius, Max_radius**: servono rispettivamente per selezionare il *raggio* *minimo* e il *raggio massimo* (in questo caso delle nostre pucce) che il nostro sistema deve rilevare. Finestra di riferimento: **Frame_radius**. Dall'immagine di possono notare due circonferenze: quella **blu** (*Min_radius*), quella **rossa** (Max_radius).
> - **Arm_verse**, **Arm_limiter**: servono per il braccio-robotico, nello ***stato attuale*** del progetto non ***vanno utilizzati***.
>- **Roi_x, Roi_y**, **wx**, **wy** : utilizzati in combinazione con ***wx*** e ***wy*** per delimitare un ***Range of Interest*** a partire dal frame HSV. Questo per eliminare dal frame che sarà dato in pasto allo script, eventuali *porzioni periferiche* dell'immagine ***non necessarie***. Finestra di riferimento: **Frame_radius** (*Roi visibile grazie al  rettangolo blu*).
>- **Morph_Blur**: serve per scegliere quali effetti usare sul **frame HSV**, se settato a **0** usa sia il ***blur*** che l'effetto dato dai ***morph***, se settato a **1** utilizza solo i ***morph***, se settato a **2** invece utilizza solo il ***blur***.
>- **Debug_mode**: serve per avviare a *configurazione **finita*** un altro script, nello specifico ***main_debug.py***. Se settato a **0** *non avvierà nulla*, se settato a **1** lo avvierà.

- Una volta conclusa la configurazione con **.\Picker.py** premere "***s***" per *salvare* (oppure "***q***" per uscire *senza salvare*).
>**!ATTENZIONE**: il file di configurazione che verrà salvato in .**\Config** è indispensabile per l'utilizzo degli script ***main_debug.py*** e ***main.py***, senza il file di configurazione gli script non partono.
- A questo punto avviare **main_debug.py**, per effettuare un altro tipo di configurazione (nello specifico per stabilire ***il range*** di media colore per il quale una puccia può considerarsi "*buona*" o "*bruciata*") tramite il comando:
```console
rasp@puccia:~$ python3 main_debug.py
```
>Queste sono le schermate che si presenteranno:
>![Puccia-Conf](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/Sample_mdebug.png)
>Lo script è molto simile al **.\Picker.py**, serve per visualizzare in *tempo reale* gli effetti della configurazione fatta e nel caso sistemare qualche valore come per esempio il *raggio*. Mostra la finestra **"Operative_Mask"** che non è altro che la *maschera*, costruita con la configurazione precedente, che lo script utilizza per *rilevare le pucce*. L'altra finestra: **"Puccia_Cam"** da cui è possibile vedere in tempo reale il ricoscimento della puccia, al centro si trova **l'ID**, in alto a sinistra il valore del ***raggio rilevato*** e in alto a destra la ***media colore*** (se è buona avrà un valore *alto*, se è bruciata il valore sarà *basso*).
>Gli slider presenti sono praticamente *gli stessi* di .\Picker.py, con un aggiunta però:
>- **mAVG_color, MAVG_color**: (*valore minimo, valore massimo*) muovendo questi slider si vanno a selezionare *i valori della media colore* per il quale la puccia riconosciuta è considerata ***buona*** o ***bruciata***. (Nel caso fosse buona il ***cerchio di rilevazione*** sarà **verde**, se bruciata invece sarà **rosso**).

- Conclusa anche la configurazione con il **.\main_debug.py** premere "s" per salvare.
- A questo punto dovrebbe avviarsi in automatico **\main.py**,  lo script principale. Nel caso non si avviasse:
```console
rasp@puccia:~$ python3 main.py
# eseguire il comando nella cartella della repository
```
- Il sistema adesso è in grado di rilevare correttamente e segnalare le pucce, tra le schermate troviamo:
![Puccia-main](https://gitlab.com/poggiolevante/puccia-perfetta/-/raw/master/Resource/Media/Puccia-main.png)
Le finestre *Operative_Mask* e *Puccia_CAM* sono le stesse di **.\main_debug.py**, sulla finestra del terminale invece saranno stampati eventuali messaggi: per esempio quando la scrittura sul foglio verrà effettuata con successo. Oppure **messaggi di errore**, con *descrizione* (e ovviamente gli **ID** delle *pucce presenti* in *Puccia_CAM*).

## Configurazione delle credenziali per Google Drive:
Per utilizzare le **feature** di *upload* di **dati e immagini** necessitiamo di alcuni file che permetteranno al sistema di *autenticarsi* e quindi di ricevere i *permessi di scrittura* e *upload*.
- Per la procedura di creazione delle *credenziali* per scrivere su **Google sheet**, rimandiamo a questo [video](https://www.youtube.com/watch?v=4ssigWmExak&t=814s) (dal minuto 3:40 in poi). Una volta scaricato il file **.json** rinominarlo in ***creds.json*** e spostarlo in ***.\Lib\Creds***.
- Invece per la creazione dei file **.json** per l'upload di immagini, consigliamo di seguire questa [guida](https://gitlab.com/poggiolevante/puccia-perfetta/-/blob/master/Resource/Doc/Get+Authentication+for+Google+Service+API+.pdf). Una volta creati i file ***"settings.yaml"*** e ***"client_secrets.json"*** spostarli nella cartella ***.\Lib\Creds***.

Avviato lo script **main.py** vi chiederà di fare l'accesso con l'*account Google* con il quale avete creato le **credenziali**. Fatto la prima volta non vi sarà più richiesto.

## Demone Linux:
Per eseguire lo script *all'avvio* del **RaspBerryPI**:
- Aprire [questo](https://gitlab.com/poggiolevante/puccia-perfetta/-/blob/master/Resource/Puccia-Daemon.service) **file**
- **Modificare** le voci racchiuse tra **< .. >** (*es. al posto di <abs_path_puccia-perfetta> va messo il percorso assoluto della repository*)
- Copiare il file in  **/etc/systemd/system/**
- Poi *attivarlo* con il **comando** da terminale:
```console
rasp@puccia:~$ sudo systemctl enable Puccia-Daemon
# Al riavvio del RaspBerryPI lo script partirà automaticamente
```
- Nel caso si volesse far partire **subito** senza riavviare: 
```console
rasp@puccia:~$ sudo systemctl start Puccia-Daemon
```

## Variabili modificabili: 
Variabili presenti in **.\main.py**:
```python
19 - fold_image_drive_burned = "<str>" # token della cartella Google Drive che conterrà le immagini delle pucce bruciate rilevate
20 - fold_image_drive_random = "<str>" # token della cartella Google Drive che conterrà le immagini prese a campione
28 - interval = <int> # intervallo di tempo (in minuti) per stabilire ogni quanto lo script fara uno screen delle pucce prese a campione 
31 - block_hour = <int> # range(1, 24) ora in cui lo script caricherà le immagini su drive  
32 - block_min = <int> # range(0, 60) minuto in cui lo script caricherà le immagini su drive
33 - block_sec = <int> # range(0, 60) secondo in cui lo script caricherà le immagini su drive  
34 - sheet_name = "<str>" # nome del foglio google su cui andranno scritti i dati raccolti
```

## Stato attuale del progetto:
Il progetto è stato pubblicato a Maggio 2022, nella sua **prima versione** ed è **attualmente funzionante**.

> **Sviluppi futuri**:
>  - Implementare ***IA*** e ***ML*** per il riconoscimento delle pucce da scartare
>  - Riconoscimento delle **pucce crude**
>  - Riconoscimento delle **pucce** con una forma "***strana***"
>  - Implementare **braccio robotico** per scartare le pucce "*non buone*" 

## Autori:
**Software**: 
Tommaso Orlando, Rei Doda, Davide Palma e Nicola Nargiso.

**Hardware** & **Dimostratore**:
Carmine Capece, Francesco Muccilli e Giovanni Pompigna.
>**Maggio 2022**