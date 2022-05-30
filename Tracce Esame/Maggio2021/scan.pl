#!/usr/bin/perl
sub tagetIp{
    $ip_target = shift;
    print "$ip_target\n";
    $open_ports = 0;
    @log = @{ (shift) };
    for (@log){
        chomp;
        if(/^.*open\sport\s(\d+).*$ip_target$/){
            print "$1\n";
            $open_ports += 1;
        }
    }
    print "---------------------------\n Total: $open_ports\n";
}
sub listroutine{
    @log = @{ (shift) };
    for (@log){
        chomp;
        if(/^.*open\sport\s(\d+).*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/){
           $hash{$2} = $hash{$2} + 1; 
        }
    }
    for (sort {$hash{$b} <=> $hash{$a}} keys %hash){
        print "$_ -----> $hash{$_}\n";
    }
}
die "Numero di argomenti non validi" unless (scalar @ARGV == 2);
$nome_file = shift or die "Nessun file inserito";
$option = shift;

die "Opzione $option non valida" unless $option =~ /(--ip)=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(--list)/;
open($fh,"<",$nome_file) or die "Impossibile aprire il file";
@lines = <$fh>;
close $fh;
if($1 eq "--ip"){
    tagetIp($2,\@lines);
}
elsif($3 eq "--list"){
    listroutine(\@lines);
}