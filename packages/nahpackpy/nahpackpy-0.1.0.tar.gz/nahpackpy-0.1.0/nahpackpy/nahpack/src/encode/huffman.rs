// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


pub fn compress_literal(writer: &mut Vec<u8>, literal: &[u8]) -> usize {
    let start = writer.len();
    let mut pos = start;
    let mut free = 8;
    let mut bits: u8;
    let mut code: u32;

    for (idx, &byte) in literal.iter().enumerate() {
        let (sbits, scode) = ENCODE_BITS[byte as usize];
        code = scode;
        bits = sbits;

        if bits <= free {
            if free == 8 || free == 0 {
                writer.push((code << 8 - bits) as u8);
                free = 8 - bits;
                pos += 1;
            } else {
                writer[pos - 1] |= (code << (free - bits)) as u8;
                free -= bits;
            }
        } else {
            if idx != 0 {
                writer[pos - 1] |= (code >> (bits - free)) as u8;
                bits -= free;
            }
            let offset = bits & 7;
            if offset > 0 {
                code <<= 8 - offset;
            }

            match bits {
                1...8 => {
                    writer.push(code as u8);
                    free = 8 - bits;
                    pos += 1;
                },
                9...16 => {
                    writer.push((code >> 8) as u8);
                    writer.push(code as u8);
                    free = 16 - bits;
                    pos += 2;
                },
                17...24 => {
                    writer.push((code >> 16) as u8);
                    writer.push((code >> 8) as u8);
                    writer.push(code as u8);
                    free = 24 - bits;
                    pos += 3;
                },
                25...32 => {
                    writer.push((code >> 24) as u8);
                    writer.push((code >> 16) as u8);
                    writer.push((code >> 8) as u8);
                    writer.push(code as u8);
                    free = 32 - bits;
                    pos += 4;
                },
                0 => { },
                _ => {
                    unreachable!();
                }
            }
        }
    }
    if free & 7 > 0 {
        writer[pos - 1] |= 255 >> 8 - free;  // EOS
    }
    pos - start
}


