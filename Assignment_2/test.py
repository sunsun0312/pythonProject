from tangram import *
# file = open('tangram_A_1_b.xml')
# coloured_pieces = available_coloured_pieces(file)
# print(are_valid(coloured_pieces))


file = open('pieces_A.xml')
coloured_pieces_1 = available_coloured_pieces(file)
file = open('pieces_AA.xml')
coloured_pieces_2 = available_coloured_pieces(file)
print(are_identical_sets_of_coloured_pieces(coloured_pieces_1, coloured_pieces_2))



# file = open('./test/_Shape_A_1.xml')
# shape = available_coloured_pieces(file)
# file = open('./test/_Tangram_A_1_a.xml')
# tangram = available_coloured_pieces(file)
# print(is_solution(tangram, shape))

#print(available_coloured_pieces)