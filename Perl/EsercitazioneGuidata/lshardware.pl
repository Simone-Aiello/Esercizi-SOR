#!/usr/bin/perl

$mode = shift or die "Inserire un opzione [-s|-b]";

if($mode eq "-b"){
    stampa_info();
}
elsif($mode eq "-s" || die "Opzione specificata non è supportarta $mode"){
    salva_su_file(shift || die "Specificare il nome del file");
}

sub stampa_info{
    %vendorNumDisp;
    %vendorDescr;
    $nome_file = shift;
    open($file,">",$nome_file) or die "Impossibile aprire il file in scrittura\n";
    
    while(<$file>){
        if(/description:(.*)/){
        }
        elsif(/product:(.*)/ || /vendor:(.*)/){ #viene sempre prima product di vendor, quindi se entro 2 volte viene sempre dopo il vendor
            $vendor = $1;
        }
        elsif(/\*.*/){ #in questo momento cambiamo prodotto, salviamo le cose del valore precedente
            $description = $1;
            if($vendor and $description){ #se vendor è undef questa chiave non viene inserita
                $vendorDescr{$vendor} = $description; 
                $vendorNumDisp{$vendor} += 1;
            }
            $vendor = undef;
            $description = undef;
        }
    }
    if($vendor){ #Serve altrimenti non salva l'ultimo prodotto
        $vendorDescr{$vendor} .= "\n$description"; 
        $vendorNumDisp{$vendor} += 1;
    }
}

sub salva_su_file{
    $nome_file = shift;
    qx(lshw > $nome_file 2> /dev/null); #re indirizziamo stdout sul file che ci è stato chiesto, mentre l'error lo buttiamo (perché lshw stampa alcuni warning e mi danno fastidio)
}