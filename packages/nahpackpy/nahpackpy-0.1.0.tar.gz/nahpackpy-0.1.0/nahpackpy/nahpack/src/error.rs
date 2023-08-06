// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


/// HPACK decoding error states are detailed here.
#[derive(Debug,PartialEq)]
#[repr(C)]
pub enum HpackDecodeError {

    /// The header block ends prematurely.
    InsufficientData = -1,

    /// There was reference to an indexed header that is not in the table.
    InvalidIndex = -2,

    /// An integer could not be decoded.
    InvalidInteger = -3,

    /// This library's limit of an integer being at most 4 bytes was exceeded.
    ExcessiveInteger = -4,

    /// The compressed literal could not be decoded.
    InvalidCompressedLiteral = -5,

    /// EOS symbol was unexpectedly found in a compressed literal.
    IllegalEOS = -6,

    /// Header block gave a value for table resize that exceeds the value
    /// set by a settings frame.
    SettingsSizeExceeded = -7,
}
