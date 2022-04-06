#!/usr/bin/perl
#Creare uno script che presi 2 interi in input ne mostri la somma, la
#differenza, il prodotto e il quoziente

#Rimodellare lo stesso programma facendo però uso delle
#subroutine. Creare quindi una subroutine che prende come
#parametri 2 variabili per ogni operazione matematica da eseguire

#Creare uno script che presi in input una sequenza di numeri
#positivi terminati da tappo "-1", li inserisca in un array e
#successivamente ne calcoli la somma

#Faccio un merge dei 3 io, prendo in input tutti i valori terminati da -1 salvandoli in un array, poi prendo un operazione da input e la calcolo sull'array

sub calcolatrice_povera{
    $_operazione = shift @_;
    $totale = $_operazione eq '*' ? 1 : 0;
    foreach (@_){
        if($_operazione eq '+'){
            $totale += $_;
        }
        elsif($_operazione eq '-'){
            $totale -= $_;
        }
        elsif($_operazione eq '*'){
            $totale *= $_;
        }
        else {
            die "Teoricamente qua non dovevi arrivarci :D";
        }
    }
    return $totale;
}

print "Inserisci i valori su cui vuoi effettuare l'operazione, -1 per terminare\n";
$valore = <STDIN>;
@valori = ();
while($valore != -1){
    chomp $valore; #NB chomp restituisce il numero di caratteri che ha rimosso, non la stringa, quella viene direttamente modificata
    push @valori, $valore;
    $valore = <STDIN>;
}
die "Inserisci almeno un valore" unless scalar @valori;
print "I valori inseriti sono: @valori\n";
print "Inserisci l'operazione da effettuare\n";
$operazione = <STDIN>;
chomp $operazione;
print "Operazione scelta: $operazione\n";
die "Operazione $operazione non supportata" unless $operazione eq '+' or $operazione eq '-' or $operazione eq '*';
print "Risultato: ",calcolatrice_povera($operazione,@valori),"\n";