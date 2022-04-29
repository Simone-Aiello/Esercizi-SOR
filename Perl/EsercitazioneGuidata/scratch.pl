#!/usr/bin/perl

print "Inserire una stringa in input:\n";
$input = <STDIN>;
#Quando prendiamo da input una parola, viene in automatico preso anche \n alla fine, per risolvere si usa chomp
chomp $input; #Rimuove \n dalla fine delle stringhe
print "$input\n";

#NB chop invece cancella l'ultimo carattere, indipendentemente se sia uno \n o un altro carattere
chop $input;
print "$input\n";

#funzioni in perl
sub funzione{
    print "Sono all'interno della funzione\n";
    print "I parametri passati sono: @_\n";
    print "Il valore in posizione 0 è: $_[0]\n";

    #Si può anche usare la funzione shift
    $parametro = shift @_ or die "Nessun parametro";
    #Oppure se vogliamo mettere un valore di default $parametro = shift @_ or $parametro = "valore di default";
    #$parametro = shift; è uguale, nel caso delle funzioni il fatto che sia su @_ è implicito
    print "Primo parametro della funzione con lo shift è $parametro\n";
    print "\n";
}
funzione("hello");


#Cose sugli array
@array = ("Ciao\n","come stai?\n");
@array2 = (1,2,3);
#$_ prende il valore in base al contesto
for (@array){
    chomp; #Toglie \n su $_;
    print "$_"; #QUa prende i valori del primo array
    for (@array2){
        print "$_ ";# Qua del secondo
    }
    print "\n";
}


#regex
for (@array){
    chomp;
    print "$_\n";
    if(/come/){ #In automatico fa il match su $_, è come se scrivessi $_=~ /come/
        print "Trovata la parola \"come\"\n";
    }
}

#Regex per ip

$ip_address = "192.168.1.107";
$ip_address =~ /(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/;

#^CAPTURE è una referenza che contiene tutti i gruppi matchati
#@{^CAPTURE} lo dereferenziamo quindi otteniamo un array
print "Tutti i gruppi: @{^CAPTURE}\n";

for(1..@{^CAPTURE}){
    print "$$_\n"; #$_ nella prima iterazione è 1, quindi $1 è il primo gruppo $($_) -> $1 -> 192
}