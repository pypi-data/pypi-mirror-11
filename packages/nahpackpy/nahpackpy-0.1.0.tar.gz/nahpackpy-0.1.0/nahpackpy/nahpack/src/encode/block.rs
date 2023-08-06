// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


use context::{
    HpackContext,
    HpackEncodable,
};
use encode::integer::{
    encode_integer,
};
use encode::huffman::{
    compress_literal,
};


/// Encode an [HTTP/2](https://www.rfc-editor.org/rfc/rfc7540.txt)
/// header block to transmit in one or more `HEADERS`, `PUSH_PROMISE`, or
/// `CONTINUATION` frames. The data written may be too large for one frame,
/// and the caller is responsible for splitting it.
///
///
///
/// # Examples
/// ```
/// use nahpack::{encode_block, HpackEncodable, HpackContext};
///
/// struct Header {
///     name: &'static [u8],
///     value: &'static [u8],
///     is_compressable: bool,
/// }
///
/// impl HpackEncodable for Header {
///
///     fn name(&self) -> &'static [u8] { self.name }
///     fn value(&self) -> &'static [u8] { self.value }
///     fn is_compressable(&self) -> bool { self.is_compressable.clone() }

/// }
///
/// let headers = vec![Header { name: b"name", value: b"value", is_compressable: true }, ];
///
/// let mut context = HpackContext::new();
/// let mut writer: Vec<u8> = Vec::new();
///
/// let bytes = encode_block(&mut writer, &headers, &mut context, 0);
///
/// ```
#[allow(unused_assignments)]
pub fn encode_block<T:HpackEncodable>(
        writer: &mut Vec<u8>,
        block: &[T],
        context: &mut HpackContext,
        compress_threshold: usize,
    ) -> usize {
    let mut writer = writer;  // borrow checker bug

    let mut bytes = 0; // total written

    let mut buffered = 0;
    let mut buf: Vec<u8> = Vec::with_capacity(512);

    let mut idx: u64;
    for header in block.iter() {
        idx = context.get_index(header.name(), header.value());
        match idx >> 32 {
            2 => {
                bytes += encode_integer(&mut writer, idx as u32, 7, 0b10000000);
            },
            1 => {
                context.insert(header.name(), header.value());
                bytes += encode_integer(&mut writer, idx as u32, 6, 0b01000000);
                if header.is_compressable() && header.value().len() > compress_threshold {
                    buffered = compress_literal(&mut buf, header.value());
                    bytes += buffered;
                    bytes += encode_integer(&mut writer, buffered as u32, 7, 128);
                    writer.extend(&buf[buf.len() - buffered.. buf.len()]);
                } else {
                    bytes += encode_integer(&mut writer, header.value().len() as u32, 7, 0);
                    bytes += header.value().len();
                    writer.extend(header.value());
                }
            },
            0 => {
                if header.is_compressable() && header.value().len() > compress_threshold {
                    context.insert(header.name(), header.value());

                    writer.push(0b01000000);
                    bytes += 1;

                    bytes += encode_integer(&mut writer, header.name().len() as u32, 7, 0);
                    bytes += header.name().len();
                    writer.extend(header.name());

                    buffered = compress_literal(&mut buf, header.value());
                    bytes += buffered;
                    bytes += encode_integer(&mut writer, buffered as u32, 7, 128);
                    writer.extend(&buf[buf.len() - buffered .. buf.len()]);
                } else {
                    writer.push(0b00010000);

                    bytes += 1 + encode_integer(&mut writer, header.name().len() as u32, 7, 0);
                    writer.extend(header.name());
                    bytes += header.name().len();

                    bytes += encode_integer(&mut writer, header.value().len() as u32, 7, 0);
                    writer.extend(header.value());
                }
            },
            _ => { unreachable!() }
        }
    }
    bytes
}


#[cfg(test)]
mod test {
    extern crate test;
    use self::test::Bencher;
    use context::{
        Header,
        HpackContext,
        StaticHeader,
    };
    use context::{
        NUMBER_STATIC_HEADERS,
    };
    use super::{
        encode_block,
    };


