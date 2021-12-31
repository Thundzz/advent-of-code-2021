example = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
def parse(pattern):
	stripped = pattern.strip().splitlines()
	H0, H1,H2,H3,H4,H5,H6,H7,H8,H9,HA = stripped[1][1:12]
	A1, B1, C1, D1 = stripped[2][3], stripped[2][5], stripped[2][7], stripped[2][9]
	A2, B2, C2, D2 = stripped[3][3], stripped[3][5], stripped[3][7], stripped[3][9]
	state = {"H0":H0,"H1":H1,"H2":H2,"H3":H3,"H4":H4,"H5":H5,"H6":H6,"H7":H7,"H8":H8,"H9":H9,"HA":HA,"A1":A1,"B1":B1,"C1":C1,"D1":D1,"A2":A2,"B2":B2,"C2":C2,"D2":D2}
	return tuple(sorted([ (k, v) for k, v in state.items() if v != "."]))

example_patterns = [
"""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""",
"""#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########""",
"""#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########""",
"""#############
#.....D.....#
###B#.#C#D###
  #A#B#C#A#
  #########""",
"""#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########""",
"""#############
#.....D.D.A.#
###.#B#C#.###
  #A#B#C#.#
  #########""",
"""#############
#.........A.#
###.#B#C#D###
  #A#B#C#D#
  #########""",
"""#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""
]

for pattern in example_patterns:
	x = parse(pattern)
	print(x)

parsed = parse(
"""#############
#...........#
###C#D#A#B###
  #B#A#D#C#
  #########"""
)
print(parsed)