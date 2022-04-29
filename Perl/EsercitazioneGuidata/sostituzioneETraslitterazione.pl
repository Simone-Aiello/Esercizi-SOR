#!/usr/bin/perl
$stringa = "Università della Calabria";
print "PRIMA: $stringa\n";

$stringa =~ s/della/ciao/; #sostituisce della con ciao, la modifica viene fatta direttamente sulla stringa originale

$stringa =~ s/\s//g; #Elimina gli spazi, g sta per global, senza di quello toglierebbe solo il primo spazio
print "DOPO: $stringa\n";

$stringa2 = "Università della Calabria";

$stringa2 =~ s/(.*)\s(.*)\s(.*)/\3 \2 \1/; #Inverte la stringa,  \1 \2 \3 sono la controparte di $1 $2 $3 nelle sostituzioni

print "$stringa2\n";

#Traslitterazione
print "TRASLITTERAZIONE\n";
$stringa3 = "Università della Calabria";

$stringa3 =~ tr/[a-z]/[A-Z]/; #controlla la stringa carattere per carattere, tr fa questo, quindi se il carattere fa match su [a-z] lo trasforma in [A-Z], quindi da minuscolo a maiuscolo. Funziona perchè [a-z] è una shortcut di a|b|c..|z

print "$stringa3\n";