    #[test]
    /// C.5 Response Examples without Huffman Coding
    fn test_spec_example_without_huffman() {
        let mut enc_context = HpackContext::with_capacity(256);
        {
            let block = b"H\x03302X\x07privatea\x1dMon, 21 Oct 2013 20:13:21 GMTn\x17https://www.example.com";
            let mut data = Vec::new();
            data.push(Header::new(b":status", b"302", true));
            data.push(Header::new(b"cache-control", b"private", true));
            data.push(Header::new(b"date", b"Mon, 21 Oct 2013 20:13:21 GMT", true));
            data.push(Header::new(b"location", b"https://www.example.com", true));
            let mut res = Vec::with_capacity(4072);
            let len = encode_block(&mut res, &data[..], &mut enc_context, 1024);
            assert_eq!(block.len(), len);
            assert_eq!(len, 70);
            assert_eq!(block.to_vec(), res);
            assert_eq!(enc_context.len(), NUMBER_STATIC_HEADERS + 4);
            assert_eq!(enc_context.used(), 222);
        }
        {
            let block = b"H\x03307\xc1\xc0\xbf";
            let mut data = Vec::new();
            data.push(Header::new(b":status", b"307", true));
            data.push(Header::new(b"cache-control", b"private", true));
            data.push(Header::new(b"date", b"Mon, 21 Oct 2013 20:13:21 GMT", true));
            data.push(Header::new(b"location", b"https://www.example.com", true));
            let mut res = Vec::with_capacity(4072);
            let len = encode_block(&mut res, &data[..], &mut enc_context, 1024);
            assert_eq!(block.len(), len);
            assert_eq!(len, 8);
            assert_eq!(block.to_vec(), res);
            assert_eq!(enc_context.len(), NUMBER_STATIC_HEADERS + 4);
            assert_eq!(enc_context.used(), 222);
        }
        {
            let block = b"\x88\xc1a\x1dMon, 21 Oct 2013 20:13:22 GMT\xc0Z\x04gzipw8foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1";
            let mut data = Vec::new();
            data.push(Header::new(b":status", b"200", true));
            data.push(Header::new(b"cache-control", b"private", true));
            data.push(Header::new(b"date", b"Mon, 21 Oct 2013 20:13:22 GMT", true));
            data.push(Header::new(b"location", b"https://www.example.com", true));
            data.push(Header::new(b"content-encoding", b"gzip", true));
            data.push(Header::new(
                b"set-cookie",
                b"foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1",
                true,
            ));
            let mut res = Vec::with_capacity(4072);
            let len = encode_block(&mut res, &data[..], &mut enc_context, 1024);
            assert_eq!(block.len(), len);
            assert_eq!(len, 98);
            assert_eq!(block.to_vec(), res);
            assert_eq!(enc_context.len(), NUMBER_STATIC_HEADERS + 3);
            assert_eq!(enc_context.used(), 215);
        }
    }


    #[test]
    /// C.6 Response Examples with Huffman Coding
    fn test_spec_example_with_huffman() {
        let mut enc_context = HpackContext::with_capacity(256);
        {
            let block = b"H\x82d\x02X\x85\xae\xc3w\x1aKa\x96\xd0z\xbe\x94\x10T\xd4D\xa8 \x05\x95\x04\x0b\x81f\xe0\x82\xa6-\x1b\xffn\x91\x9d)\xad\x17\x18c\xc7\x8f\x0b\x97\xc8\xe9\xae\x82\xaeC\xd3";
            let mut data = Vec::new();
            data.push(Header::new(b":status", b"302", true));
            data.push(Header::new(b"cache-control", b"private", true));
            data.push(Header::new(b"date", b"Mon, 21 Oct 2013 20:13:21 GMT", true));
            data.push(Header::new(b"location", b"https://www.example.com", true));
            let mut res = Vec::with_capacity(4072);
            let len = encode_block(&mut res, &data[..], &mut enc_context, 0);
            assert_eq!(block.len(), len);
            assert_eq!(len, 54);
            assert_eq!(block.to_vec(), res);
            assert_eq!(enc_context.len(), NUMBER_STATIC_HEADERS + 4);
            assert_eq!(enc_context.used(), 222);
        }
        {
            let block = b"H\x83d\x0e\xff\xc1\xc0\xbf";
            let mut data = Vec::new();
            data.push(Header::new(b":status", b"307", true));
            data.push(Header::new(b"cache-control", b"private", true));
            data.push(Header::new(b"date", b"Mon, 21 Oct 2013 20:13:21 GMT", true));
            data.push(Header::new(b"location", b"https://www.example.com", true));
            let mut res = Vec::with_capacity(4072);
            let len = encode_block(&mut res, &data[..], &mut enc_context, 0);
            assert_eq!(len, 8);
            assert_eq!(block.to_vec(), res);
            assert_eq!(enc_context.len(), NUMBER_STATIC_HEADERS + 4);
            assert_eq!(enc_context.used(), 222);
        }
        {
            let block = b"\x88\xc1a\x96\xd0z\xbe\x94\x10T\xd4D\xa8 \x05\x95\x04\x0b\x81f\xe0\x84\xa6-\x1b\xff\xc0Z\x83\x9b\xd9\xabw\xad\x94\xe7\x82\x1d\xd7\xf2\xe6\xc7\xb35\xdf\xdf\xcd[9`\xd5\xaf'\x08\x7f6r\xc1\xab'\x0f\xb5)\x1f\x95\x871`e\xc0\x03\xedN\xe5\xb1\x06=P\x07";
            let mut data = Vec::new();
            data.push(Header::new(b":status", b"200", true));
            data.push(Header::new(b"cache-control", b"private", true));
            data.push(Header::new(b"date", b"Mon, 21 Oct 2013 20:13:22 GMT", true));
            data.push(Header::new(b"location", b"https://www.example.com", true));
            data.push(Header::new(b"content-encoding", b"gzip", true));
            data.push(Header::new(
                b"set-cookie",
                b"foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1",
                true,
            ));
            let mut res = Vec::with_capacity(4072);
            let len = encode_block(&mut res, &data[..], &mut enc_context, 0);
            assert_eq!(len, 79);
            assert_eq!(block.to_vec(), res);
            assert_eq!(enc_context.len(), NUMBER_STATIC_HEADERS + 3);
            assert_eq!(enc_context.used(), 215);
        }
    }


