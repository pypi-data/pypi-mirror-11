// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


use std::ops::Index;
use std::slice;
use error::{
    HpackDecodeError,
};
use context::{
    Header,
    HpackContext,
    NUMBER_STATIC_HEADERS,
};
use decode::integer::{
    decode_integer,
};
use decode::huffman::{
    decompress_literal,
};


macro_rules! decode_integer_to_var(
    (
        $var:ident,
        $headers:ident,
        $prefix:expr,
        $len:ident,
        $idx:ident
    ) => {
    match decode_integer($headers.block, $prefix, $len, $idx) {
        Ok((idx, res)) => {
            $idx = idx;
            $var = res as usize;
        },
        Err(err) => {
            return Err(err);
        }
    }
});


macro_rules! buffered_slice(($var:ident, $slice:ident, $headers:ident) => {
    $headers.buffer.extend($slice);
    if $slice.len() > 0 {
        unsafe {
            // avoid borrow checker
            $var = slice::from_raw_parts(
                &($headers.buffer[$headers.buffer.len() - $slice.len()]) as *const u8,
                $slice.len()
            );
        }
    } else {
        $var = b"";
    }
});


macro_rules! literal_to_var(
    (
        $var:ident,
        $headers:ident,
        $len:ident,
        $idx:ident,
        $huf:ident,
        $num_octets:ident
    ) => {
    if $idx == $len {
        return Err(HpackDecodeError::InsufficientData);
    }

    $huf = $headers.block[$idx] & 128 == 128;

    decode_integer_to_var!($num_octets, $headers, 7, $len, $idx);

    $idx += $num_octets;
    if $idx > $len {
        return Err(HpackDecodeError::InsufficientData);
    }

    if $num_octets == 0 {
        $var = b"";
    } else {
        match $huf {
            true => {
                match decompress_literal(
                    &$headers.block[$idx - $num_octets..$idx],
                    &mut $headers.buffer
                ) {
                    Ok(written) => {
                        unsafe {
                            $var = slice::from_raw_parts(
                                &($headers.buffer[$headers.buffer.len() - written]) as *const u8,
                                written
                            );
                        }
                    },
                    Err(err) => {
                        return Err(err);
                    }
                }
            },
            false => {
                $var = &$headers.block[$idx - $num_octets..$idx];
            }
        }
    }
});


static HEADERS_DEFAULT_BUFFER_CAPACITY: usize = 4096 - 256;

static HEADERS_DEFAULT_CAPACITY: usize = 30;


#[repr(C)]
/// Header is a collection of decoded Header objects backed by both the
/// `block` passed to it and an owned buffer of decoded literals.
pub struct Headers<'h> {

    pub inner: Vec<Header>,  // TODO implement Iterator
    block: &'h [u8],
    buffer: Vec<u8>,
}


impl<'h> Headers<'h> {

    #[allow(dead_code)]
    #[inline(always)]
    pub fn new(block: &[u8]) -> Headers {
        Headers {
            block: block,
            buffer: Vec::with_capacity(HEADERS_DEFAULT_BUFFER_CAPACITY),
            inner: Vec::with_capacity(HEADERS_DEFAULT_CAPACITY),
        }
    }

    #[inline(always)]
    pub fn insert_header(
            &mut self,
            name: &[u8],
            value: &[u8],
            compressable: bool
        ) {
        self.inner.push(
            Header::new(name, value, compressable)
        );
    }

    #[allow(dead_code)]
    #[inline(always)]
    pub fn len(&self) -> usize {
        self.inner.len()
    }
}


impl<'h> Index<usize> for Headers<'h> {

    type Output = Header;

    #[inline(always)]
    fn index(&self, index: usize) -> &Header {
        &self.inner[index]
    }
}


