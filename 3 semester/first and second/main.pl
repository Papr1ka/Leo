use strict;
use warnings;

my %operations = (
	'*' => 3,
	'/' => 3,
	'+' => 2,
	'-' => 2,
	'(' => 1,
	')' => 1,
);
my @operationsList = keys %operations;

my $str = "( 6 + 9 - 5 ) / ( 8 + 1 * 2 ) + 7";
my $last = "";
my $result = "";
my @buffer = ();
my $isFirst = 1;

my @tokens = split(" ", $str);
# my $first = shift @tokens;


for my $token (@tokens)
{
	unless ($token ~~ @operationsList)
	{
		if($isFirst == 1)
		{
			$result .= $token;
			$isFirst = 0;
		}
		else
		{
			$result .= " $token";
		}
	}
	else
	{
		if ($token eq "(")
		{
			push @buffer, $token;
			next;
		}
		elsif ($token eq ")")
		{
			while ($buffer[$#buffer] ne "(")
			{
				$result .= " ".$buffer[$#buffer];
				pop @buffer;
			}
			pop @buffer;
			next;
		}
		while ($#buffer > -1 && ($operations{$token} <= $operations{$buffer[$#buffer]}))
		{
			$result .= " $buffer[$#buffer]";
			pop @buffer;
		}
		push @buffer, $token;
	}
}

for (my $iter = $#buffer; $iter >= 0; $iter--)
{
	$result .= " ".$buffer[$iter];
}
print $result."\n";