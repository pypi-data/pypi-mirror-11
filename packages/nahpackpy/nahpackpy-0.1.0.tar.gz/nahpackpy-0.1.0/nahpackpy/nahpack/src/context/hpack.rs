// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


use std::collections::VecDeque;

use error::{
    HpackDecodeError,
};
use context::statics::{
    NUMBER_STATIC_HEADERS,
    STATIC_HEADERS,
    StaticHeader,
};
use context::dynamics::{
    DynamicHeader,
};
use context::encodable::{
    HpackEncodable,
};


pub const DEFAULT_DYNAMIC_TABLE_SIZE: u32 = 4096;


#[derive(Debug,PartialEq)]
#[repr(C)]
pub enum HeaderMatch {
    NoMatch = 0,
    PartialMatch = 1,
    ExactMatch = 2,
}


pub const STATIC_NAME_HASHES: &'static [u64; NUMBER_STATIC_HEADERS] = &[
    9804212764789973231,
    3935597810934138275,
    3935597810934138275,
    2813736326501155653,
    2813736326501155653,
    8034644593952000117,
    8034644593952000117,
    16760268494586961328,
    16760268494586961328,
    16760268494586961328,
    16760268494586961328,
    16760268494586961328,
    16760268494586961328,
    16760268494586961328,
    5832268178580645549,
    17575425420285973585,
    13813587645528885630,
    4719998439915665237,
    10403716137041344024,
    3858984777405725827,
    5174106015222579547,
    2737172024924371865,
    13724495111684852361,
    12060518562027835438,
    5892510698016766559,
    14308046916566642613,
    12860498637404006466,
    3151113280193573028,
    10712240356488876367,
    8893873012219113581,
    7046745349106309264,
    12829516086434206662,
    5190672623209665236,
    12665991646063912629,
    6143453806934152073,
    8454952118092024740,
    842967327269899056,
    701543821944900562,
    16992311201626097831,
    8269074199898523202,
    361141770380727020,
    14066196517025818171,
    381858477305791709,
    8830586315060107844,
    844327650770374768,
    12814791534803762599,
    3398265324783889743,
    610117102360019422,
    15463904469916458576,
    7178591564177704885,
    2615655976016620953,
    4248774582039396811,
    7322828425559916945,
    1779401126493601483,
    17926239735044206937,
    2075775169895360534,
    7251324828759648795,
    1113210331033828639,
    432250841288650776,
    18411672961051154064,
    7783164523854228551,
];


pub const STATIC_VALUE_HASHES: &'static [u64; NUMBER_STATIC_HEADERS] = &[
    0,
    7478775843406383772,
    6266954156490974954,
    51677046525917,
    2567418391244101994,
    12369302829782977792,
    2469855966792981097,
    12715550713149969446,
    12715555111196482290,
    12715552912173225868,
    13370330778299875005,
    14025207600473063132,
    14025203202426550288,
    14679983267576455847,
    0,
    0,
    2509498677697523587,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
];


/// HpackContext contains the state, namely dynamic table and capacity
/// setting, for either the transmitting or receiving part of a
/// connection.
#[repr(C)]
pub struct HpackContext {
    statics: &'static [StaticHeader<'static>; NUMBER_STATIC_HEADERS],
    static_name_hashes: &'static [u64; NUMBER_STATIC_HEADERS],
    static_value_hashes: &'static [u64; NUMBER_STATIC_HEADERS],
    pub dynamics: VecDeque<DynamicHeader>,
    capacity: u32,
    settings_capacity: u32,
    used: u32,
}


impl HpackContext {

    /// Instantiate an HpackContext with the specification's default dynamic
    /// table capacity of 4,096 octets.
    #[inline(always)]
    pub fn new() -> HpackContext {
        HpackContext {
            statics: STATIC_HEADERS,
            static_name_hashes: STATIC_NAME_HASHES,
            static_value_hashes: STATIC_VALUE_HASHES,
            dynamics: VecDeque::with_capacity(30),
            capacity: DEFAULT_DYNAMIC_TABLE_SIZE,
            settings_capacity: DEFAULT_DYNAMIC_TABLE_SIZE,
            used: 0,
        }
    }

