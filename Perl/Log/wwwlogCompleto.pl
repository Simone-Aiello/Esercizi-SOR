#!/usr/bin/perl

chdir "/root/script/tests";
$logtail = "/usr/sbin/logtail";
$logfile = '/var/log/apache2/ssl_access.log';
$logfile2 = '/var/log/apache2/access.log';
$logfile3 = '/var/log/apache2/ssl_access.log.1';
$logfile4 = '/var/log/apache2/access.log.1';
$oldlogfile = '/root/script/tests/ssl_access_log.inf';
$filter = $ARGV[0] || die "You must specify a filter string";
$email = $ARGV[1] || die "You must specify a valid mail address"; 
$wholelog = "/root/script/tests/$filter-wholelogtail.txt";
$offsetfile = "/root/script/tests/$filter-diff.off";
$offsetfile2 = "/root/script/tests/$filter-diff2.off";
open(STDERR,">>/root/script/tests/$filter-errors.txt");
qx{$logtail -f$logfile2 -o$offsetfile2 | grep \"$filter\" > $wholelog};
qx{$logtail -f$logfile -o$offsetfile | grep \"$filter\" >> $wholelog};

#open(COMMAND,"cat $logfile2 $logfile | grep $filter|");
open(COMMAND,"cat $wholelog|");

foreach ( <COMMAND> ) {
        
        #print "Main loop\n";
        ( $ip, $date, $url, $referrer ) = /(\d+?\.\d+?\.\d+?\.\d+).*?\[(.*?)\].*?GET (.*?) .*?".*?"(.*?)"/;    
        #print "$ip, $date, $url, $referrer\n";  
        $name = '-';
        $name = qx"host $ip" unless !$ip;
        ($name) = $name =~ /domain name pointer (.*)\./;
        if (! ($name  =~ /msnbot/ || $name  =~ /googlebot/) ) {        
        # Visitor from $ip came from URL $referrer
        #
        $ips{$ip} = $name;
        #
        # Visitor from $ip came in date $date
        #
        $date{$ip} = $date; 
        #
        # Resource $url has been visited once more
        #
	$urls{$url}++;
        if ($referrer =~ /www\.google.*(\?|&)q=(.*?)(&|$)/)
        {
            $query = $2;
            $query =~ s/(%20|\+)/ /g;
	    $refs{$url} = "GOOGLE: $query\n";
            $gugols{$query}++;
        }
	else {
		$refs{$url} .= "\t$referrer\n" unless (($referrer eq '-') || !$referrer || $refs{$url} =~ /\t$referrer\n/s );
	}
        #
        # If $ip accessed an .mp3, assume it's visiting the blog 

        #
        $blog{$ip}++ if /\w+\.mp3/;
}

}

@tutti = sort keys %ips;
@urls = sort { $urls{$b} <=> $urls{$a} } keys %urls; 
@gugols = sort { $gugols{$b} <=> $gugols{$a} } keys %gugols; 
$command = 'mail -s [WWW\ Daily\ update] '.$email;
#$command = 'tee out.txt';
open (INFO, "| $command");
#
# Lists visited resources, sorted per number of accesses
#
print INFO "GOOGLE VISITS:\n";
foreach (@gugols)
{
	print INFO "$gugols{$_}\t$_\n";
}
print INFO "------\n";
print INFO "RESOURCES VISITED\n";
foreach (@urls)
{
	print INFO "$urls{$_}\t$_\n";
	print INFO "Referrer URLs:\n" if $refs{$_};
	print INFO "$refs{$_}";
	print INFO "----\n";
}
print INFO "------\n";
print INFO "DETAILED VISITORS LIST (excludes indexing bots)\n";
foreach $ip (@tutti) {
        ($name) = /.* (.*?)$/;
        print INFO $ip."\t\t\t".$name."\n  DATE:\t\t".$date{$ip}."\n  HOSTNAME:\t".$ips{$ip}."\n----\n";
}