/// Decode an [HTTP/2](https://www.rfc-editor.org/rfc/rfc7540.txt)
/// header block transmitted in one or more `HEADERS`, `PUSH_PROMISE`,
/// or `CONTINUATION` frames. If the header block was split across multiple
/// frames, they must first be merged.
///
/// If the header block is invalid, an `HpackDecodeError` is returned.
/// These are all fatal, and in the HTTP/2 spec require that an error be
/// returned to the sender.
///
/// # Examples
/// This implements the C.3 example from the
/// [HPACK RFC's](https://www.rfc-editor.org/rfc/rfc7541.txt).
///
/// ```
/// use nahpack::{decode_block, HpackContext, Headers};
///
/// let mut context = HpackContext::new();
///
/// {
///     // first request
///     let block = b"\x82\x86\x84A\x0fwww.example.com";
///     let mut headers = Headers::new(block);
///     match decode_block(&mut context, &mut headers) {
///         Ok(_) => { },
///         Err(_) => { }
///     }
/// }
/// {
///     // second request
///     let block = b"\x82\x86\x84\xbe\x58\x08no-cache";
///     let mut headers = Headers::new(block);
///     match decode_block(&mut context, &mut headers) {
///         Ok(_) => { },
///         Err(_) => { }
///     }
/// }
/// {
///     // third request
///     let block = b"\x82\x87\x85\xbf@\x88%\xa8I\xe9[\xa9}\x7f\x89%\xa8I\xe9[\xb8\xe8\xb4\xbf";
///     let mut headers = Headers::new(block);
///     match decode_block(&mut context, &mut headers) {
///         Ok(_) => { },
///         Err(_) => { }
///     }
/// }
/// ```
pub fn decode_block<'h>(
        context: &mut HpackContext,
        headers: &mut Headers<'h>,
    ) -> Result<(), HpackDecodeError> {
    let mut idx = 0usize;  // position in block
    let mut hdx: usize;  // header index
    let mut huf: bool;
    let mut literal_octets: usize;

    let mut name: &[u8];
    let mut value: &[u8];

    let len = headers.block.len();
    if len == 0 {
        return Err(HpackDecodeError::InsufficientData)
    }
    while idx < len {
        match headers.block[idx] {
            0b10000001...0b11111111 => {  // 129 - 255
                // 6.1 Indexed Header Field Representation

                decode_integer_to_var!(hdx, headers, 7, len, idx);
                match context.header_by_index(hdx) {
                    Some((hdr_name, hdr_value)) => {
                        if hdx > NUMBER_STATIC_HEADERS {
                            buffered_slice!(name, hdr_name, headers);
                            buffered_slice!(value, hdr_value, headers);
                            headers.insert_header(name, value, true);
                        } else {
                            headers.insert_header(hdr_name, hdr_value, true);
                        }
                    },
                    None => {
                        return Err(HpackDecodeError::InvalidIndex);
                    }
                }
            },
            0b01000001...0b01111111 => {  // 65 - 127
                // 6.2.1 Literal Header Field with Incremental Indexing
                // Figure 6--path with an indexed name

                decode_integer_to_var!(hdx, headers, 6, len, idx);
                match context.header_name_by_index(hdx) {
                    Some(header_name) => {
                        buffered_slice!(name, header_name, headers);
                    },
                    None => {
                        return Err(HpackDecodeError::InvalidIndex);
                    }
                }

                literal_to_var!(value, headers, len, idx, huf, literal_octets);

                headers.insert_header(name, value, true);
                context.insert(name, value);
            },
            0b01000000 => {  // 64
                // 6.2.1 Literal Header Field with Incremental Indexing
                // Figure 7--path with a new name

                idx += 1;
                literal_to_var!(name, headers, len, idx, huf, literal_octets);
                literal_to_var!(value, headers, len, idx, huf, literal_octets);

                headers.insert_header(name, value, true);
                context.insert(name, value);
            },
            0b00000001...0b00001111 => {  // 1 - 15
                // 6.2.2 Literal Header Field without Indexing
                // Figure 8--path with an indexed name

                decode_integer_to_var!(hdx, headers, 4, len, idx);
                match context.header_name_by_index(hdx) {
                    Some(header_name) => {
                        buffered_slice!(name, header_name, headers);
                    },
                    None => {
                        return Err(HpackDecodeError::InvalidIndex);
                    }
                }

                literal_to_var!(value, headers, len, idx, huf, literal_octets);

                headers.insert_header(name, value, true);
            },
            0b00000000 => {  // 0
                // 6.2.2 Literal Header Field without Indexing
                // Figure 9--path with a new name

                idx += 1;
                literal_to_var!(name, headers, len, idx, huf, literal_octets);
                literal_to_var!(value, headers, len, idx, huf, literal_octets);

                headers.insert_header(name, value, false);
                context.insert(name, value);
            },
            0b00010001...0b00011111 => {  // 17 - 31
                // 6.2.3 Literal Header Field never Indexed
                // Figure 10--path with an indexed name

                decode_integer_to_var!(hdx, headers, 4, len, idx);
                match context.header_name_by_index(hdx) {
                    Some(header_name) => {
                        buffered_slice!(name, header_name, headers);
                    },
                    None => {
                        return Err(HpackDecodeError::InvalidIndex);
                    }
                }

                literal_to_var!(value, headers, len, idx, huf, literal_octets);

                headers.insert_header(name, value, false);
            }
            0b00010000 => {  // 16
                // 6.2.3 Literal Header Field never Indexed
                // Figure 11--literal name and value

                idx += 1;
                literal_to_var!(name, headers, len, idx, huf, literal_octets);
                literal_to_var!(value, headers, len, idx, huf, literal_octets);

                headers.insert_header(name, value, false);
            },
            0b00100000...0b00111111 => {  // 32 - 63
                // 6.3 Dynamic Table Size Update

                decode_integer_to_var!(hdx, headers, 5, len, idx);
                try!(context.resize(hdx as u32));
            },
            _ => {
                // 6.1 with `0` index
                return Err(HpackDecodeError::InvalidIndex)
            }
        }
    }
    Ok(())
}


