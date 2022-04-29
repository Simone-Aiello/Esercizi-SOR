#!/usr/bin/perl

$soglia_mem = 100;
$soglia_cpu = 100;
for $i (@ARGV){
    if($i =~ /MEM=((\d+\.\d+)|([1-9]\d+))/){
        $soglia_mem = $2 ? $2 : $3;
    }
    elsif($i =~ /CPU=((\d+\.\d+)|([1-9]\d+))/){
        $soglia_cpu = $2 ? $2 : $3;
    }
}
print "SOGLIA CPU $soglia_cpu\n";
print "SOGLIA MEM $soglia_mem\n";
#./squid.pl MEM=x CPU=y
#USR          PID CPU  MEM   VSZ    RSS TTY      STAT START   TIME COMMAND
#root         1   0.0  0.0   8948   380 ?        Ssl  11:57   0:00 /init
while(1){
    print "Bravo six going dark\n";
    #Spawn di un processo fake che consuma memoria e cpu giusto per
    system("./processoFake.py &"); #Perché qx non funziona? 
    sleep(3);
    @output = qx(ps -aux);
    #print "@output\n";
    %cpu_load = {};
    %mem_load = {};
    for (@output){
        chomp;
        if($_ =~ /.+?(\d+)\s+(\d+(\.\d+)*)\s+(\d+\.\d+).+\d+:\d+\s+(.*)/){
            #print "Nome: $5 CPU: $2 MEM:$4 PID:$1\n";
            $cpu_load{$5} += $2;
            $mem_load{$5} += $4;
            if($cpu_load{$5} > $soglia_cpu or $mem_load{$5} > $soglia_mem){
                qx(pkill -f "$5");
                print "Target $5 spotted...\nTarget $5 neutralized\n";
            }
        }
    }
}