#!/usr/bin/perl
$path = shift or die "No input file provided\n";
$write_to_file = 0;
$file_searched = ".*";
for (@ARGV){
    if(/-b/){
        $write_to_file = 1;
    }
    elsif(/-t=(.*)/) {
        $file_searched = $1;
    }
    else{
        die "Invalid argument $_\n";
    }
}

@out = qx(ls $path);
$file_corrente = "";
$file_min = "";
$file_max = "";
$size_b_min = -1;
$size_b_max = 0;
$size_folder = 0;
for $fl (@out){
    chomp;
    $absolute_path = $path . $fl;
    @stats = qx(stat $absolute_path);
    for (@stats){
        if(/.*File:\s+(.*)/){
            $file_corrente = $1;
        }
        elsif(/.*Blocks:\s+(\d+).*IO\s+Block:\s+(\d+)\s+($file_searched).*/){
            $current_size_b = $1*$2;
            $size_folder += $current_size_b;
            if($current_size_b > $size_b_max){
                $size_b_max = $current_size_b;
                $file_max = $file_corrente;
            }
            if($current_size_b < $size_b_min || $size_b_min == -1){
                $size_b_min = $current_size_b;
                $file_min = $file_corrente;
            }
            $hash{$file_corrente} = $current_size_b;
        }
    }
}
if($write_to_file){
    for (sort {$hash{$b} <=> $hash{$a} or $a cmp $b} keys %hash){
        print "$_ ----> $hash{$_}\n";
    }
}
else{
    print "Folder size = $size_folder\n";
    print "MAX File = $file_max : $size_b_max\n";
    print "MIN File = $file_min : $size_b_min\n";
}




