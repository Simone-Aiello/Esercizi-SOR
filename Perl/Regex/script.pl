#!/usr/bin/perl
$testo = "Oggi è una bella giornata";

#!~ è il contrario, se non matcha torna true
if($testo =~ /la/){
    print "La stringa $testo verifica il match con /la/\n";
}

#di default .* mangi più caratteri possibili, per fare il match con meno caratteri posibili si fa così .*? (idem .+?)
@matches = ($testo =~ /ora/g); #mette nell'array tutti i match di ora, senza la g le regex si fermano al primo match

#codice fiscale
$testo = "LLASMN00M14C352J";
if($testo =~ /^([A-Z]{3})([A-Z]{3})(\d{2})([A-Z])(\d{2})([A-Z]\d{3})([A-Z])$/){
    print "Il giorno del mese di nascita è $5\n";
}

$regex = "([A-Z]{3})([A-Z]{3})(\d{2})([A-Z])(\d{2})([A-Z]\d{3})([A-Z])";
if($testo =~ /$regex/){
    print "Il giorno del mese di nascita è $5\n";
}

#Se una regex prevede più match si può fare così per ciclare su di essi
while ($testo =~ /$regex/){
    print "Il giorno del mese di nascita è $5\n";
}

$data = qx(date);
$data =~ /([0-9]{2}):([0-9]{2})/;
print("Sono le ore $1 e $2 minuti\n");

$_ = qx(date);
#funziona anche, se non metto =~ perl lo matcha direttamente su $_
/([0-9]{2}):([0-9]{2})/;
print("Sono le ore $1 e $2 minuti\n");
