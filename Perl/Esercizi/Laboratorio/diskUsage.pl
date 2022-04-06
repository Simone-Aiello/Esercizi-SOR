#!/usr/bin/perl
$argv_size = scalar @ARGV;
$argv_1 = shift @ARGV;
$argv_2 = shift @ARGV;
$pt = ".";
die "Numero di parametri non valido" if $argv_size == 0 || $argv_size >= 3;
die "Inserire i formati" unless $argv_1 =~ /--format=.+/ || $argv_2 =~ /--format=.+/;
#le estensioni sono nel primo argv, il secondo è il path
@accepted_extensions;
if($argv_1 =~ /--format=.+/){
    $extensions = (split("--format=",$argv_1))[-1];
    @accepted_extensions = split(",",$extensions);
    print "ESTENSIONI: @accepted_extensions\n";
    $pt = $argv_2;
    print "PATH: $pt\n";
}
else{
    $pt = $argv_1;
    print "PATH: $pt\n";
}
@command = qx(du -ka $pt);
print "@command";
%out;
$somma = 0;
for (@accepted_extensions){
    $out{$_} = 0;
}
for(@command){
    @splitted = split(" ",$_);
    $size = $splitted[0];
    $path = $splitted[1];
    $file = (split("/",$path))[-1];
    $ext = (split('\.',$file))[-1];
    chomp $ext;
    for $e (@accepted_extensions){
        if($e eq $ext){
            $out{$ext} = $out{$ext} +  $size;
        }
    }
}
for (sort keys %out){
    print "Keys $_ --> Value: $out{$_}Kb\n";
    $somma += $out{$_};
}

open($fh,">","du.out");
print $fh "$pt: $somma";
close $fh;