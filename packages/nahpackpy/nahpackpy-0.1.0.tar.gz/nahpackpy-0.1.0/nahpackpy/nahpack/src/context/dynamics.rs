// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


use std::slice;
use std::fmt::{
    Debug,
    Error,
    Formatter,
};
use context::encodable::{
    HpackEncodable,
};


/// Header is a decoded header of &[u8] backed by a Headers buffer.
#[repr(C)]
pub struct Header {
    name: (*const u8, usize),
    value: (*const u8, usize),
    compressable: bool,
}


impl Header {

    #[inline(always)]
    pub fn new(
            name: &[u8],
            value: &[u8],
            compressable: bool,
        ) -> Header {
        Header {
            name: (name.as_ptr(), name.len()),
            value: (value.as_ptr(), value.len()),
            compressable: compressable,
        }
    }

}


impl HpackEncodable for Header {

    #[inline(always)]
    fn name(&self) -> &[u8] {
        unsafe {
            slice::from_raw_parts(self.name.0, self.name.1)
        }
    }

    #[inline(always)]
    fn value(&self) -> &[u8] {
        let value = unsafe {
            slice::from_raw_parts(self.value.0, self.value.1)
        };
        value
    }

    #[inline(always)]
    fn is_compressable(&self) -> bool {
        self.compressable
    }

}


impl Debug for Header {

    fn fmt(&self, formatter: &mut Formatter) -> Result<(), Error> {
        write!(
            formatter,
            "Header ( name: {}, value: {} )",
            String::from_utf8(self.name().to_vec()).unwrap(),
            String::from_utf8(self.value().to_vec()).unwrap(),
        )
    }

}


#[derive(Clone)]
#[repr(C)]
pub struct DynamicHeader {
    seg: usize,
    buf: Vec<u8>,
}


impl DynamicHeader {

    #[inline]
    pub fn new(name: &[u8], value: &[u8]) -> DynamicHeader {
        let mut buf = Vec::with_capacity(name.len() + value.len());
        buf.extend(name);
        buf.extend(value);
        DynamicHeader {
            seg: name.len(),
            buf: buf,
        }
    }

}


impl HpackEncodable for DynamicHeader {

    #[inline(always)]
    fn name(&self) -> &[u8] {
        &self.buf[0..self.seg]
    }

    #[inline(always)]
    fn value(&self) -> &[u8] {
        &self.buf[self.seg..self.buf.len()]
    }

    #[inline]
    fn size(&self) -> u32 {
        self.buf.len() as u32 + 32
    }

    #[inline]
    fn is_compressable(&self) -> bool {
        true
    }

}


impl Debug for DynamicHeader {

    fn fmt(&self, formatter: &mut Formatter) -> Result<(), Error> {
        write!(
            formatter,
            "DynamicHeader ( name: {}, value: {} )",
            String::from_utf8(self.name().to_vec()).unwrap(),
            String::from_utf8(self.value().to_vec()).unwrap(),
        )
    }

}
