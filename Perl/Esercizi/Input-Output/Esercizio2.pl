#!/usr/bin/perl
$persona = <STDIN>;
$numero = <STDIN>;
%rubrica;
chomp $persona;
while($persona ne "-1"){
    $p = $persona;
    $rubrica{$p} = $numero;
    $persona = <STDIN>;
    $numero = <STDIN>;
    chomp $persona;
}
while(($chiave,$valore) = each %rubrica){
    print "Persona: $chiave ha il numero: $valore";
}

@persone = keys %rubrica;
print "Le persone che ho in rubrica sono @persone";