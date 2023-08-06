// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.


typedef struct {
    uint8_t *name;
    size_t name_len;
    uint8_t *value;
    size_t value_len;
    bool compressable;
} nahpack_header;


typedef struct {
    void *values;
    size_t len;
    size_t cap;
} nahpack_vec;


typedef struct {
    void *slice;
    size_t len;
} nahpack_slice;


typedef struct {
    nahpack_vec *decoded;
    void *slice;
    void *buffer;
} nahpack_headers;


void *nahpack_context_new();


void nahpack_context_free(void *context);


void nahpack_set_context_capacity(void *context, uint32_t size);


nahpack_headers * nahpack_headers_new(uint8_t *block, size_t block_len);


void nahpack_headers_free(nahpack_headers *headers);


nahpack_header * nahpack_get_header(nahpack_headers *headers, size_t index);


ssize_t nahpack_decode_block(void *context, nahpack_headers *headers);


// callback must have a signature of:
// void fn(void *passthrough_ptr, uint8_t *const block, size_t len);
// the block will be deallocated after the function returns
ssize_t nahpack_encode_block(
    nahpack_header *block,
    size_t block_len,
    void *context,
    void *callback,
    void *passthrough_ptr
);
