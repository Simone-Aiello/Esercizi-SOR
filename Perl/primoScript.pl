#!/usr/bin/perl
#Scalari --> variabili che memorizzano un unico valore, intero, stringa, carattere, booleana
#Array --> contenitori di tipi base
#Mappe --> coppia chiave valore



#Dichiarazione e uso di scalari
$nome_variabile; #--> se non metto un valore di default è undef
$nome_variabile = 3; #--> tipo digit
$nome_variabile = "stringa"; #--> tipo string
$nome_variabile = undef; #--> non necessario, è di default
$nome_variabile = 1; #--> tipo booleano, non esiste true e false, perl decide se un numero è un bool o un digit in base al contesto, >= 1 true, 0 false

print "$nome_variabile \n";

if($nome_variabile){
    print "OK\n";
}

#Le varibili possono anche essere di tipo filehandle
#Se il file esiste lo sovrascrive (a meno che non lo apro con >> invece di >), se non esiste lo crea, se non ho i permessi per scrivere sul file non scrivo niente ma non mi viene segnalato a meno che non mi faccio stampare l'eccezione
#apro un file, lo manipolo tramite fh, lo apro in scrittura ">", e apro il file "testo.txt"
open($fh,">","testo.txt") || die $!; #$! è un eccezione propria del perl e mi da info sul perché non è riuscito a fare l'open, come ad esempio non ho i permessi di scrittura
#open($fh,">","testo.txt") || die "$! - Testo mio ciao" stessa cosa ma aggiungo del mio testo
print $fh "ciao"; #scrivo ciao nel file
close $fh;

#Apertura in lettura
open($fh, "<", "testo.txt") || die $!;
while($current_line = <$fh>){ #fh è un puntatore a file, con <> non mi riferisco alla variabile ma al suo contenuto
    print "$current_line \n"
}
close $fh;


#Dichiarazione e uso degli array
@array;
@array = (1,2,3);
#@matrice = ((1,2),(3,4),(5,6)) credo
$array[2] = 4; #Si usa il dollaro perché array[2] è uno scalare, non un array

$indice = $#array; #mi restituisce l'ultimo indice
$size = scalar @array; #scalar è un cast a scalare, ma visto che lo faccio su un array mi da la size
print "SIZE: $size\nm";
print "INDICE ULTIMO ELEMENTO: $indice\n";
print "ULTIMO VALORE ARRAY: $array[$indice]\n";
print "@array\n";


print "ULTIMO ELEMETNO $array[-1]\n"; #mi stampa l'ultimo elemento
print "PENULTIMO ELEMENTO $array[-2]\n";
#Se eccedo la size non stampa nulla

@new_array = @array[1..2]; #dico che voglio un nuovo array con gli elementi che vanno dall'indice 1 al 2 del vecchio array
print "Subset: @new_array\n";

@array = sort @array;

print "Sort: @array\n";

push @array, 5;
print "Push: @array\n";

pop @array;
print "Pop: @array\n";


unshift @array, 0; #aggiunge all'inizio dell'array un valore
print "UNSHIFT: @array\n";

shift @array; # rimuove il primo elemento dell'array
print"SHIFT: @array\n";


#NOTA BENE
#SORT su elementi stringa --> contesti perl

@to_sort = ("1","2","11");
@sorted = sort @to_sort; #fa il sort nel contesto stringa
print "Sorted: @sorted\n";

#Si possono fare array misti ma bisogna stare attenti ai contesti

#auto conversioni di perl
print "SIZE ARRAY " . @sorted . "\n"; #essendo la stringa una scalare, la concatenzaione converte l'array in scalare e quindi mi da la size, implicitamente chiama scalar @array


#Nota bene su pop/shift ARGV
#@ARGV contiene tutti gli argomenti passati allo script
print "$ARGV[0]\n";
$size_argv = scalar @ARGV;
$arg1 = shift @ARGV || die "L'argomento è obbligatorio"; #posso omettere argv e scrivere direttamente $arg1 = shift perché viene fatto di default su argv

#Mappe in perl

#%hash = ("francesco",1,"Giovanni",2);
%hash = ("francesco" => 1, "Giovanni" => 2);
#print %hash; #Non è detto che la print sia in ordine, le hash non sono ordinate

print "$hash{\"francesco\"}\n"; #nelle graffe ci va la chiave

#Cambia il valore
$hash{"francesco"} = 5;
print "$hash{\"francesco\"}\n";

