#!/usr/bin/perl


$string = "addddabaca";
$lunghezzaStringa = length($string);
@spl = split('a',$string);
$nuovaLunghezza = 0;
for (@spl){
    $nuovaLunghezza += length($_);
}
$occorrenze = $lunghezzaStringa - $nuovaLunghezza;
print "Occorrenze: $occorrenze";