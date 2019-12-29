# Picprime: Render an ASCII image as a prime number
Bart Massey

This code fills in digits in an ASCII image template such
that the digits of the resulting ASCII image form a prime
number. The code was inspired by this
[Reddit post](https://www.reddit.com/r/interestingasfuck/comments/efhy5m/i_found_this_really_great_the_correct_alignment/).

## Usage

This program comes in two versions: a Python program and a
Rust program. To use either, run it with the ASCII template
image file either as the first argument or on standard
input. For example:

    python3 picprime.py template.txt

or

    cargo run --release <template.txt

The runtime is highly variable: I have not observed a
runtime longer than 30 seconds with the provided sample
template on my box, and have occasionally gotten an answer
in a couple of seconds.

## Templates

The template file can contain arbitrary UTF-8 text.  In the
template file:

* Digit characters 0..9 are treated as literal digits of the
  prime.

* Dot characters `.` are treated as "free" digits of the
  prime and will be replaced with random digits such that
  the resulting number is prime.

* Other characters are passed through unchanged.

An example `template.txt` is provided.

Note that if the template has too few free digits the
program will have a hard time finding a prime, if one even
exists.  If the last digit in the template is fixed at 0, 2
or 5 the template is guaranteed only produce composites. No
checking is done: in this case the program will run forever.

## How It Works

The basic idea here is to randomly fill in the `.` cells in
the template with digits and use a probabilistic primality
test to see if the resulting overall number is prime: repeat
until a prime is discovered, then render the result.

## Python *vs* Rust

The Python version was constructed first. The Rust version
targets better performance and better reliability. It is
extremely difficult to compare the performance of the two
versions, due to the randomness involved.

Some preliminary benchmarking suggests that the Rust version
completes one iteration in ½ to ¼ the time, but that is
questionable. The Python version could be sped up a bit by
cutting down the number of bases tested by the crude bespoke
Miller-Rabin test from 40 to 20 without much chance of
false-positives; it could be sped up a bit more by making
the Miller-Rabin test iterative instead of recursive.

The Rust version uses a primality test from the
`glass_pumpkin` crate — it is likely much more reliable than
my Miller-Rabin implementation. I did not find a Python
primality test package in a quick Google search: I'm sure I
must have missed one.

My overall conclusion is that it was mostly a waste of time
to write a Rust version of this, at least from a practical
perspective. Hopefully it at least makes a nice Rust demo.

## Acknowledgments

Thanks to the anonymous person who posted this image
originally, to `/u/An_average_one` for reposting on Reddit,
and to Michael Lodder for the `glass_pumpkin` crate.

## License

This program is licensed under the "MIT License". Please see
the file `LICENSE` in this distribution for license terms.
