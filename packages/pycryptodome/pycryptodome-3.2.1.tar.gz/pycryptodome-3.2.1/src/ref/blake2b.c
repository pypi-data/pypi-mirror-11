   // A simple BLAKE2b Reference Implementation

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

   #include "blake2b.h"

   // cyclic right rotation

   #ifndef ROTR64
   #define ROTR64(x, y)  (((x) >> (y)) ^ ((x) << (64 - (y))))
   #endif

   // little-endian byte access

   #define B2B_GET64(p)                            \
       (((uint64_t) ((uint8_t *) (p))[0]) ^        \
       (((uint64_t) ((uint8_t *) (p))[1]) << 8) ^  \
       (((uint64_t) ((uint8_t *) (p))[2]) << 16) ^ \
       (((uint64_t) ((uint8_t *) (p))[3]) << 24) ^ \
       (((uint64_t) ((uint8_t *) (p))[4]) << 32) ^ \
       (((uint64_t) ((uint8_t *) (p))[5]) << 40) ^ \
       (((uint64_t) ((uint8_t *) (p))[6]) << 48) ^ \
       (((uint64_t) ((uint8_t *) (p))[7]) << 56))

   // G Mixing function

   #define B2B_G(a, b, c, d, x, y) {   \
       v[a] = v[a] + v[b] + x;         \
       print_state(v); \
       v[d] = ROTR64(v[d] ^ v[a], 32); \
       v[c] = v[c] + v[d];             \
       v[b] = ROTR64(v[b] ^ v[c], 24); \
       v[a] = v[a] + v[b] + y;         \
       v[d] = ROTR64(v[d] ^ v[a], 16); \
       v[c] = v[c] + v[d];             \
       v[b] = ROTR64(v[b] ^ v[c], 63); }


void print_state(uint64_t s[16])
{
    int i;
    printf("======\n");
    for (i=0; i<16; i++)
        printf("%016llx\n", s[i]);
}

   // Initialization Vector

   static const uint64_t blake2b_iv[8] = {
       0x6A09E667F3BCC908, 0xBB67AE8584CAA73B,
       0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1,
       0x510E527FADE682D1, 0x9B05688C2B3E6C1F,
       0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179
   };

   // Compression function. "last" flag indicates last block.

   static void blake2b_compress(blake2b_ctx *ctx, int last)
   {
       const uint8_t sigma[12][16] = {
           { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 },
           { 14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3 },
           { 11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4 },
           { 7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8 },
           { 9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13 },
           { 2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9 },
           { 12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11 },
           { 13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10 },
           { 6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5 },
           { 10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0 },
           { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 },
           { 14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3 }
       };
       int i;
       uint64_t v[16], m[16];

       for (i = 0; i < 8; i++) {           // init work variables
           v[i] = ctx->h[i];
           v[i + 8] = blake2b_iv[i];
       }

       v[12] ^= ctx->t[0];                 // low 64 bits of offset
       v[13] ^= ctx->t[1];                 // high 64 bits
       if (last)                           // last block flag set ?
           v[14] = ~v[14];


       for (i = 0; i < 16; i++)            // get little-endian words
           m[i] = B2B_GET64(&ctx->b[8 * i]);

        print_state(v);

       for (i = 0; i < 12; i++) {          // twelve rounds
           B2B_G( 0, 4,  8, 12, m[sigma[i][ 0]], m[sigma[i][ 1]]);
           B2B_G( 1, 5,  9, 13, m[sigma[i][ 2]], m[sigma[i][ 3]]);
           B2B_G( 2, 6, 10, 14, m[sigma[i][ 4]], m[sigma[i][ 5]]);
           B2B_G( 3, 7, 11, 15, m[sigma[i][ 6]], m[sigma[i][ 7]]);
           B2B_G( 0, 5, 10, 15, m[sigma[i][ 8]], m[sigma[i][ 9]]);
           B2B_G( 1, 6, 11, 12, m[sigma[i][10]], m[sigma[i][11]]);
           B2B_G( 2, 7,  8, 13, m[sigma[i][12]], m[sigma[i][13]]);
           B2B_G( 3, 4,  9, 14, m[sigma[i][14]], m[sigma[i][15]]);

       }

       for( i = 0; i < 8; ++i )
           ctx->h[i] ^= v[i] ^ v[i + 8];
   }

   // Initialize the state. key is optional

   int blake2b_init(blake2b_ctx *ctx, size_t outlen,
       const void *key, size_t keylen)     // (keylen=0: no key)
   {
       size_t i;

       if (outlen == 0 || outlen > 64 || keylen > 64)
           return -1;                      // illegal parameters

       for (i = 0; i < 8; i++)             // state, "param block"
           ctx->h[i] = blake2b_iv[i];
       ctx->h[0] ^= 0x01010000 ^ (keylen << 8) ^ outlen;

       ctx->t[0] = 0;                      // input count low word
       ctx->t[1] = 0;                      // input count high word
       ctx->c = 0;                         // pointer within buffer
       ctx->outlen = outlen;

       for (i = keylen; i < 128; i++)      // zero input block
           ctx->b[i] = 0;
       if (keylen > 0) {
           blake2b_update(ctx, key, keylen);
           ctx->c = 128;                   // at the end
       }

       return 0;
   }

   // update with new data

   void blake2b_update(blake2b_ctx *ctx,
       const void *in, size_t inlen)       // data bytes
   {
       size_t i;

       for (i = 0; i < inlen; i++) {
           if (ctx->c == 128) {            // buffer full ?
               ctx->t[0] += ctx->c;        // add counters
               if (ctx->t[0] < ctx->c)     // carry overflow ?
                   ctx->t[1]++;            // high word
               blake2b_compress(ctx, 0);   // compress (not last)
               ctx->c = 0;                 // counter to zero
           }
           ctx->b[ctx->c++] = ((const uint8_t *) in)[i];
       }
   }

   // finalize

   void blake2b_final(blake2b_ctx *ctx, void *out)
   {
       size_t i;

       ctx->t[0] += ctx->c;                // mark last block offset
       if (ctx->t[0] < ctx->c)             // carry overflow
           ctx->t[1]++;                    // high word

       while (ctx->c < 128)                // fill up with zeros
           ctx->b[ctx->c++] = 0;
       blake2b_compress(ctx, 1);           // final block flag = 1

       // little endian convert and store
       for (i = 0; i < ctx->outlen; i++) {
           ((uint8_t *) out)[i] =
               (ctx->h[i >> 3] >> (8 * (i & 7))) & 0xFF;
       }
   }

   // convenience function for all-in-one computation

   int blake2b(void *out, size_t outlen,
       const void *key, size_t keylen,
       const void *in, size_t inlen)
   {
       blake2b_ctx ctx;

       if (blake2b_init(&ctx, outlen, key, keylen))
           return -1;
       blake2b_update(&ctx, in, inlen);
       blake2b_final(&ctx, out);

       return 0;
   }

