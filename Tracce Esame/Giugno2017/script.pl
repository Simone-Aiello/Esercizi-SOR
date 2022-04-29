#!/usr/bin/perl
$option = shift or die "Inserire un opzione";
$file = shift or die "Inserire un file";
@out = qx(file $file); 
die "Il file inserito non esiste" if $out[0] =~ /.*No\ssuch\sfile\sor\sdirectory.*/;
if($option =~ /^-w$/){
    @wcout = qx(wc -m $file);
    $wcout[0] =~ /(\d+)\s+.*/;
    print "Numero di parole: $1\n";
}
elsif($option =~ /^-d$/){
    $file2 = shift or die "File 2 non inserito\n";
    @outfile2 = qx(file $file2); 
    die "Il file 2 inserito non esiste" if $outfile2[0] =~ /.*No\ssuch\sfile\sor\sdirectory.*/;
    system("diff $file $file2");
}
elsif($option =~ /^-s$/ or die "Opzione inserita non valida"){
    $file2 = shift or die "File 2 non inserito\n";
    qx(cat $file | grep -P ".+" | sort > $file2); #grep è solo per togliere le righe vuote, alla fine è inutile, l'ho messo giusto per
}