    #[test]
    fn test_encode_bin_0() {
        let block = b"\x82\x86A\x0byahoo.co.jp\x84";
        let mut enc_context = HpackContext::new();
        let mut data = Vec::new();
        data.push(Header::new(b":method", b"GET", true));
        data.push(Header::new(b":scheme", b"http", true));
        data.push(Header::new(b":authority", b"yahoo.co.jp", true));
        data.push(Header::new(b":path", b"/", true));
        let mut res = Vec::with_capacity(4072);
        let len = encode_block(&mut res, &data[..], &mut enc_context, 1024);
        assert_eq!(len, 16);
        assert_eq!(block.to_vec(), res);
    }


    #[test]
    fn test_encode_not_indexed_not_compressed() {
        let mut enc_context = HpackContext::new();
        let mut data = Vec::new();
        data.push(Header::new(b"X-Waka-Waka", b"value", true));
        let mut res = Vec::with_capacity(4072);
        let len = encode_block(&mut res, &data[..], &mut enc_context, 1024);
        assert_eq!(len, 14);
    }


    #[test]
    fn test_encode_not_indexed_compressed() {
        let mut enc_context = HpackContext::new();
        let mut data = Vec::new();
        data.push(Header::new(b"X-Waka-Waka", b"value", true));
        let mut res = Vec::with_capacity(4072);
        let len = encode_block(&mut res, &data[..], &mut enc_context, 0);
        assert_eq!(len, 18);
    }


    #[bench]
    fn bench_encode(b: &mut Bencher) {
        let mut enc_context = HpackContext::new();
        let mut data: Vec<StaticHeader> = Vec::new();
        data.push(
            StaticHeader {
                name: b":status",
                value: b"200",
            }
        );
        data.push(
            StaticHeader {
                name: b"content-length",
                value: b"7156",
            }
        );
        data.push(
            StaticHeader {
                name: b"cookie",
                value: b"blah=00az48010b8z3b5bh2pj0002",
            }
        );
        data.push(
            StaticHeader {
                name: b"accept",
                value: b"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        );
        data.push(
            StaticHeader {
                name: b"accept-encoding",
                value: b"gzip, deflate",
            }
        );
        data.push(
            StaticHeader {
                name: b"vary",
                value: b"Host",
            }
        );
        data.push(
            StaticHeader {
                name: b"cache-control",
                value: b"max-age=0",
            }
        );
        let mut bytes = 0;
        for header in data.iter() {
            bytes += (header.name.len() + header.value.len()) as u64;
        }
        b.bytes = bytes;
        b.iter(
            || {
                let mut res = Vec::with_capacity(1024);
                let _ = encode_block(&mut res, &data[..], &mut enc_context, 1024);
            }
        );
    }

}