#[cfg(test)]
mod test {
    extern crate test;
    use self::test::Bencher;

    use context::{
        NUMBER_STATIC_HEADERS,
    };
    use context::{
        HpackContext,
        HpackEncodable,
    };
    use error::{
        HpackDecodeError,
    };
    use super::{
        Headers,
        decode_block,
    };

    #[test]
    /// Headers::new() for coverage
    fn test_headers_new() {
        let block = b"";
        let headers = Headers::new(block);
        assert!(headers.block == block);
    }


    #[test]
    /// block with no bytes is a decode error
    fn test_decode_no_block() {
        let mut context = HpackContext::new();
        let mut headers = Headers::new(b"");
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InsufficientData
        );
    }


    #[test]
    /// 6.1 with a `0` index is a decode error
    fn test_decode_61_0() {
        let mut context = HpackContext::new();
        let block = &[0b10000000, ];
        let mut headers = Headers::new(block);
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InvalidIndex
        );
    }


    #[test]
    /// 6.1 with a non-existent index is a decode error
    fn test_decode_61_invalid_index() {
        let mut context = HpackContext::new();
        let block = &[0b10111111, ];
        let mut headers = Headers::new(block);
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InvalidIndex
        );
    }


    #[test]
    /// 6.1 indexed header
    fn test_decode_indexed() {
        let mut context = HpackContext::new();
        let block = &[0b10000010, ];
        let mut headers = Headers::new(block);
        {
            decode_block(&mut context, &mut headers).unwrap();
        }
        assert_eq!(headers.len(), 1usize);
        assert_eq!(headers[0].name(), b":method");
        assert_eq!(headers[0].value(), b"GET");
    }


    #[test]
    /// 6.1 indexed header invalid index
    fn test_decode_indexed_invalid_index() {
        let mut context = HpackContext::new();
        let block = &[0b10111111, ];
        let mut headers = Headers::new(block);
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InvalidIndex
        );
    }


    #[test]
    fn test_decode_literal_insufficient_data() {
        let mut context = HpackContext::new();
        let block = b"\x82\x86A\x0byahoo.\x84";
        let mut headers = Headers::new(block);
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InsufficientData
        );
    }


    #[test]
    fn test_context_resize() {
        let mut context = HpackContext::new();
        assert_eq!(context.capacity(), 4096);
        let block = &[0b00100001, ];
        let mut headers = Headers::new(block);
        {
            let _ = decode_block(&mut context, &mut headers).unwrap();
        }
        assert_eq!(context.capacity(), 1);
    }


    #[test]
    fn test_context_resize_invalid_int() {
        let mut context = HpackContext::new();
        assert_eq!(context.capacity(), 4096);
        let block = &[0b00111111, 255];
        let mut headers = Headers::new(block);
        {
            assert_eq!(
                decode_block(&mut context, &mut headers).err().unwrap(),
                HpackDecodeError::InvalidInteger
            );
        }
    }


    #[test]
    fn test_context_resize_exceeds_setting() {
        let mut context = HpackContext::new();
        context.set_capacity(1);
        let block = &[0b00100010, ];
        let mut headers = Headers::new(block);
        {
            assert_eq!(
                decode_block(&mut context, &mut headers).err().unwrap(),
                HpackDecodeError::SettingsSizeExceeded
            );
        }
    }


    #[test]
    /// 6.2.1 indexed
    fn test_decode_literal_indexed() {
        let mut context = HpackContext::new();
        let block = &[
            0b01000001,
            0b00000101,
            118, 97, 108, 117, 101,
        ];
        let mut headers = Headers::new(block);
        let _ = decode_block(&mut context, &mut headers).unwrap();
        assert_eq!(headers.len(), 1);
        assert_eq!(headers[0].name(), b":authority");
        assert_eq!(headers[0].value(), [118, 97, 108, 117, 101]);
    }


    #[test]
    /// 6.2.1 invalid index
    fn test_decode_literal_indexed_invalid_index() {
        let mut context = HpackContext::new();
        let block = &[0b01111111, 50];
        let mut headers = Headers::new(block);
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InvalidIndex
        );
    }


    #[test]
    /// 6.2.1 new
    fn test_decode_literal_indexed_new() {
        let mut context = HpackContext::new();
        let block = &[
            0b01000000,
            0b00000100,
            110, 97, 109, 101, // "name"
            0b00000101,
            118, 97, 108, 117, 101 // "value"
        ];
        let mut headers = Headers::new(block);
        let _ = decode_block(&mut context, &mut headers).unwrap();
        assert_eq!(headers.len(), 1);
        assert_eq!(headers[0].name(), b"name");
        assert_eq!(headers[0].value(), b"value");
    }


    #[test]
    /// 6.2.2 using index for name, literal value
    fn test_decode_literal_indexed_name() {
        let mut context = HpackContext::new();
        let block = &[1, 5, 118, 97, 108, 117, 101];
        let mut headers = Headers::new(block);
        let _ = decode_block(&mut context, &mut headers).unwrap();
    }


    #[test]
    /// 6.2.2 using invalid index for name
    /// HERE
    fn test_decode_literal_invalid_index() {
        let mut context = HpackContext::new();
        let block = b"\x0f\xb9\x01'";
        let mut headers = Headers::new(block);
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InvalidIndex
        );
    }


    #[test]
    /// 6.2.2
    fn test_decode_literal_never_indexed_new_insufficient_data() {
        let mut context = HpackContext::new();
        let block = &[0b00000000, ];
        let mut headers = Headers::new(block);
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InsufficientData
        );
    }


    #[test]
    /// 6.2.3
    fn test_decode_literal_never_indexed() {
        let mut context = HpackContext::new();
        let block = &[
            0b00010000,
            0b00000100,
            110, 97, 109, 101, // "name"
            0b00000101,
            118, 97, 108, 117, 101 // "value"
        ];
        let mut headers = Headers::new(block);
        assert!(decode_block(&mut context, &mut headers).is_ok());
        assert_eq!(context.len(), NUMBER_STATIC_HEADERS);
        assert_eq!(headers.len(), 1);
        assert_eq!(headers[0].name(), b"name");
        assert_eq!(headers[0].value(), b"value");
    }


    #[test]
    /// 6.2.3 using index for name, literal value
    fn test_decode_literal_never_indexed_name() {
        let mut context = HpackContext::new();
        let block = &[0b00010001, 5, 118, 97, 108, 117, 101];
        let mut headers = Headers::new(block);
        let _ = decode_block(&mut context, &mut headers).unwrap();
    }


    #[test]
    /// 6.2.3
    fn test_decode_literal_never_indexed_insufficient_data() {
        let mut context = HpackContext::new();
        let block = &[0b00010000, ];
        let mut headers = Headers::new(block);
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InsufficientData
        );
    }


    #[test]
    /// 6.2.3
    fn test_decode_literal_never_indexed_invalid_header() {
        let mut context = HpackContext::new();
        let block = &[0b00011111, 169, 1];
        let mut headers = Headers::new(block);
        assert_eq!(
            decode_block(&mut context, &mut headers).err().unwrap(),
            HpackDecodeError::InvalidIndex
        );
    }


    #[test]
    fn test_decode_bin_0() {
        let mut context = HpackContext::new();
        let block = b"\x82\x86A\x88\xf49\xceu\xc8u\xfaW\x84";
        let mut headers = Headers::new(block);
        let _ = decode_block(&mut context, &mut headers).unwrap();
    }


    #[test]
    fn test_decode_bin_1() {
        let mut context = HpackContext::new();
        let block = b"\x82\x86A\x8c\xf1\xe3\xc2\xfe\x879\xce\xb9\x0e\xbfJ\xff\x84";
        let mut headers = Headers::new(block);
        let _ = decode_block(&mut context, &mut headers).unwrap();
    }


    #[test]
    fn test_decode_bin_2() {
        let mut context = HpackContext::new();
        let block = b"\x82\x86A\x87\xea\xbf\xa3S2\xfd+\x04\x9b`\xd4\x8eb\xa1\x84\x9e\xb6\x11X\x98%51A\xe6:\xd5!`\xb2\x06\xc4\xf2\xf5\xd57";
        let mut headers = Headers::new(block);
        let _ = decode_block(&mut context, &mut headers).unwrap();
    }


    #[test]
    fn test_decode_bin_3() {
        let mut context = HpackContext::new();
        let block = b"\x0f\r\x82lB@\x90\xf2\xb1\x0fRKRVO\xaa\xca\xb1\xebI\x8fR?\x85\xa8\xe8\xa8\xd2\xcb\x89\x0f\x17\x96\xdfi~\x94\x10T\xd0?J\x08\x01e@\xbfp/\\e\x951h\xdf@\x87\xf2\xb1*)\x12c\xd5\x84%\x07A\x7f\x0f \x96\xdf=\xbfJ\x04JC]\x8a\x08\x01\x12\x80f\xe0\x19\xb8 )\x8bF\xff@\x87!\xea\xa8\xa4I\x8fW\x88\xeaR\xd6\xb0\xe87r\xff\x0f\r\x92\xae\xd8\xe81>\x94\xa4~V\x1c\xc5\x80.\x88.<\xe3\xff\x0f\x16\x96\xdc4\xfd(\x06T\xd2~\xea\x08\x01\x12\x81\x15\xc6\xc1q\xa6\x94\xc5\xa3\x7f\x0f\t\x81\xf9\x0f\x14\x875#\x98\xacLi\x7f@\x88\xf2\xb4\xb1\xad!c\xb6o\xa4\xc9\xc4\xacn\xf1i2\xdbu\x19\xd3\xc7\x1f,\xbe\x05\xafD\x9a\xb7\xea\xf3n\x0e\\\rcf\x9bf\x9d\xf3\xf5\xdf4\x1f";
        let mut headers = Headers::new(block);
        let _ = decode_block(&mut context, &mut headers).unwrap();
    }

    #[test]
    fn test_invalid_compressed_literal() {
        let mut context = HpackContext::new();
        let request = b"\x82\x86\x84A\x8c\xf1\xe3\xc2\xe5\xf2:k\xa0\xab\x90\xf4\x00";
        let mut headers = Headers::new(request);
        {
            assert_eq!(
                decode_block(&mut context, &mut headers).err().unwrap(),
                HpackDecodeError::InvalidCompressedLiteral
            );
        }
    }


    #[bench]
    fn bench_decode_spec_example(b: &mut Bencher) {
        let mut context = HpackContext::new();
        {
            let block = b"\x82\x86A\tbaidu.com\x84zQMozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20100101 Firefox/16.0S?text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Q\x0een-US,en;q=0.5\x90@\nconnection\nkeep-alive";
            let mut headers = Headers::new(block);
            let _ = decode_block(&mut context, &mut headers).unwrap();
        }
        {
            let block = b"\x82\x86\xc2\x04\x0c/favicon.ico\xc1\xc0\xbf\x90\xbe";
            let mut headers = Headers::new(block);
            let _ = decode_block(&mut context, &mut headers).unwrap();
        }
        {
            let block = b"\x82\x86A\rwww.baidu.com\x84\xc2\xc1\xc0\x90\xbf";
            let mut headers = Headers::new(block);
            let _ = decode_block(&mut context, &mut headers).unwrap();
        }
        let block = b"\x82\x86\xbe\x04\x16/img/baidu_sylogo1.gif\xc2S!image/png,image/*;q=0.8,*/*;q=0.5\xc1\x90\xc0s\x15http://www.baidu.com/`-BAIDUID=B6136AC10EBE0A8FCD216EB64C4C1A5C:FG=1";

        b.bytes = block.len() as u64;
        b.iter(
            || {
                let mut headers = Headers::new(block);
                let _ = decode_block(&mut context, &mut headers);
            }
        );
    }


    #[bench]
    fn bench_decode_spec_example_full(b: &mut Bencher) {
        b.iter(|| {
            let mut context = HpackContext::new();
            {
                let block = b"\x82\x86A\tbaidu.com\x84zQMozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20100101 Firefox/16.0S?text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Q\x0een-US,en;q=0.5\x90@\nconnection\nkeep-alive";
                let mut headers = Headers::new(block);
                {
                    decode_block(&mut context, &mut headers).unwrap();
                }
            }
            {
                let block = b"\x82\x86\xc2\x04\x0c/favicon.ico\xc1\xc0\xbf\x90\xbe";
                let mut headers = Headers::new(block);
                {
                    decode_block(&mut context, &mut headers).unwrap();
                }
            }
            {
                let block = b"\x82\x86A\rwww.baidu.com\x84\xc2\xc1\xc0\x90\xbf";
                let mut headers = Headers::new(block);
                {
                    decode_block(&mut context, &mut headers).unwrap();
                }
            }
            {
                let block = b"\x82\x86\xbe\x04\x16/img/baidu_sylogo1.gif\xc2S!image/png,image/*;q=0.8,*/*;q=0.5\xc1\x90\xc0s\x15http://www.baidu.com/`-BAIDUID=B6136AC10EBE0A8FCD216EB64C4C1A5C:FG=1";
                let mut headers = Headers::new(block);
                {
                    decode_block(&mut context, &mut headers).unwrap();
                }
            }
        });
    }


    #[test]
    fn test_story_31() {
    let mut context = HpackContext::new();
        let block = b"\x0f\r\x03522\x00\x16x-content-type-options\x07nosniff\x88\x0f\x15\x1dTue, 21 May 2013 19:18:33 GMT\x00\nx-cnection\x05close\x0f\x1d\x1dThu, 12 Apr 2012 03:03:20 GMT\x00\nconnection\nkeep-alive\x0f\t\x18public, max-age=17216869\x0f\x12\x1dSat, 03 Nov 2012 12:50:44 GMT\x0f\x05\x01*\x0f\x10\timage/gif\x00\nx-fb-debug,IVe/SwucJuBsLtVHWJw2PMdOTOxuEWUir5igQNThkTg=";
        let mut headers = Headers::new(block);
        let _ = decode_block(&mut context, &mut headers).unwrap();
        assert_eq!(headers.len(), 12usize);
    }


    #[bench]
    fn bench_decode_bin_1(b: &mut Bencher) {
        let block = b"\x82\x86A\x8c\xf1\xe3\xc2\xfe\x879\xce\xb9\x0e\xbfJ\xff\x84";
        b.bytes = block.len() as u64;
        b.iter(
            || {
                let mut context = HpackContext::new();
                let mut headers = Headers::new(block);
                let _ = decode_block(&mut context, &mut headers).unwrap();
            }
        );
    }


    #[bench]
    fn bench_decode_bin_3(b: &mut Bencher) {
        let block = b"\x0f\r\x82lB@\x90\xf2\xb1\x0fRKRVO\xaa\xca\xb1\xebI\x8fR?\x85\xa8\xe8\xa8\xd2\xcb\x89\x0f\x17\x96\xdfi~\x94\x10T\xd0?J\x08\x01e@\xbfp/\\e\x951h\xdf@\x87\xf2\xb1*)\x12c\xd5\x84%\x07A\x7f\x0f \x96\xdf=\xbfJ\x04JC]\x8a\x08\x01\x12\x80f\xe0\x19\xb8 )\x8bF\xff@\x87!\xea\xa8\xa4I\x8fW\x88\xeaR\xd6\xb0\xe87r\xff\x0f\r\x92\xae\xd8\xe81>\x94\xa4~V\x1c\xc5\x80.\x88.<\xe3\xff\x0f\x16\x96\xdc4\xfd(\x06T\xd2~\xea\x08\x01\x12\x81\x15\xc6\xc1q\xa6\x94\xc5\xa3\x7f\x0f\t\x81\xf9\x0f\x14\x875#\x98\xacLi\x7f@\x88\xf2\xb4\xb1\xad!c\xb6o\xa4\xc9\xc4\xacn\xf1i2\xdbu\x19\xd3\xc7\x1f,\xbe\x05\xafD\x9a\xb7\xea\xf3n\x0e\\\rcf\x9bf\x9d\xf3\xf5\xdf4\x1f";
        b.bytes = block.len() as u64;
        b.iter(
            || {
                let mut context = HpackContext::new();
                let mut headers = Headers::new(block);
                let _ = decode_block(&mut context, &mut headers).unwrap();
            }
        );
    }


    #[bench]
    fn bench_story_07(b: &mut Bencher) {
        let block = b"\x82\x86\x01\x13static.ak.fbcdn.net\x04!/rsrc.php/v2/yb/r/GsNJNwuI-UM.gif\x0f+QMozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20100101 Firefox/16.0\x0f\x04!image/png,image/*;q=0.8,*/*;q=0.5\x0f\x02\x0een-US,en;q=0.5\x90@\nconnection\nkeep-alive\x0f$\x18http://www.facebook.com/";
        b.bytes = block.len() as u64;
        b.iter(
            || {
                let mut context = HpackContext::new();
                let mut headers = Headers::new(block);
                let _ = decode_block(&mut context, &mut headers).unwrap();
            }
        );
    }


    #[bench]
    fn bench_decode_story_31(b: &mut Bencher) {
        let block = b"\x0f\r\x03522\x00\x16x-content-type-options\x07nosniff\x88\x0f\x15\x1dTue, 21 May 2013 19:18:33 GMT\x00\nx-cnection\x05close\x0f\x1d\x1dThu, 12 Apr 2012 03:03:20 GMT\x00\nconnection\nkeep-alive\x0f\t\x18public, max-age=17216869\x0f\x12\x1dSat, 03 Nov 2012 12:50:44 GMT\x0f\x05\x01*\x0f\x10\timage/gif\x00\nx-fb-debug,IVe/SwucJuBsLtVHWJw2PMdOTOxuEWUir5igQNThkTg=";
        b.bytes = block.len() as u64;
        b.iter(
            || {
                let mut context = HpackContext::new();
                let mut headers = Headers::new(block);
                let _ = decode_block(&mut context, &mut headers).unwrap();
            }
        );
    }

}
