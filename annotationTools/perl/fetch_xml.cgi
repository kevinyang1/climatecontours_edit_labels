#!/usr/bin/perl

use lib '.';
use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );

require 'globalvariables.pl';
use vars qw($LM_HOME);

my $im_file;

# hardcode the location of this
my $fname = $LM_HOME . "annotationCache/DirLists/xmls.txt";

if(!open(FP,$fname)) {
  print "Status: 404\n\n";
return;
}


# store in memory
my @LINES = <FP>;
close(FP);

# get the number of lines
open(NUMLINES,"wc -l $fname |");
my $numlines = <NUMLINES>;
($numlines,my $bar) = split(" DirLists",$numlines);
close(NUMLINES);

# open/create a new file to store the modified dirList
open FH, '>', "$fname.temp";

# get a random xml
my $line = int(rand($numlines));
my $counter = 0;

foreach my $LINE ( @LINES ) {
  if ($counter == $line) {
    $im_file = $LINE;
    $im_file =~ tr/"\n"//d; # remove trailing newline
  } else {
    print FH $LINE;
  }
  $counter += 1;
}

unlink $fname;
rename "$fname.temp", $fname;
# Send back data:
print "Content-type: text/xml\n\n" ;
print "<out><file>$im_file</file></out>";
