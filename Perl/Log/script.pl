#!/usr/bin/perl
#-f cosa fa, si mette in wait, appena arriva una riga nuova la mostra, quindi il programma gira all'infinito agganciandosi a questo comando
open(LOG,"tail -f mail.ripulito.log |");

#%dabandire ip => x

#%banditi ip => 1

$sogliaspam = 100;
$tempodisqualifica = 10;
while(<LOG>){
    #Il problema di questo script è che una persona viene ripristinata dal ban solo se arriva una mail spam da parte sua dopo un tot che non ne sono arrivate, il che è meh
    if(/SPAM.*?\[(.*?)\].*Hits:\s(\d+\.\d+)/){
        ($ip,$spamscore) = ($1,$2);
        $dabandire{$1} += $spamscore; #perl crea al volo un dizionario, crea la chiave, la mette a 0 e ci somma il resto
        if($dabandire{$ip} > $sogliaspam){
            print "Madonna lo ammazzo\n";
            #comandare il vero firewall -> se ti arriva in input qualcosa dalla sorgente $1 allora fai DROP di quel pacchetto
            qx(iptables -I INPUT -s $1 -j DROP);
            $banditi{$ip} = time();
            delete $dabandire{$ip};
        }
        for $ip (keys %banditi){
            if (time() - $banditi{$ip} > $tempodisqualifica){
                #elimina la regona inserita prima
                qx(iptables -D INPUT -s $ip -j DROP);
                delete $banditi{$ip};
            }
        }
    }
}