const ENCODE_BITS: [(u8, u32); 256] = [
    (13, 8184),
    (23, 8388568),
    (28, 268435426),
    (28, 268435427),
    (28, 268435428),
    (28, 268435429),
    (28, 268435430),
    (28, 268435431),
    (28, 268435432),
    (24, 16777194),
    (30, 1073741820),
    (28, 268435433),
    (28, 268435434),
    (30, 1073741821),
    (28, 268435435),
    (28, 268435436),
    (28, 268435437),
    (28, 268435438),
    (28, 268435439),
    (28, 268435440),
    (28, 268435441),
    (28, 268435442),
    (30, 1073741822),
    (28, 268435443),
    (28, 268435444),
    (28, 268435445),
    (28, 268435446),
    (28, 268435447),
    (28, 268435448),
    (28, 268435449),
    (28, 268435450),
    (28, 268435451),
    (6, 20),
    (10, 1016),
    (10, 1017),
    (12, 4090),
    (13, 8185),
    (6, 21),
    (8, 248),
    (11, 2042),
    (10, 1018),
    (10, 1019),
    (8, 249),
    (11, 2043),
    (8, 250),
    (6, 22),
    (6, 23),
    (6, 24),
    (5, 0),
    (5, 1),
    (5, 2),
    (6, 25),
    (6, 26),
    (6, 27),
    (6, 28),
    (6, 29),
    (6, 30),
    (6, 31),
    (7, 92),
    (8, 251),
    (15, 32764),
    (6, 32),
    (12, 4091),
    (10, 1020),
    (13, 8186),
    (6, 33),
    (7, 93),
    (7, 94),
    (7, 95),
    (7, 96),
    (7, 97),
    (7, 98),
    (7, 99),
    (7, 100),
    (7, 101),
    (7, 102),
    (7, 103),
    (7, 104),
    (7, 105),
    (7, 106),
    (7, 107),
    (7, 108),
    (7, 109),
    (7, 110),
    (7, 111),
    (7, 112),
    (7, 113),
    (7, 114),
    (8, 252),
    (7, 115),
    (8, 253),
    (13, 8187),
    (19, 524272),
    (13, 8188),
    (14, 16380),
    (6, 34),
    (15, 32765),
    (5, 3),
    (6, 35),
    (5, 4),
    (6, 36),
    (5, 5),
    (6, 37),
    (6, 38),
    (6, 39),
    (5, 6),
    (7, 116),
    (7, 117),
    (6, 40),
    (6, 41),
    (6, 42),
    (5, 7),
    (6, 43),
    (7, 118),
    (6, 44),
    (5, 8),
    (5, 9),
    (6, 45),
    (7, 119),
    (7, 120),
    (7, 121),
    (7, 122),
    (7, 123),
    (15, 32766),
    (11, 2044),
    (14, 16381),
    (13, 8189),
    (28, 268435452),
    (20, 1048550),
    (22, 4194258),
    (20, 1048551),
    (20, 1048552),
    (22, 4194259),
    (22, 4194260),
    (22, 4194261),
    (23, 8388569),
    (22, 4194262),
    (23, 8388570),
    (23, 8388571),
    (23, 8388572),
    (23, 8388573),
    (23, 8388574),
    (24, 16777195),
    (23, 8388575),
    (24, 16777196),
    (24, 16777197),
    (22, 4194263),
    (23, 8388576),
    (24, 16777198),
    (23, 8388577),
    (23, 8388578),
    (23, 8388579),
    (23, 8388580),
    (21, 2097116),
    (22, 4194264),
    (23, 8388581),
    (22, 4194265),
    (23, 8388582),
    (23, 8388583),
    (24, 16777199),
    (22, 4194266),
    (21, 2097117),
    (20, 1048553),
    (22, 4194267),
    (22, 4194268),
    (23, 8388584),
    (23, 8388585),
    (21, 2097118),
    (23, 8388586),
    (22, 4194269),
    (22, 4194270),
    (24, 16777200),
    (21, 2097119),
    (22, 4194271),
    (23, 8388587),
    (23, 8388588),
    (21, 2097120),
    (21, 2097121),
    (22, 4194272),
    (21, 2097122),
    (23, 8388589),
    (22, 4194273),
    (23, 8388590),
    (23, 8388591),
    (20, 1048554),
    (22, 4194274),
    (22, 4194275),
    (22, 4194276),
    (23, 8388592),
    (22, 4194277),
    (22, 4194278),
    (23, 8388593),
    (26, 67108832),
    (26, 67108833),
    (20, 1048555),
    (19, 524273),
    (22, 4194279),
    (23, 8388594),
    (22, 4194280),
    (25, 33554412),
    (26, 67108834),
    (26, 67108835),
    (26, 67108836),
    (27, 134217694),
    (27, 134217695),
    (26, 67108837),
    (24, 16777201),
    (25, 33554413),
    (19, 524274),
    (21, 2097123),
    (26, 67108838),
    (27, 134217696),
    (27, 134217697),
    (26, 67108839),
    (27, 134217698),
    (24, 16777202),
    (21, 2097124),
    (21, 2097125),
    (26, 67108840),
    (26, 67108841),
    (28, 268435453),
    (27, 134217699),
    (27, 134217700),
    (27, 134217701),
    (20, 1048556),
    (24, 16777203),
    (20, 1048557),
    (21, 2097126),
    (22, 4194281),
    (21, 2097127),
    (21, 2097128),
    (23, 8388595),
    (22, 4194282),
    (22, 4194283),
    (25, 33554414),
    (25, 33554415),
    (24, 16777204),
    (24, 16777205),
    (26, 67108842),
    (23, 8388596),
    (26, 67108843),
    (27, 134217702),
    (26, 67108844),
    (26, 67108845),
    (27, 134217703),
    (27, 134217704),
    (27, 134217705),
    (27, 134217706),
    (27, 134217707),
    (28, 268435454),
    (27, 134217708),
    (27, 134217709),
    (27, 134217710),
    (27, 134217711),
    (27, 134217712),
    (26, 67108846),
];


