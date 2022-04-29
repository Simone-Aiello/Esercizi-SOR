
#! /usr/bin/perl

#
# Per fare qualche prova di esempio rimpiazzare la seguente con
# open(LOG,"pathalmiofilediesempiopreferito");
#
open(LOG,"tail -f /var/log/mail.log |");

$sogliaspam = 5;
$tempodisqualifica = 10;

while(<LOG>)
{
    if (/SPAM.*?\[(.*?)\]/)
    {
	$dabandire{$1}++;
        if ($dabandire{$1} > $sogliaspam)
        {
           qx{iptables -I INPUT -s $1 -j DROP};
           $banditi{$ip} = time();
           delete $dabandire{$ip};
        }
        foreach $ip (keys %banditi)
        {
	      if (time() - $banditi{$ip} > $tempodisqualifica)
	      {
                 qx{iptables -D INPUT -s $ip -j DROP};
		 delete $banditi{$ip};
	      }	
        }
    }
}




