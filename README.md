# projekts riepas mmk

Riepu meklēšanas rīks MMKriepas.lv vietnei
Projekta uzdevums:
Šī projekta mērķis ir izveidot automatizētu riepu meklēšanas rīku, kas ievāc lietotāja ievadītos parametrus un veic riepu meklēšanu e-veikalā MMKriepas.lv. Projekts ļauj lietotājam:

Ievadīt riepu meklēšanas parametrus (platums, augstums, diametrs, sezona, ražotājs)

Automātiski atvērt pārlūkprogrammu un aizpildīt meklēšanas formas laukus

Veikt meklēšanu pēc norādītajiem kritērijiem

Parādīt meklēšanas rezultātus

Programma ir paredzēta lietotājiem, kas vēlas ātri un efektīvi atrast piemērotas riepas pēc precīziem izmēriem un citiem parametriem, izvairoties no manuālas meklēšanas veikšanas vietnē.

Izmantotās Python bibliotēkas
Selenium - galvenā bibliotēka, kas tiek izmantota pārlūkprogrammas automatizācijai. Tā ļauj:

Automātiski atvērt un kontrolēt Chrome pārlūkprogrammu

Atrast un mijiedarboties ar elementiem web lapā

Aizpildīt formas un veikt darbības kā lietotājs

Time - izmantota paužu ieviešanai starp darbībām, lai nodrošinātu, ka visas lapas komponentes ir pareizi ielādējušās pirms ar tām mijiedarbosies.

WebDriverWait un Expected Conditions - Selenium komponentes, kas palīdz gaidīt noteiktu elementu parādīšanos vai kļūšanu interaktīvu pirms turpināt izpildi. Tas ir būtiski, jo mūsdienu web lapas bieži izmanto asinhronu ielādi.

Datu struktūras
Projektā tiek izmantota šāda lietotāja definēta datu struktūra:

filters = {'platums': '', 'augstums': '', 'diametrs': '', 'sezona': '', 'razotajs': ''}

Šī vārdnīca tiek izmantota, lai saglabātu lietotāja ievadītos meklēšanas parametrus. Pēc ievades, tiek veikta šīs struktūras attīrīšana, noņemot tukšos laukus:
filters = {k: v for k, v in filters.items() if v}
Šī pieeja ļauj elastīgi apstrādāt dažādu skaitu ievades parametrus un nodrošina, ka meklēšana tiek veikta tikai pēc norādītajiem kritērijiem.
Programmatūras izmantošanas metodes
Lietotāja saskarne:

Programma prasa lietotājam ievadīt meklēšanas parametrus

Katrs parametrs ir neobligāts - lietotājs var ievadīt vienu vai vairākus kritērijus

Ja nav ievadīts neviens parametrs, programma prasīs ievadi atkārtoti

Pārlūkprogrammas kontrole:

Tiek izmantots Chrome pārlūkprogrammas draiveris ar maksimizētu logu

Tiek atvērta MMKriepas.lv riepu meklēšanas lapa

Programma pārbauda, vai meklēšanas forma ir pieejama pirms turpināšanas

Formas aizpildīšana:

Katram ievades parametram tiek atrasts atbilstošais izvēles lauks

Tiek atvērts izvēlnes lauks un ievadīta lietotāja vērtība

Tiek meklēta un atlasīta atbilstošā opcija no nolaižamā saraksta

Pēc veiksmīgas izvēles tiek veikta 1 sekundes pauze

Meklēšanas rezultāti:

Pēc visu parametru ievades tiek noklikšķināts uz meklēšanas pogas

Programma gaidīs rezultātu ielādi un pēc tam paliks atvērta, lai lietotājs varētu apskatīt rezultātus

Ja rodas kļūda, programma informē lietotāju un paliek atvērta kļūdas analīzei

Ievades parametru apstrāde
Programma veic šādas ievades datu pārbaudes un transformācijas:

Sezonas parametrs tiek pārveidots ar pirmo lielo burtu (capitalize())

Visi ievades dati tiek apstrādāti, noņemot liekās atstarpes (strip())

Pārbauda, vai vismaz viens meklēšanas parametrs ir norādīts

Kļūdu apstrāde
Programma izmanto izņēmumu apstrādi, lai:

Uztvertu un apstrādātu laika noilguma kļūdas

Paziņotu lietotājam, ja nevar atrast vai atlasīt kādu no meklēšanas parametriem

Paziņotu par kritisku kļūdu, ja nevar ielādēt meklēšanas lapu vai veikt meklēšanu

Video demonstrācija
Saite uz video demonstrāciju - šeit var ievietot saiti uz video, kurā redzama programmas darbība. Video parāda:

Lietotāja ievades procesu

Automātisko pārlūkprogrammas atvēršanu

Formas aizpildīšanu

Meklēšanas rezultātu parādīšanos

Papildu piezīmes:
Projektā varētu turpmāk izstrādāt:

Rezultātu datu iegūšanu un saglabāšanu

Vairāku lapu meklēšanas rezultātu apstrādi

Cenu salīdzināšanas funkciju

Grafisko lietotāja saskarni ievades vienkāršošanai

Programma ir izstrādāta kā komandrindas rīks, kas ļauj to integrēt citās sistēmās vai izmantot kā atsevišķu rīku ātrai riepu meklēšanai.