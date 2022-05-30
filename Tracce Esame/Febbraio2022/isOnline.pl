#!/usr/bin/perl
$file = shift or die "Nessun file inserito\n";

open($fh,"<",$file);
for (<$fh>){
    chomp;
    if(/(([A-F0-9a-f]{2}:){5}[A-F0-9a-f]{2})#(.*)/){
        print "$1 ------> $3\n";
        $mac_name{$1} = $3;
    }
}
close $fh;

#@out = qx(arp -an) sulla WSL ho solo una riga quindi leggo un out da testo
open($fh,"<","arpout.txt");
for (<$fh>){
    chomp;
    if(/.*\((.*)\).*(([A-F0-9a-f]{2}:){5}[A-F0-9a-f]{2}).*/){
        print "$1 -----> $2\n";
        $ip_mac{$1} = $2;
    }
}
close $fh;
@online_ip = ();
@offline_ip = ();

for (keys %ip_mac){
    $onl = 1;
    @ping_out = qx(ping -c1 $_);
    for $line (@ping_out){
        if($line =~ /.*100% packet loss.*/){
            $onl = 0;
        }
    }
    if($onl){
        push @online_ip, $_;
    }
    else{
        push @offline_ip, $_;
    }
}
@online_names = ();
@offiline_names = ();
for (@online_ip){
    push @online_names, $mac_name{$ip_mac{$_}} 
}
for (sort @online_names){
    print "$_\n";
}
for (@offline_ip){
    push @offline_names, $mac_name{$ip_mac{$_}} 
}
for (sort {$b cmp $a} @offline_names){
    print "$_\n";
}
