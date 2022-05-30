#!/usr/bin/perl
@lines = <STDIN>;
for (@lines){
    chomp;
    $name = $_;
    $to_search = $_;
    $to_search =~ s/\s+/\+/;
    $url = "https://scholar.google.com/scholar?hl=en&q=$to_search";

    @out = qx(wget -O output -U 'Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' '$url');

    open($fh,"<","output");
    $count = 0;
    while (<$fh>){
        chomp;
        if (/.*About\s+(.*?)\s+results.*/){
            $count = $1;
        }
    }
    $count =~ s/,//g;
    $hash{$name} = $count;
    close $fh;
}

for (sort {$hash{$a} cmp $hash{$b}} keys %hash){
    print "$_ -----> $hash{$_}\n";
}
