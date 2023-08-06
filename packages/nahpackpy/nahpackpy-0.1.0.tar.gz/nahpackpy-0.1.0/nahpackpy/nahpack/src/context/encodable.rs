// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


/// HpackEncodable is the interface which headers decoded by `decode_block`
/// adhere to, and headers to be encoded by `encode_block` must adhere to.
pub trait HpackEncodable {

    /// Bytes of the header's name. No validation has been performed.
    #[inline]
    fn name(&self) -> &[u8];

    /// Bytes of the header's value. No validation has been performed.
    #[inline]
    fn value(&self) -> &[u8];

    /// Calculates the HPACK-defined size of this header, which includes
    /// a specified amount of overhead. This affects the capacity remaining
    /// in dynamic tables. It does not indicate the object's size in memory.
    fn size(&self) -> u32 {
        (self.name().len() + self.value().len()) as u32 + 32
    }

    /// For headers containing information that must remain private (e.g.,
    /// `Authorization`), both compression and entry to the dynamic table,
    /// which is potentially shared, can be disabled. Headers that return
    /// `false` here are encoded as never-indexed literals.
    #[inline]
    fn is_compressable(&self) -> bool;

}