$hash{"jacopo"} = 1;
print "$hash{'jacopo'} \n";
#Incremento il valore di 1
$hash{"jacopo"} = ++$hash{"jacopo"}; #nb usare $hash{"jacopo"}++ non funziona, restituisce prima il valore e poi incrementa (ricordi di fondamenti)

$hash{"mario"};
print "MARIO: $hash{'mario'}\n"; #Non stampa nulla
$hash{"mario"} += 1; #capisce in automatico che a mario associo interi, quindi di default mette lo zero e poi lo incrementa
print "MARIO DOPO: $hash{'mario'}\n";


#Control flow

#$cont = <STDIN>; #leggo da input
$cont = 12;
#Sono sintassi equivalenti, il primo è il postfix if, il secondo è il prefix if
print $cont if $cont > 10;

if ($cont > 10){
    print $cont;
}

#funzione
sub do_something{
    print "OK\n";
    $a = 3;
}

do_something if (1);
print "$a\n";

$name = "Bobby";
print "You're not Bob!\n" unless $name eq "Bob"; #contrario di if


#Variabili di default $_ per gli scalari, @_ per gli array
@array_nuovo = (6,7,8);
for $current_val (@array_nuovo){
    print "$current_val\n";
}

#In modo più conciso 
for (@array_nuovo){
    print "$_\n";
}
#for = foreach in perl
#foreach (@array_nuovo){
#    print "$_\n";
#}

#postfix for
print "$_\n" foreach (@array_nuovo);

#Scorrere array con un while

#Questo è un loop infinito, while (@array) itera fino a quando la size dell'array non è vuota
#while(@array_nuovo){
#    print "$_\n";
#}
while(@array_nuovo){
    $value = shift @array_nuovo;
    print "Value: $value\n";
}

$fine = 0;
until ($fine){ #è l'inverso del while
    print "Until\n";
    $fine++;
}


#break in perl = last
#continue in perl = next
#redo fa ripartire il ciclo senza controllare la condizione


#Scorrere array associativi (mappe)

%hash_nuovo = ("Francesco" => 1, "Giovanni" => 2);

#Metodo 1, prendere le chiavi e poi scorrerle:
@chiavi = keys %hash_nuovo;
for (@chiavi){
    print "$_ --> $hash_nuovo{$_}\n";
}

#Metodo 2 mi prendo direttramente i valori

@valori = values %hash_nuovo;

for(@valori){
    print "Valori: $_\n";
}

#Metodo 3 mi prendo entrambe le cose
while(($chiave,$valore) = each %hash_nuovo){
    print "$chiave ---> $valore\n";
}



#sort su hasmap
%hash_media_studente ("Francesco" => 19, "Denise" => 20, "Ianni" => 18);
#print %hash; Non è detto che vengano stampate in ordine

for(sort keys %hash_media_studente){ #prende le keys e ne fa un sort in ordine lessicografico
    print "$_ ---> $hash_media_studente{'$_'}\n";
}

#il sort consente di specificare una routine di ordinamento
for(sort{$a cmp $b} keys %hash_media_studente){ #sort classico su stringhe
    print "$_ ---> $hash_media_studente{'$_'}\n";
}

for(sort{$b cmp $a} keys %hash_media_studente){ #sort inverso su stringhe
    print "$_ ---> $hash_media_studente{'$_'}\n";
}

for(sort{$hash_media_studente{$a} <=> $hash_media_studente{$b}} keys %hash_media_studente){ #sort classico sui valori
    print "$_ ---> $hash_media_studente{'$_'}\n";
}
for(sort{$a <=> $b} values %hash_media_studente){ #così non posso risalire alle chiavi però
    print "Valori: $_\n";
}

#Voglio ordinare per valori, se due valori sono uguali allora ordina per chiave
for(sort{$hash_media_studente{$a} <=> $hash_media_studente{$b} || $a cmp $b } keys %hash_media_studente){ #sort classico sui valori
    print "$_ ---> $hash_media_studente{'$_'}\n";
}


#Split delle stringhe
$info = "root:x:0:0:root:/:/bin/bash";
@splitted_string = split(":",$info);


#NB split ha la precedenza come operatore, $splitted_string = split(":",$info)[-1] da errore di sintassi, bisogna fare così:
#Se lo chiudo tra parentesi eseguo prima split, viene salvato il risultato in una variabile temporanea e poi prendiamo l'ultimo elemento con [-1]
$last = (split(":",$info))[-1];