#[cfg(test)]
mod test {
    extern crate test;
    use self::test::Bencher;
    use super::compress_literal;
    use decode::decompress_literal;


    #[test]
    fn test_compress_literal_no_cache() {
        let mut buf = Vec::with_capacity(128);
        let _ = compress_literal(&mut buf, b"no-cache");

        let mut decoded = Vec::new();
        let _ = decompress_literal(&buf[..], &mut decoded).unwrap();
        assert_eq!(b"no-cache", &decoded[..]);
        assert_eq!(
            b"\xa8\xeb\x10d\x9c\xbf",
            &buf[..]
        );
    }


    #[test]
    fn test_compress_literal_custom_value() {
        let mut buf = Vec::with_capacity(128);
        let _ = compress_literal(&mut buf, b"custom-value");
        assert_eq!(
            b"%\xa8I\xe9[\xb8\xe8\xb4\xbf",
            &buf[..]
        );
    }


    #[test]
    fn test_compress_literal_cookie() {
        let literal = b"PRpc=|HwqgHD3W:1|HrYwHDG0:1|HrYvHDG1:2|#;domain=ads.pointroll.com; path=/; expires=Mon, 03-Nov-2014 13:39:17 GMT;";
        let mut buf = Vec::with_capacity(128);
        let _ = compress_literal(&mut buf, literal);

        let mut decoded = Vec::new();
        let _ = decompress_literal(&buf[..], &mut decoded).unwrap();
        assert_eq!(
            String::from_utf8(literal.to_vec()).unwrap(),
            String::from_utf8(decoded.clone()).unwrap()
        );
    }


    #[test]
    fn test_compress_literal_quoted() {
        let literal = b"\\\"41YZLkI+UsL_SL135_#1\\\"";
        let mut buf = Vec::with_capacity(128);
        let _ = compress_literal(&mut buf, literal);

        let mut decoded = Vec::new();
        let _ = decompress_literal(&buf[..], &mut decoded).unwrap();
        assert_eq!(
            String::from_utf8(literal.to_vec()).unwrap(),
            String::from_utf8(decoded.clone()).unwrap()
        );
    }


    #[test]
    fn test_compress_literal_four_byte() {
        let literal = vec![9, 10, 0, 127];
        let mut buf = Vec::with_capacity(128);
        let _ = compress_literal(&mut buf, &literal[..]);

        let mut decoded = Vec::new();
        let _ = decompress_literal(&buf[..], &mut decoded).unwrap();
        assert_eq!(
            String::from_utf8(literal).unwrap(),
            String::from_utf8(decoded.clone()).unwrap()
        );
    }


    #[test]
    fn test_compress_literal_datetime() {
        let mut buf = Vec::with_capacity(128);
        let _ = compress_literal(&mut buf, b"Mon, 21 Oct 2013 20:13:21 GMT");
        assert_eq!(
            b"\xd0z\xbe\x94\x10T\xd4D\xa8 \x05\x95\x04\x0b\x81f\xe0\x82\xa6-\x1b\xff",
            &buf[..]
        );
    }


    #[bench]
    fn bench_compress_literal_no_cache(b: &mut Bencher) {
        let mut buf = Vec::with_capacity(16384);
        b.iter(
            || compress_literal(&mut buf, b"no-cache")
        )
    }


    #[bench]
    fn bench_compress_literal_datetime(b: &mut Bencher) {
        let mut buf = Vec::with_capacity(16384);
        b.iter(
            || compress_literal(&mut buf, b"Mon, 21 Oct 2013 20:13:21 GMT")
        )
    }

}
