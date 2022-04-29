#! /usr/bin/perl

 $ARGV[0] ||  die "ARGV[0] non presente\n";
 $ARGV[1] ||  die "ARGV[1] non presente\n";

$email = $ARGV[1];
open(LOG,$ARGV[0]);


while ($linea = <LOG>)

{
    if ($linea =~ /(\d+?\.\d+?\.\d+?\.\d+?).*?\[(.*?)\].*?GET (.*?) HTTP/)
    {
       ($ip, $data, $url) = ($1,$2,$3);
       $visitedi{$ip}++;
       $datadi{$ip} = $data;
       $visitedirisorsa{$url}++;
       #$nomehost = qx{host $ip};
       #$nomehost =~ /.* (.*)/;
       $nomedi{$ip} = $ip;
    }
}
open(MESSAGGIO,"| mail $email -s [rapporto]");
foreach $visitatore (sort { $visitedi{$b} <=> $visitedi{$a}; } keys %visitedi)
{
	print MESSAGGIO "$visitedi{$visitatore} = $visitatore = $nomedi{$visitatore}\n";
}
close(MESSAGGIO);

