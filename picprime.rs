// Bart Massey

// Render an ASCII image from a template, constructed such
// that the digits in the resulting image form a large prime
// number.

// This code is licensed under the "MIT license".  See
// the file `LICENSE` in this distribution for license terms.

use glass_pumpkin::prime;
use num_bigint::BigUint;
use rand::prelude::*;
use std::fs::File;
use std::io::Read;

fn main() {
    let mut template_file: Box<dyn Read> = match std::env::args().nth(1)
    {
        None => Box::new(std::io::stdin()),
        Some(f) => {
            Box::new(File::open(f).expect("could not open template"))
        }
    };
    let mut template = String::new();
    template_file
        .read_to_string(&mut template)
        .expect("could not read template");
    let mut rng = thread_rng();
    loop {
        let digits: String = template
            .chars()
            .filter(|&c| c.is_digit(10) || c == '.')
            .map(|c| {
                if c == '.' {
                    char::from(b'0' + rng.gen_range(0, 10))
                } else {
                    c
                }
            })
            .collect();
        let candidate: BigUint =
            digits.parse().expect("internal error: candidate");
        if prime::strong_check(&candidate) {
            let cstring = candidate.to_string();
            let mut cchars = cstring.chars();
            let answer: String = template
                .chars()
                .map(|c| {
                    if c == '.' {
                        return cchars.next().unwrap();
                    }
                    if c.is_digit(10) {
                        assert_eq!(c, cchars.next().unwrap());
                    }
                    c
                })
                .collect();
            assert!(cchars.next().is_none());
            print!("{}", answer);
            return;
        }
    }
}