    /// Instantiate an HpackContext with a dynamic table capacity of the
    /// given number of octets.
    #[inline(always)]
    pub fn with_capacity(size: u32) -> HpackContext {
        HpackContext {
            statics: STATIC_HEADERS,
            static_name_hashes: STATIC_NAME_HASHES,
            static_value_hashes: STATIC_VALUE_HASHES,
            dynamics: VecDeque::with_capacity(30),
            capacity: size,
            settings_capacity: DEFAULT_DYNAMIC_TABLE_SIZE,
            used: 0,
        }
    }

    /// Number of headers in the context, both static and dynamic.
    #[inline]
    pub fn len(&self) -> usize {
        self.dynamics.len() + NUMBER_STATIC_HEADERS
    }

    /// The number of octets, with HPACK-specified overhead included, that the
    /// dynamic table can hold.
    #[inline(always)]
    pub fn capacity(&self) -> u32 {
        self.capacity
    }

    /// The number of octets, with HPACK-specified overhead included, that are
    /// used by the dynamic table.
    #[inline(always)]
    pub fn used(&self) -> u32 {
        self.used
    }

    /// Set the dynamic table's capacity to the number of HPACK-specified
    /// octets given. The value given must be from a SETTINGS frame.
    ///
    /// Headers will be evicted from the dynamic table as necessary.
    pub fn set_capacity(&mut self, value: u32) {
        self.settings_capacity = value;
        if value < self.capacity {
            self.shrink_to_fit(value);
            self.capacity = value;
        }
    }

    pub fn settings_capacity(&self) -> u32 {
        self.settings_capacity
    }

    /// Resize the dynamic table's size to the number of HPACK-specified
    /// octets given.
    ///
    /// Headers will be evicted from the dynamic table as necessary.
    pub fn resize(&mut self, value: u32) -> Result<(), HpackDecodeError> {
        if value > self.settings_capacity {
            return Err(HpackDecodeError::SettingsSizeExceeded)
        }
        if value < self.capacity {
            self.shrink_to_fit(value);
        }
        self.capacity = value;
        Ok(())
    }

    fn shrink_to_fit(&mut self, value: u32) {
        let mut diff = self.used as i32 - value as i32;
        if diff > 0 {
            if value == 0 {
                self.used = 0;
                self.dynamics.clear();
            } else {
                while diff > 0 {
                    let size = self.dynamics.pop_back().unwrap().size();
                    self.used -= size;
                    diff -= size as i32;
                }
            }
        }
    }

    /// Insert a header into the dynamic table.
    ///
    /// If the given header exceeds the dynamic table's size,
    /// the insert may only clear the dynamic table without being added. The
    /// returned bool indicates whether the header was added or not.
    ///
    /// If it was added, it now occupies the first dynamic index.
    pub fn insert(&mut self, name: &[u8], value: &[u8]) -> bool {
        let size = (name.len() + value.len()) as u32 + 32;
        if size + self.used <= self.capacity {
            self.used += size;
            self.dynamics.push_front(
                DynamicHeader::new(name, value)
            );
            true
        }
        else if size > self.capacity {
            self.dynamics.clear();
            self.used = 0;
            false
        } else {
            let mut diff = (size - (self.capacity - self.used)) as i32;
            while diff > 0 {
                let hdr_size = self.dynamics.pop_back().unwrap().size();
                self.used -= hdr_size;
                diff -= hdr_size as i32;
            }
            self.used += size;
            self.dynamics.push_front(
                DynamicHeader::new(name, value)
            );
            true
        }
    }

    /// Look up a header by a client's index value.
    #[inline]
    pub fn header_by_index(&self, idx: usize) -> Option<(&[u8], &[u8])> {
        match idx {
            0 => {
                None
            },
            1...61 => {
                let ref header = self.statics[idx - 1];
                Some((header.name, header.value))
            },
            _ => {
                let dyn_idx = idx - NUMBER_STATIC_HEADERS - 1;
                let dyn_len = self.dynamics.len();
                if dyn_len > 0 && dyn_len > dyn_idx {
                    let ref header = self.dynamics[dyn_idx];
                    Some((header.name(), header.value()))
                } else {
                    None
                }
            }
        }
    }

    /// Look up a header name by a client's index value.
    #[inline]
    pub fn header_name_by_index(&self, idx: usize) -> Option<&[u8]> {
        match idx {
            0 => {
                None
            },
            1...61 => {
                Some(self.statics[idx - 1].name)
            },
            _ => {
                let dyn_idx = idx - NUMBER_STATIC_HEADERS - 1;
                let dyn_len = self.dynamics.len();
                if dyn_len > 0 && dyn_len > dyn_idx {
                    Some(self.dynamics[dyn_idx].name())
                } else {
                    None
                }
            }
        }
    }

