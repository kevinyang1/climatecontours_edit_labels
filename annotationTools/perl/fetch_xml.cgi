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

open(NUMLINES,"wc -l $fname |");
my $numlines = <NUMLINES>;
($numlines,my $bar) = split(" DirLists",$numlines);
close(NUMLINES);

# get a random xml
my $line = int(rand($numlines))+1;

for(my $i=1; $i < $line; $i++) {
my $garbage = readline(FP);
}

my $fileinfo = readline(FP);
# TODO: change the way that this processes here
#($im_dir,$im_file) = split(",",$fileinfo);
$im_file = $fileinfo;
$im_file =~ tr/"\n"//d; # remove trailing newline

close(FP);

# Send back data:
print "Content-type: text/xml\n\n" ;
print "<out><file>$im_file</file></out>";
