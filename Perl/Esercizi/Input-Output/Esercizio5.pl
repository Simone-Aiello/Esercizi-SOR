#!/usr/bin/perl

$string = "mi fa male la testa";

$lunghezza = length($string);
$reversed = "";
for(0..$lunghezza -1){
    $reversed = $reversed . substr($string,$lunghezza-1-$_,1);
}
print "$reversed\n";
#Soluzione one line: print scalar reverse($string);
$rev = reverse($string); #Se il contesto scalare glielo imponiamo con un assegnamento la keyword scalar non serve
#Reverse funziona anche sugli array
print "$rev\n";