    #[inline]
    pub fn get_index(&self, name: &[u8], value: &[u8]) -> u64 {
        let mut res: u64 = (HeaderMatch::NoMatch as u64) << 32;
        'outer: loop {
            for (idx, hdr) in self.statics.iter().enumerate() {
                if name == hdr.name() {
                    if value == hdr.value() {
                        res = (HeaderMatch::ExactMatch as u64) << 32;
                        res |= idx as u64 + 1;
                        break 'outer;
                    } else if res << 32 == 0 {
                        res = (HeaderMatch::PartialMatch as u64) << 32;
                        res |= idx as u64 + 1;
                    }
                }
            }
            for (idx, hdr) in self.dynamics.iter().enumerate() {
                if name == hdr.name() {
                    if value == hdr.value() {
                        res = (HeaderMatch::ExactMatch as u64) << 32;
                        res |= idx as u64 + 62;
                        break 'outer;
                    } else if res << 32 == 0 {
                        res = (HeaderMatch::PartialMatch as u64) << 32;
                        res |= idx as u64 + 62;
                    }
                }
            }
            break;
        }
        res
    }

}


#[cfg(test)]
mod test{
    extern crate test;
    use self::test::Bencher;

    use context::{
        DEFAULT_DYNAMIC_TABLE_SIZE,
        HpackContext,
        HpackEncodable,
        NUMBER_STATIC_HEADERS,
        StaticHeader,
    };


    #[test]
    fn test_header_new() {
        let name = b"name";
        let value = b"value";
        let header = StaticHeader { name: name, value: value };
        assert_eq!(
            header.name,
            name
        );
        assert_eq!(
            header.value,
            value
        );
    }


    #[test]
    fn test_header_size() {
        let name = b"name";
        let value = b"value";
        let header = StaticHeader { name: name, value: value };
        assert_eq!(
            header.size(),
            (name.len() + value.len() + 32) as u32
        );
    }


    #[test]
    fn test_context_header_by_index_none() {
        let headers = HpackContext::new();
        assert!(headers.header_by_index(0).is_none());
        assert!(headers.header_by_index(NUMBER_STATIC_HEADERS + 1).is_none());
    }


    #[test]
    fn test_context_header_by_index_static() {
        let context = HpackContext::new();
        let auth = context.header_by_index(1).unwrap();
        assert_eq!(
            auth.0,
            b":authority"
        );
        assert_eq!(
            auth.1,
            b""
        );
        let status = context.header_by_index(14).unwrap();
        assert_eq!(
            status.0,
            b":status"
        );
        assert_eq!(
            status.1,
            b"500"
        );
        let www = context.header_by_index(61).unwrap();
        assert_eq!(
            www.0,
            b"www-authenticate"
        );
        assert_eq!(
            www.1,
            b""
        );
    }


    #[test]
    fn test_context_header_by_index_dynamic() {
        let mut context = HpackContext::new();
        let name = b"name";
        let value = b"value";
        context.insert(name, value);
        let  hdr = context.header_by_index(NUMBER_STATIC_HEADERS + 1).unwrap();
        assert_eq!(hdr.0, name);
        assert_eq!(hdr.1, value);

    }


    #[test]
    fn test_context_header_name_by_index_none() {
        let context = HpackContext::new();
        assert!(context.header_name_by_index(0).is_none());
        assert!(context.header_name_by_index(NUMBER_STATIC_HEADERS + 1).is_none());
    }


    #[test]
    fn test_context_header_name_by_index_static() {
        let context = HpackContext::new();
        assert_eq!(
            context.header_name_by_index(1).unwrap(),
            b":authority"
        );
    }


    #[test]
    fn test_context_header_name_by_index_dynamic() {
        let mut context = HpackContext::new();
        let name = b"name";
        context.insert(name, b"value");
        let hdr_name = context.header_name_by_index(NUMBER_STATIC_HEADERS + 1).unwrap();
        assert_eq!(hdr_name, name);
    }


    #[test]
    fn test_context_by_resize_up() {
        let mut context = HpackContext::new();
        assert_eq!(context.capacity(), DEFAULT_DYNAMIC_TABLE_SIZE);
        context.set_capacity(10240);
        let _ = context.resize(8192).unwrap();
        assert_eq!(context.capacity(), 8192);
    }


