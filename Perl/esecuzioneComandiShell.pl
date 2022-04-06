#!/usr/bin/perl
@output = qx(ls -l);
$i = 0;
for(@output){
    print "Linea $i: $_\n";
    $i++;
}

#altro modo: @output = `ls -l`;
#altro modo ancora: system("ls -l") che stampa direttamente su terminale anche, spesso usato con clear così pulisce in automatico, qx ad esempio non lo fa, perché salva l'output, per avere effetto con qx dovrei anche stampare l'output (ovvero tanti enter fino a quando la riga di output non sale su)

