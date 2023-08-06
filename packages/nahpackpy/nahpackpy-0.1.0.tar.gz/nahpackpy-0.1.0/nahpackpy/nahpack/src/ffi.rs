// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

extern crate alloc;
extern crate core;
extern crate libc;
use self::alloc::boxed::Box;
use self::core::mem;
use std::slice::from_raw_parts;

use context::{
    HpackContext,
    Header,
};
use decode::{
    decode_block,
    Headers,
};
use encode::{
    encode_block,
};


#[allow(dead_code)]
#[no_mangle]
pub extern "C" fn nahpack_context_new() -> *mut HpackContext {
    let context: Box<HpackContext> = Box::new(HpackContext::new());
    let res: *mut HpackContext = unsafe { mem::transmute(context) };
    res
}


#[allow(dead_code)]
#[no_mangle]
pub extern "C" fn nahpack_set_context_capacity(
        context: *mut HpackContext,
        size: libc::uint32_t
    ) {
    let rcontext: &mut HpackContext = unsafe { mem::transmute(context) };
    rcontext.set_capacity(size as u32);
}


#[allow(dead_code)]
#[no_mangle]
pub extern "C" fn nahpack_context_free(context: *mut HpackContext) {
    let context: Box<HpackContext> = unsafe { mem::transmute(context) };
    drop(*context);
}


#[allow(dead_code)]
#[no_mangle]
pub extern "C" fn nahpack_headers_new<'a>(
        block: *const libc::uint8_t,
        block_len: libc::size_t
    ) -> *mut Headers<'a> {
    let rblock: &[u8] = unsafe {
        mem::transmute(
            from_raw_parts(block, block_len as usize)
        )
    };
    let context: Box<Headers> = Box::new(
        Headers::new(rblock)
    );
    let res: *mut Headers = unsafe { mem::transmute(context) };
    res
}


#[allow(dead_code)]
#[no_mangle]
pub extern "C" fn nahpack_headers_free(headers: *mut Headers) {
    let headers: Box<Headers> = unsafe { mem::transmute(headers) };
    drop(*headers);
}


#[allow(dead_code)]
#[no_mangle]
pub extern "C" fn nahpack_get_header(headers: *mut Headers, index: usize) -> *const Header {
    let rheaders: &mut Headers = unsafe { mem::transmute(headers) };
    let res: *const Header;
    if index > rheaders.inner.len() {
        unsafe { res = mem::transmute(0usize); }
    } else {
        unsafe { res = mem::transmute(&rheaders.inner[index]); }
    }
    res
}


#[allow(dead_code)]
#[no_mangle]
pub extern "C" fn nahpack_decode_block(
        context: *mut HpackContext,
        headers: *mut Headers
    ) -> libc::ssize_t {
    let mut rcontext: &mut HpackContext = unsafe { mem::transmute(context) };
    let mut rheaders: &mut Headers = unsafe { mem::transmute(headers) };
    match decode_block(&mut rcontext, &mut rheaders) {
        Ok(_) => { },
        Err(err) => { return err as libc::ssize_t }
    }
    rheaders.len() as libc::ssize_t
}


#[allow(dead_code)]
#[no_mangle]
pub extern "C" fn nahpack_encode_block(
        block: *const Header,
        len: libc::size_t,
        context: *mut HpackContext,
        callback: extern fn(*mut libc::c_void, *const libc::uint8_t, libc::size_t),
        passthrough_ptr: *mut libc::c_void,
    ) -> libc::ssize_t {
    let block_slice: &[Header] = unsafe {
        from_raw_parts(block, len as usize)
    };
    let mut rcontext: &mut HpackContext = unsafe { mem::transmute(context) };

    let mut rvec: Vec<u8> = Vec::with_capacity(4096);
    let num_bytes = encode_block(&mut rvec, block_slice, &mut rcontext, 0);

    let output_slice: &[i8] = unsafe { mem::transmute(&rvec[..]) };
    callback(
        passthrough_ptr,
        output_slice.as_ptr() as *const libc::uint8_t,
        num_bytes as libc::size_t,
    );
    num_bytes as libc::ssize_t
}


#[cfg(test)]
mod test {
    extern crate libc;
    extern crate core;
    use self::core::mem;
    use std::ffi::CString;
    use std::slice::from_raw_parts;
    use super::*;

    use context::{
        Header,
        HpackContext,
    };


    #[test]
    fn test_decode_block() {
        let slice = b"\x82\x86\x84A\x0fwww.example.com";
        let buffer = CString::new(slice.to_vec()).unwrap().as_ptr();
        let context = nahpack_context_new();
        let headers = nahpack_headers_new(
            buffer as *const libc::uint8_t,
            slice.len() as u64,
        );
        let res = nahpack_decode_block(context, headers);
        assert_eq!(res, 4);
        nahpack_headers_free(headers);
        nahpack_context_free(context);
    }


    extern "C" fn encode_callback(
            buffer: *mut libc::c_void,
            block: *const libc::uint8_t,
            len: libc::size_t
        ) {
        let rbuffer: &mut Vec<u8> = unsafe { mem::transmute(buffer) };
        let rblock: &[u8] = unsafe {
            from_raw_parts(block, len as usize)
        };
        rbuffer.extend(rblock);
        assert_eq!(rbuffer.len(), len as usize);
    }


    #[test]
    fn test_encode_block() {
        let mut result_buffer: Vec<u8> = Vec::with_capacity(1024);

        let headers: [Header; 4] = [
            Header::new(b":method", b"GET", true),
            Header::new(b":scheme", b"http", true),
            Header::new(b":path", b"/", true),
            Header::new(b":authority", b"www.example.com", true),
        ];
        let context = nahpack_context_new();

        let res = nahpack_encode_block(
            headers.as_ptr(),
            4,
            context,
            encode_callback,
            result_buffer.as_mut_ptr() as *mut libc::c_void,
        );
        assert_eq!(res, 17);

        // todo `result_buffer.len() == 0`, so:
        let rbuffer: &mut Vec<u8> = unsafe {
            mem::transmute(result_buffer.as_mut_ptr() as *mut libc::c_void)
        };
        assert_eq!(rbuffer.len(), 17);
        assert_eq!(
            &rbuffer[0 .. 17],
            b"\x82\x86\x84A\x8c\xf1\xe3\xc2\xe5\xf2:k\xa0\xab\x90\xf4\xff"
        );

        assert_eq!(headers.len(), 4);
        nahpack_context_free(context);
    }


    #[test]
    fn test_decode_block_invalid() {
        let slice = b"\x01";
        let buffer = CString::new(slice.to_vec()).unwrap().as_ptr();
        let context = nahpack_context_new();
        let headers = nahpack_headers_new(
            buffer as *const libc::uint8_t,
            slice.len() as u64,
        );
        let res = nahpack_decode_block(context, headers);
        assert_eq!(res, -1);
        nahpack_headers_free(headers);
        nahpack_context_free(context);
    }


    #[test]
    fn test_set_context_capacity() {
        let context = nahpack_context_new();
        nahpack_set_context_capacity(context, 8192);
        let rcontext: &mut HpackContext = unsafe { mem::transmute(context) };
        assert_eq!(8192, rcontext.settings_capacity());
    }

}
