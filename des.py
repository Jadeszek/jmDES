__author__ = 'jadeszek'

B_SIZE = 64  # block size

# The 64 bits of the input block to be enciphered are first subjected to the following permutation,
# called the initial permutation IP:

IP = [i - 1 for i in [58, 50, 42, 34, 26, 18, 10, 2,
                      60, 52, 44, 36, 28, 20, 12, 4,
                      62, 54, 46, 38, 30, 22, 14, 6,
                      64, 56, 48, 40, 32, 24, 16, 8,
                      57, 49, 41, 33, 25, 17, 9, 1,
                      59, 51, 43, 35, 27, 19, 11, 3,
                      61, 53, 45, 37, 29, 21, 13, 5,
                      63, 55, 47, 39, 31, 23, 15, 7]
      ]

IP_INV = [i - 1 for i in [40, 8, 48, 16, 56, 24, 64, 32,
                          39, 7, 47, 15, 55, 23, 63, 31,
                          38, 6, 46, 14, 54, 22, 62, 30,
                          37, 5, 45, 13, 53, 21, 61, 29,
                          36, 4, 44, 12, 52, 20, 60, 28,
                          35, 3, 43, 11, 51, 19, 59, 27,
                          34, 2, 42, 10, 50, 18, 58, 26,
                          33, 1, 41, 9, 49, 17, 57, 25]
          ]

# Let E denote a function which takes a block of 32 bits as input and yields a block of 48 bits as
# output. Let E be such that the 48 bits of its output, written as 8 blocks of 6 bits each, are
# obtained by selecting the bits in its inputs in order according to the following table:
E = [i - 1 for i in [32, 1, 2, 3, 4, 5,
                     4, 5, 6, 7, 8, 9,
                     8, 9, 10, 11, 12, 13,
                     12, 13, 14, 15, 16, 17,
                     16, 17, 18, 19, 20, 21,
                     20, 21, 22, 23, 24, 25,
                     24, 25, 26, 27, 28, 29,
                     28, 29, 30, 31, 32, 1]
     ]

S = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]

P = [i - 1 for i in [16, 7, 20, 21,
                     29, 12, 28, 17,
                     1, 15, 23, 26,
                     5, 18, 31, 10,
                     2, 8, 24, 14,
                     32, 27, 3, 9,
                     19, 13, 30, 6,
                     22, 11, 4, 25]
     ]

PC = [
    [i - 1 for i in [57, 49, 41, 33, 25, 17, 9,
                     1, 58, 50, 42, 34, 26, 18,
                     10, 2, 59, 51, 43, 35, 27,
                     19, 11, 3, 60, 52, 44, 36,
                     63, 55, 47, 39, 31, 23, 15,
                     7, 62, 54, 46, 38, 30, 22,
                     14, 6, 61, 53, 45, 37, 29,
                     21, 13, 5, 28, 20, 12, 4]
     ],
    [i - 1 for i in [14, 17, 11, 24, 1, 5,
                     3, 28, 15, 6, 21, 10,
                     23, 19, 12, 4, 26, 8,
                     16, 7, 27, 20, 13, 2,
                     41, 52, 31, 37, 47, 55,
                     30, 40, 51, 45, 33, 48,
                     44, 49, 39, 56, 34, 53,
                     46, 42, 50, 36, 29, 32
                     ]
     ]
]

KEY_SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def apply_permutation(byte_block, perm):
    result = [0] * len(perm)
    i = 0
    for p in perm:
        result[i] = byte_block[p]
        i += 1
    return result


def init(byte_block):
    apply_permutation(byte_block, IP)


def split_block(byte_block):
    half = len(byte_block) / 2
    return [byte_block[:half], byte_block[half + 1:]]


def left_shift(block, step):
    return block[-step:] + block[:-step]


def right_shift(block, step):
    return left_shift(block, -step)


def generate_key(base_key, iter):  # key in byte form
    permuted = apply_permutation(base_key, PC[0])
    split = split_block(permuted)
    shifted = left_shift(split[0], KEY_SHIFT[iter]) + left_shift(split[1], KEY_SHIFT[iter])
    final = apply_permutation(shifted, PC[1])
    return final


def dec2bin(decimal):
    return [int(d) for d in bin(decimal)[2:]]


def bin2dec(bin_list):
    return int(reduce(lambda x, y: str(x) + str(y), bin_list), 2)


def get_sbox_coordinates(six_byte_chunk):
    row_bin = [six_byte_chunk[0]] + [six_byte_chunk[-1]]
    column_bin = six_byte_chunk[1:-1]

    print(row_bin, column_bin)
    return bin2dec(row_bin), bin2dec(column_bin)


def apply_sbox(chunk, sbox):
    row, col = get_sbox_coordinates(chunk)
    number = sbox[row * 16 + col]
    return dec2bin(number)


def f(right_block, key, iter):
    permuted = apply_permutation(right_block, E)
    print('permuted', permuted)
    key_48bit = generate_key(key, iter)
    print('key48', key_48bit)
    assert len(permuted) != len(key_48bit)

    xored = [p ^ k for p, k in zip(permuted, key_48bit)]
    print('xored', xored)
    six_byte_chunks = [xored[i:i + 6] for i in range(0, len(xored), 6)]
    print('six_byte_chunks ', six_byte_chunks )
    sbox_out = [apply_sbox(chunk, sbox) for chunk, sbox in zip(six_byte_chunks, S)]
    print('sbox_out', sbox_out )

    return apply_permutation(sbox_out, )


test = [0, 0, 0, 1, 0, 1, 1, 0,
        1, 0, 1, 1, 1, 1, 0, 1,
        0, 1, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 1, 0, 1, 0, 0,
        1, 0, 1, 1, 0, 1, 0, 0,
        0, 1, 0, 1, 0, 0, 1, 1,
        1, 0, 0, 0, 1, 0, 1, 0,
        0, 1, 1, 1, 1, 0, 1, 0, ]


def DES(block, key):
    permuted = init(block)
    print(permuted)
    split = split_block(permuted)
    print(split)


s = get_sbox_coordinates([1, 1, 1, 1, 1, 1])
decimal = 19
print( [int(x) for x in bin(decimal)[2:]])

print(s[0], s[1])
# print(left_shift([1, 2, 3, 4, 5, 6], 3))

# DES(test, [0, 1, 1, 1, 1, 0])


























