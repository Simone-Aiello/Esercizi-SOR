#!/usr/bin/perl
$folder = shift;
@out = qx(ls $folder);
$maxfile = "";
$minfile = "";
$maxdim = 0;
$mindim = 0;
$minset = 0;
$current_file = "";
for (@out){
    chomp;
    @statOut = qx(stat $_);
    for (@statOut){
        chomp;
        if(/.*Size:\s+(\d+)\s+Blocks:\s+(\d+)\s+IO\sBlock:\s\d+\s+(.*)/){
            print "Size $1 Blocks: $2 Tipo File: $3\n";
            $somma = $1 + $2;
            if($somma > $maxdim){
                $maxdim = $somma;
                $maxfile = $current_file;
            }
            if($somma < $mindim or !$minset){
                $mindim = $somma;
                $minfile = $current_file;
                $minset = 1;
            }
            print "$current_file -> $somma\n";
        }
        if(/.*File:\s+(.*)/){
            print"FILE: $1\n";
            $current_file = $1;
            print "$current_file\n";
        }
    }
}
print "File massimo $maxfile --> $maxdim\n";
print "File minimo $minfile --> $mindim\n";