const uint8_t key_hex[] = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f";

static uint8_t hex_to_bin_c(uint8_t c)
{
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    return 0;
}

static void bin_to_hex_c(uint8_t in, uint8_t out[2])
{
    int i;

    for (i=1; i>=0; i--) {
        uint8_t digit;

        digit = (in >> (4*(1-i))) & 15;
        assert(digit<16);
        if (digit<10)
            out[i] = digit + '0';
        else
            out[i] = digit - 10 + 'a';
    }
}

struct swlen {
    uint8_t* s;
    unsigned len;
};

static struct swlen hex_to_bin_s(const uint8_t *hex_s)
{
    size_t hex_len;
    uint8_t* out;
    unsigned i;
    struct swlen string_out;

    hex_len = strlen((const char*)hex_s);
    assert(hex_len % 2 == 0);

    out = calloc(1, hex_len/2);
    for (i=0; i<hex_len/2; i++) {
        out[i] = hex_to_bin_c(hex_s[2*i]) * 16;
        out[i] |= hex_to_bin_c(hex_s[2*i+1]);
    }

    string_out.s = out;
    string_out.len = hex_len / 2;

    return string_out;
}

static void print_bin(const uint8_t *p, size_t len)
{
    for (; len!=0; len--, p++) {
        uint8_t byte[2];
        bin_to_hex_c(*p, byte);
        printf("%c%c", byte[0], byte[1]);
    }
    printf("\n");
}

int main(void)
{
    struct swlen key_bin;
    uint8_t digest[64];
    int res;

    key_bin = hex_to_bin_s(key_hex);
    print_bin(key_bin.s, key_bin.len);

    blake2b(digest, 64, key_bin.s, key_bin.len, NULL, 0);

    print_bin(digest, 64);
    return 0;
}
