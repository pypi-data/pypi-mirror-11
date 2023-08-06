// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


const INT_BOUNDARY: u32 = 128;


#[inline]
pub fn encode_integer(writer: &mut Vec<u8>, data: u32, n: u32, mask: u8) -> usize {
    let mut bytes = 0;
    let max_num: u32 = (1 << n) - 1;
    if data < max_num {
        writer.push(data as u8 | mask);
        bytes += 1;
    } else {
        writer.push(max_num as u8 | mask);
        bytes += 1;
        let mut i = data - max_num;
        while i >= INT_BOUNDARY {
            writer.push((i % INT_BOUNDARY + INT_BOUNDARY) as u8);
            i = i / INT_BOUNDARY;
            bytes += 1;
        }
        writer.push(i as u8);
        bytes += 1;
    }
    bytes
}


#[cfg(test)]
mod test {
    extern crate test;
    use self::test::Bencher;
    use super::encode_integer;


    #[test]
    fn test_encode_integer_idx_2() {
        let mut res = Vec::new();
        encode_integer(&mut res, 2, 7, 0b10000000);
        assert_eq!(&res[..], [130]);
    }

    #[test]
    fn test_encode_integer_idx_8() {
        let mut res = Vec::new();
        encode_integer(&mut res, 8, 7, 0b10000000);
        assert_eq!(&res[..], [136]);
    }

    #[test]
    fn test_encode_integer_1337() {
        let mut res = Vec::new();
        encode_integer(&mut res, 1337, 5, 0);
        assert_eq!(&res[..], [31, 154, 10]);
    }

    #[test]
    fn test_encode_integer_6500() {
        let mut res = Vec::new();
        encode_integer(&mut res, 65000, 5, 0);
        assert_eq!(&res[..], [31, 201, 251, 3]);
    }

    #[test]
    fn test_encode_integer_4096() {
        let mut res = Vec::with_capacity(4096);
        encode_integer(&mut res, 4096, 5, 0b00000100);
        assert_eq!(&res[..], [31, 225, 31]);
    }

    #[bench]
    fn bench_encode_integer_early(b: &mut Bencher) {
        let mut res = Vec::with_capacity(4096);
        b.iter(
            || encode_integer(&mut res, 10, 7, 0)
        )
    }

    #[bench]
    fn bench_encode_integer_loop(b: &mut Bencher) {
        let mut res = Vec::with_capacity(4096);
        b.iter(
            || encode_integer(&mut res, 1337, 7, 0)
        )
    }

}
