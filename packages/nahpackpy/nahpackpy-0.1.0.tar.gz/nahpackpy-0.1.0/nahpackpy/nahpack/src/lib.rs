// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


#![crate_name = "nahpack"]

#![allow(unused_features)]  // due to `feature(test)`
#![feature(alloc)]
#![feature(core)]
#![feature(libc)]
#![feature(test)]

//! nahpack is an [RFC 7541
//! HPACK](https://www.rfc-editor.org/rfc/rfc7541.txt)
//! encoder and decoder library. It compresses, decompresses, and validates
//! an [HTTP/2](https://www.rfc-editor.org/rfc/rfc7540.txt) "header block"
//! as contained in HEADERS, PUSH PROMISE, and CONTINUATION frames.


pub use context::{
    HpackContext,
    HpackEncodable,
};

pub use decode::{
    decode_block,
    Headers,
};

pub use encode::{
    encode_block,
};

pub use error::{
    HpackDecodeError,
};

pub use ffi::{
    nahpack_context_free,
    nahpack_context_new,
    nahpack_decode_block,
    nahpack_encode_block,
    nahpack_get_header,
    nahpack_headers_free,
    nahpack_headers_new,
    nahpack_set_context_capacity,
};


mod context;
mod decode;
mod encode;
mod error;
mod ffi;
