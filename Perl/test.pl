#!/usr/bin/perl
open($f1,"<","ciao.txt");
open($f2,"<","ciao2.txt");

while($line = <$f1> or $line2 = <$f2>){
    chomp $line;
    chomp $line2;
    print "Linea 1: $line\n";
    print "Linea 2: $line2\n";
}
close $f1;
close $f2;