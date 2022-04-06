#!/usr/bin/perl
%map = ("A" => 1, "B" => 2);
print "La chiave A ha il valore $map{'A'}\n";
$map{"A"} = 0;
$map{"C"} = 3;
$map{"D"} = 4;
$map{"E"} = 5;
$map{"F"} = 6; 
if(exists($map{"C"})){
    print "La C è presente come chiave\n";
}
else{
    print "La C NON è presente come chiave\n";
}

@slice = @map{"A","B"};  #se metti più di un parametro te li ritorna come lista
print "@slice\n";

@keys = keys %map;
@both = @keys;
unshift @both, values %map;# crea un array unico di valori e chiavi
print "@keys\n";
print "@both\n"; 


for(@keys){
    print "Chiave $_, Valore $map{$_}\n";
}

$len = scalar @keys; #Visto che lo assegno ad uno scalare il context scalare è già settato, parola scalar superflua
print "Lunghezza hash $len\n";

delete $map{"A"}; #rimuove un elemento
print keys %map;