    #[test]
    fn test_context_by_resize_down_0() {
        let mut context = HpackContext::new();
        context.insert(b"name", b"value");
        assert_eq!(context.len(), NUMBER_STATIC_HEADERS + 1);

        let _ = context.resize(0).unwrap();
        assert_eq!(context.capacity(), 0);
        assert_eq!(context.used(), 0);
        assert_eq!(context.len(), NUMBER_STATIC_HEADERS);
    }


    #[test]
    fn test_context_by_resize_down() {
        let mut context = HpackContext::new();
        context.insert(b"name", b"value");
        context.insert(b"eek", b"value");
        assert_eq!(context.len(), NUMBER_STATIC_HEADERS + 2);

        let header_size: u32;
        {
            let header = context.header_by_index(NUMBER_STATIC_HEADERS + 1).unwrap();
            header_size = (header.0.len() + header.1.len()) as u32 + 32;
        }
        let _ = context.resize(header_size).unwrap();
        assert_eq!(context.len(), NUMBER_STATIC_HEADERS + 1);
    }


    #[test]
    fn test_context_dynamic() {
        let mut context = HpackContext::new();
        assert_eq!(context.used(), 0);

        context.insert(b"name", b"value");
        assert_eq!(context.used(), 4 + 5 + 32);
        assert_eq!(context.len(), NUMBER_STATIC_HEADERS + 1);

        let header = context.header_by_index(NUMBER_STATIC_HEADERS + 1).unwrap();
        assert_eq!(header.0, b"name");
        assert_eq!(header.1, b"value");
    }


    #[test]
    fn test_context_insert_clear() {
        let mut context = HpackContext::with_capacity(41);
        assert_eq!(context.used(), 0);

        context.insert(b"name", b"value");
        assert_eq!(context.used(), 4 + 5 + 32);
        assert_eq!(context.len(), NUMBER_STATIC_HEADERS + 1);

        context.insert(b"name", b"longer string");
        assert_eq!(context.used(), 0);
        assert_eq!(context.len(), NUMBER_STATIC_HEADERS);

    }


    #[test]
    fn test_context_get_index_static() {
        let context = HpackContext::new();
        let idx = context.get_index(b"www-authenticate", b"");
        assert_eq!(idx >> 32, 2);
        assert_eq!(idx as u32, 61);
    }


    #[test]
    fn test_context_get_index_dynamic_full() {
        let mut context = HpackContext::new();
        context.insert(b"name", b"value");
        let idx = context.get_index(b"name", b"value");
        assert_eq!(idx >> 32, 2);
        assert_eq!(idx as u32, NUMBER_STATIC_HEADERS as u32 + 1);
    }


    #[test]
    fn test_context_get_index_dynamic_partial() {
        let mut context = HpackContext::new();
        context.insert(b"name", b"value");
        let idx = context.get_index(b"name", b"");
        assert_eq!(idx >> 32, 1);
        assert_eq!(idx as u32, NUMBER_STATIC_HEADERS as u32 + 1);
    }


    #[test]
    fn test_context_get_index_none() {
        let context = HpackContext::new();
        let idx = context.get_index(b"eek", b"value");
        assert_eq!(idx >> 32, 0);
        assert_eq!(idx as u32, 0);
    }


    #[bench]
    fn bench_context_header_by_index_static(b: &mut Bencher) {
        let context = HpackContext::new();
        b.iter(
            || context.header_by_index(1)
        );
    }


    #[bench]
    fn bench_context_header_by_index_dynamic(b: &mut Bencher) {
        let mut context = HpackContext::new();
        context.insert(b"name", b"value");
        b.iter(
            || context.header_by_index(NUMBER_STATIC_HEADERS + 1)
        );
    }


    #[bench]
    fn bench_context_get_index_static(b: &mut Bencher) {
        let context = HpackContext::new();
        b.iter(
            || context.get_index(b"www-authenticate", b"")
        );
    }


    #[bench]
    fn bench_context_get_index_dynamic(b: &mut Bencher) {
        let mut context = HpackContext::new();
        context.insert(b"name", b"value");
        b.iter(
            || context.get_index(b"name", b"value")
        );
    }


    #[bench]
    fn bench_context_insert(b: &mut Bencher) {
        let mut context = HpackContext::new();
        b.iter(
            || context.insert(b"name", b"value")
        );
    }

}
