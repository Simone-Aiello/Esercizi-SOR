#!/usr/bin/perl
$str1 = <STDIN>;
$str2 = <STDIN>;
chomp $str1;
chomp $str2;
#Tre metodi equivalenti
#$string = "$str1$str2";
$string = $str1 . $str2;
#$string = join '',$str1,$str2;
$lunghezza = length($string);
print "La stringa $string è di lunghezza $lunghezza\n";
$mid = $lunghezza/2;
$secmeta = substr($string,$mid,$lunghezza-$mid);
print "La seconda metà della nuova stringa è: $secmeta\n";