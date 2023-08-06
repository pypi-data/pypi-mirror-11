// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


use std::fmt::{
    Debug,
    Error,
    Formatter,
};
use context::encodable::{
    HpackEncodable,
};


#[repr(C)]
pub struct StaticHeader<'p> {
    pub name: &'p [u8],
    pub value: &'p [u8],
}


impl<'p> HpackEncodable for StaticHeader<'p> {

    #[inline(always)]
    fn name(&self) -> &[u8] {
        self.name
    }

    #[inline(always)]
    fn value(&self) -> &[u8] {
        self.value
    }

    #[inline(always)]
    fn is_compressable(&self) -> bool {
        true
    }
}


impl<'p> Debug for StaticHeader<'p> {

    fn fmt(&self, formatter: &mut Formatter) -> Result<(), Error> {
        write!(
            formatter,
            "Header ( name: {}, value: {} )",
            String::from_utf8(self.name().to_vec()).unwrap(),
            String::from_utf8(self.value().to_vec()).unwrap(),
        )
    }

}


pub const NUMBER_STATIC_HEADERS: usize = 61;


pub const STATIC_HEADERS: &'static [StaticHeader<'static>; NUMBER_STATIC_HEADERS] = &[
    StaticHeader {
        name: b":authority",
        value: b"",
    },
    StaticHeader {
        name: b":method",
        value: b"GET",
    },
    StaticHeader {
        name: b":method",
        value: b"POST",
    },
    StaticHeader {
        name: b":path",
        value: b"/",
    },
    StaticHeader {
        name: b":path",
        value: b"/index.html",
    },
    StaticHeader {
        name: b":scheme",
        value: b"http",
    },
    StaticHeader {
        name: b":scheme",
        value: b"https",
    },
    StaticHeader {
        name: b":status",
        value: b"200",
    },
    StaticHeader {
        name: b":status",
        value: b"204",
    },
    StaticHeader {
        name: b":status",
        value: b"206",
    },
    StaticHeader {
        name: b":status",
        value: b"304",
    },
    StaticHeader {
        name: b":status",
        value: b"400",
    },
    StaticHeader {
        name: b":status",
        value: b"404",
    },
    StaticHeader {
        name: b":status",
        value: b"500",
    },
    StaticHeader {
        name: b"accept-charset",
        value: b"",
    },
    StaticHeader {
        name: b"accept-encoding",
        value: b"gzip, deflate",
    },
    StaticHeader {
        name: b"accept-language",
        value: b"",
    },
    StaticHeader {
        name: b"accept-ranges",
        value: b"",
    },
    StaticHeader {
        name: b"accept",
        value: b"",
    },
    StaticHeader {
        name: b"access-control-allow-origin",
        value: b"",
    },
    StaticHeader {
        name: b"age",
        value: b"",
    },
    StaticHeader {
        name: b"allow",
        value: b"",
    },
    StaticHeader {
        name: b"authorization",
        value: b"",
    },
    StaticHeader {
        name: b"cache-control",
        value: b"",
    },
    StaticHeader {
        name: b"content-disposition",
        value: b"",
    },
    StaticHeader {
        name: b"content-encoding",
        value: b"",
    },
    StaticHeader {
        name: b"content-language",
        value: b"",
    },
    StaticHeader {
        name: b"content-length",
        value: b"",
    },
    StaticHeader {
        name: b"content-location",
        value: b"",
    },
    StaticHeader {
        name: b"content-range",
        value: b"",
    },
    StaticHeader {
        name: b"content-type",
        value: b"",
    },
    StaticHeader {
        name: b"cookie",
        value: b"",
    },
    StaticHeader {
        name: b"date",
        value: b"",
    },
    StaticHeader {
        name: b"etag",
        value: b"",
    },
    StaticHeader {
        name: b"expect",
        value: b"",
    },
    StaticHeader {
        name: b"expires",
        value: b"",
    },
    StaticHeader {
        name: b"from",
        value: b"",
    },
    StaticHeader {
        name: b"host",
        value: b"",
    },
    StaticHeader {
        name: b"if-match",
        value: b"",
    },
    StaticHeader {
        name: b"if-modified-since",
        value: b"",
    },
    StaticHeader {
        name: b"if-none-match",
        value: b"",
    },
    StaticHeader {
        name: b"if-range",
        value: b"",
    },
    StaticHeader {
        name: b"if-unmodified-since",
        value: b"",
    },
    StaticHeader {
        name: b"last-modified",
        value: b"",
    },
    StaticHeader {
        name: b"link",
        value: b"",
    },
    StaticHeader {
        name: b"location",
        value: b"",
    },
    StaticHeader {
        name: b"max-forwards",
        value: b"",
    },
    StaticHeader {
        name: b"proxy-authenticate",
        value: b"",
    },
    StaticHeader {
        name: b"proxy-authorization",
        value: b"",
    },
    StaticHeader {
        name: b"range",
        value: b"",
    },
    StaticHeader {
        name: b"referer",
        value: b"",
    },
    StaticHeader {
        name: b"refresh",
        value: b"",
    },
    StaticHeader {
        name: b"retry-after",
        value: b"",
    },
    StaticHeader {
        name: b"server",
        value: b"",
    },
    StaticHeader {
        name: b"set-cookie",
        value: b"",
    },
    StaticHeader {
        name: b"strict-transport-security",
        value: b"",
    },
    StaticHeader {
        name: b"transfer-encoding",
        value: b"",
    },
    StaticHeader {
        name: b"user-agent",
        value: b"",
    },
    StaticHeader {
        name: b"vary",
        value: b"",
    },
    StaticHeader {
        name: b"via",
        value: b"",
    },
    StaticHeader {
        name: b"www-authenticate",
        value: b"",
    },
];
