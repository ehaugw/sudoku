from board import Board

board = Board("""
53  7    
6  195   
 98    6 
8   6   3
4  8 3  1
7   2   6
 6    28 
   419  5
    8  79
""")


#  board = Board("""
#           
#    3  7  1
#   8   6 2 
#  3  7 4 8 
#    1  2 7 
#    9    4 
#    6  3  5
#     94    
#  9   6   2
#  """)

board.solve()
board.print()
