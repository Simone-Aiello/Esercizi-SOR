#!/usr/bin/perl

#HASH DI ARRAY
@array_1 = (1,2,3);
@arrat_2 = (4,5,6);

%hash;
$hash{"francesco"} = [@array_1]; #abbiamo referenziato l'array, una sintassi uguale (che trovi su internet è) \@array1 

print "$hash{francesco}\n"; #Questo stampa l'indirizzo di memoria, essendo salvato nell'hash il rioferimento all'array

print "@{$hash{francesco}}\n"; #Dereferenziando l'array otteniamo quindi l'array stesso
push @{$hash{"francesco"}}, 10;
print "@{$hash{francesco}}\n";
#Si può fare anche il push su chiavi che non esistono
push @{$hash{"ianni"}}, 11;
print "@{$hash{ianni}}\n";

for (keys %hash){
    print "Chiave: $_ ---> @{$hash{$_}}\n";
}

for (values %hash){
    print "Valore --> @{$_}\n";
}

print "HASH DI HASH\n";

#HASH DI HASH alla fine basta vederlo come una matrice e si capisce cosa puoi fare
$HoH{primachiave}{francesco} = "ciao 1";
$HoH{primachiave}{denise} = "ciao 2";
$HoH{secondachiave}{francesco} = "ciao 11";
$HoH{secondachiave}{denise} = "ciao 22";
#print "$HoH{primachiave}{francesco}\n";



#Oppure
%HoH = (primachiave => {francesco => "1",denise => "2"}, secondachiave => {francesco => "11", denise => "22"});
#for (keys %HoH){
#    print "$_\n";
#}

for $ext (values %HoH){
    for $key (keys %{$ext}){
        print "$key --> ${$ext}{$key}\n";
    }
}
