// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


use error::HpackDecodeError;


#[inline(always)]
pub fn decode_integer(
        data: &[u8],
        n: u32,
        len: usize,
        idx: usize
    ) -> Result<(usize, u32), HpackDecodeError> {
    let mut idx = idx;
    let mut byte = data[idx] as u32;
    idx += 1;
    let mut res = byte & (255 >> (8 - n));
    if res == (1 << n) - 1 {
        let mut m = 0;
        loop {
            if idx == len {
                return Err(HpackDecodeError::InvalidInteger)
            }
            byte = data[idx] as u32;
            idx += 1;
            if byte & 128 == 128 {
                res += byte - 128 << m;
                m += 7;
                if m == 28 {  // fifth octet
                    return Err(HpackDecodeError::ExcessiveInteger)
                }
            } else {
                res += byte << m;
                break;
            }
        }
    }
    Ok((idx, res))
}


#[cfg(test)]
mod test {
    use super::decode_integer;
    use error::{
        HpackDecodeError,
    };

    extern crate test;
    use self::test::Bencher;

    #[test]
    fn test_decode_integer_incomplete() {
        assert_eq!(
            decode_integer(&[31, 154], 5, 2, 0).err().unwrap(),
            HpackDecodeError::InvalidInteger
        );
    }

    #[test]
    fn test_decode_integer_overflow() {
        assert_eq!(
            decode_integer(
                &[255, 128, 255, 255, 255, 15], 5, 6, 0
            ).err().unwrap(),
            HpackDecodeError::ExcessiveInteger
        );
    }

    #[test]
    fn test_decode_integer_10_5() {
        let res = decode_integer(&[10], 5, 1, 0);
        assert!(res.is_ok());
        assert_eq!(res.unwrap().1, 10);
    }

    #[test]
    fn test_decode_integer_10_7() {
        let res = decode_integer(&[10], 7, 1, 0);
        assert!(res.is_ok());
        assert_eq!(res.unwrap().1, 10);
    }

    #[test]
    fn test_decode_integer_1337_5() {
        assert_eq!(
            decode_integer(&[31, 154, 10], 5, 3, 0).unwrap().1,
            1337
        );
    }

    #[test]
    fn test_decode_integer_65000_5() {
        assert_eq!(
            decode_integer(
                &[31, 201, 251, 3], 5, 4, 0
            ).unwrap().1,
            65000
        );
    }

    #[bench]
    fn bench_decode_integer_early(b: &mut Bencher) {
        b.iter(
            || decode_integer(&[10], 5, 1, 0).unwrap().1
        )
    }


    #[bench]
    fn bench_decode_integer_loop(b: &mut Bencher) {
        b.iter(
            ||
                decode_integer(
                    &[31, 154, 10], 5, 3, 0
                ).unwrap()
        )
    }

    #[bench]
    fn bench_decode_integer_expensive(b: &mut Bencher) {
        b.iter(
            ||
                decode_integer(
                    &[31, 201, 251, 3], 5, 4, 0
                ).unwrap()
        )
    }
}
