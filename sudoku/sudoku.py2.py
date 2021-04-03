
import copy

def list_add_one(set_of_number):
    return [x+1 for x in list(set_of_number)]

def torow(block,order):
    return (block//3)*3+order//3

def tocolumn(block,order):
    return (block%3)*3+order%3

def toblock(row,column):
    return (row//3)*3+column//3

def toorder(row,column):
    return (row%3)*3+column%3

def findsubset(initial_set_vector):
    initial_set_union=set()
    remain_index_set=set()
    for index in range(len(initial_set_vector)):
        if len(initial_set_vector[index])!=0:
            initial_set_union.update(initial_set_vector[index])
            remain_index_set.add(index)
    initial_element_size=len(initial_set_union)
    if initial_element_size==1:
        current_index=remain_index_set.pop()
        return set([current_index]),initial_set_vector[current_index]
    current_index_set=set()
    current_element_set=set()
    return findsubset_recursive(\
                      initial_set_vector,\
                      initial_element_size,\
                      current_index_set,\
                      current_element_set,\
                      remain_index_set)

def findsubset_recursive(\
               initial_set_vector,\
               initial_element_size,\
               current_index_set,\
               current_element_set,\
               remain_index_set):
    if len(remain_index_set)==0:
        return (None,None)
    while True:
        while len(remain_index_set)!=0:
            current_index=remain_index_set.pop()
            if len(current_element_set.union(initial_set_vector[current_index]))==initial_element_size:
                continue
            next_index_set=copy.deepcopy(current_index_set)
            next_index_set.add(current_index)
            next_element_set=copy.deepcopy(current_element_set)
            next_element_set.update(initial_set_vector[current_index])
            if len(next_element_set)==len(next_index_set):
                return (next_index_set,next_element_set)
            next_remain_index_set=copy.deepcopy(remain_index_set)
            result_index_set,result_element_set=\
                findsubset_recursive(\
                           initial_set_vector,\
                           initial_element_size,\
                           next_index_set,\
                           next_element_set,\
                           next_remain_index_set)
            if result_index_set!=None and result_element_set!=None:
                return result_index_set,result_element_set
        else:
            return (None,None)

class sudoku:
    def __init__(self,initial_board=None,solution_number_limit=10):
        if type(initial_board)==type([]):
            self.board=initial_board
        elif type(initial_board)==type("0"):
            self.board=[]
            for line in initial_board.split('\n'):
                if len(self.board)>=9: break
                self.board.append([])
                for ch in line:
                    if ch.isdigit():
                        if len(self.board[-1])==9:
                            self.board.append([])
                        self.board[-1].append(int(ch))
                    if ch==",":
                        while len(self.board[-1])<9:
                            self.board[-1].append(0)
            while len(self.board[-1])<9:
                self.board[-1].append(0)
        else:
            self.board=[]
            while len(self.board)<9:
                line=raw_input("please input row %d: "%(len(self.board)+1))
                self.board.append([])
                for ch in line:
                    if ch.isdigit():
                        if len(self.board[-1])==9:
                            self.board.append([])
                        self.board[-1].append(int(ch))
                    if ch==",":
                        while len(self.board[-1])<9:
                            self.board[-1].append(0)
            while len(self.board[-1])<9:
                self.board[-1].append(0)
        self.solution_number_limit=solution_number_limit

    def print_board(self,show_candidate=False):
        boardstring=""
        for i in range(9):
            print "row", i+1, ":    ",
            for j in range(9):
                number=self.board[i][j]
                boardstring+=str(number)
                gridij=""
                if number==0:
                    if show_candidate==True:
                        for k in range(9):
                            if k+1 in self.candidate[i][j]: gridij+=str(k+1)
                            else: gridij+="-"
                    else: gridij="-"
                else:
                    if show_candidate:
                        gridij=str(number)*9
                    else: gridij=str(number)
                print gridij,
                if j==2 or j==5: print "  ",
            print
            if i==2 or i==5 or i==8: print
            if i!=8: boardstring+=" "
            else: boardstring+="\n"
        print "board :    ", boardstring

    def update_all(self,i,j,number):
        self.candidate[i][j].clear()
        for k in range(9):
            self.candidate[i][k].discard(number)
            self.candidate[k][j].discard(number)
            b=toblock(i,j)
            self.candidate[torow(b,k)][tocolumn(b,k)].discard(number)
        #print "Update board by (%d,%d) using %d" % (i,j,number)

    def update_row_by_subset(self,row,column_set,candidate_set):
        dosomething = False
        for column in range(9):
            if column not in column_set:
                length=len(self.candidate[row][column])
                self.candidate[row][column].difference_update(candidate_set)
                if length!=len(self.candidate[row][column]):
                    dosomething = True
        #if dosomething: print "Update row %d by subset %s using %s" % (row,list_add_one(column_set),list_add_one(candidate_set))
        return dosomething

    def update_row_set_by_column_set(self,row_set,column_set,thecandidate):
        dosomething = False
        for row in row_set:
            for column in range(9):
                if column not in column_set:
                    length=len(self.candidate[row][column])
                    self.candidate[row][column].discard(thecandidate)
                    if length!=len(self.candidate[row][column]):
                        dosomething = True
        if dosomething: print "Update row set %s by column set %s using %d" % (list_add_one(row_set),list_add_one(column_set),thecandidate)
        return dosomething

    def update_row_by_block(self,row,theblock,thecandidate):
        dosomething = False
        for column in range(9):
            if toblock(row,column)!=theblock:
                length=len(self.candidate[row][column])
                self.candidate[row][column].discard(thecandidate)
                if length!=len(self.candidate[row][column]):
                    dosomething = True
        #if dosomething: print "Update row %d by block %d using %s" % (row,theblock,thecandidate)
        return dosomething

    def update_column_by_subset(self,column,row_set,candidate_set):
        dosomething = False
        for row in range(9):
            if row not in row_set:
                length=len(self.candidate[row][column])
                self.candidate[row][column].difference_update(candidate_set)
                if length!=len(self.candidate[row][column]):
                    dosomething = True
        #if dosomething: print "Update column %d by subset %s using %s" % (column,list_add_one(row_set),list_add_one(candidate_set))
        return dosomething

    def update_column_set_by_row_set(self,column_set,row_set,thecandidate):
        dosomething = False
        for column in column_set:
            for row in range(9):
                if row not in row_set:
                    length=len(self.candidate[row][column])
                    self.candidate[row][column].discard(thecandidate)
                    if length!=len(self.candidate[row][column]):
                        dosomething = True
        if dosomething: print "Update column set %s by row set %s using %d" % (list_add_one(column_set),list_add_one(row_set),thecandidate)
        return dosomething

    def update_column_by_block(self,column,theblock,thecandidate):
        dosomething = False
        for row in range(9):
            if toblock(row,column)!=theblock:
                length=len(self.candidate[row][column])
                self.candidate[row][column].discard(thecandidate)
                if length!=len(self.candidate[row][column]):
                    dosomething = True
        #if dosomething: print "Update column %d by block %d using %s" % (column,theblock,thecandidate)
        return dosomething

    def update_block_by_subset(self,block,order_set,candidate_set):
        dosomething = False
        for order in range(9):
            row=torow(block,order)
            column=tocolumn(block,order)
            if order not in order_set:
                length=len(self.candidate[row][column])
                self.candidate[row][column].difference_update(candidate_set)
                if length!=len(self.candidate[row][column]):
                    dosomething = True
        #if dosomething: print "Update block %d by subset %s using %s" % (block,list_add_one(order_set),list_add_one(candidate_set))
        return dosomething

    def update_block_by_row(self,block,therow,thecandidate):
        dosomething = False
        for order in range(9):
            row=torow(block,order)
            column=tocolumn(block,order)
            if row!=therow:
                length=len(self.candidate[row][column])
                self.candidate[row][column].discard(thecandidate)
                if length!=len(self.candidate[row][column]):
                    dosomething = True
        #if dosomething: print "Update block %d by row %d using %s" % (block,therow,thecandidate)
        return dosomething

    def update_block_by_column(self,block,thecolumn,thecandidate):
        dosomething = False
        for order in range(9):
            row=torow(block,order)
            column=tocolumn(block,order)
            if column!=thecolumn:
                length=len(self.candidate[row][column])
                self.candidate[row][column].discard(thecandidate)
                if length!=len(self.candidate[row][column]):
                    dosomething = True
        #if dosomething: print "Update block %d by column %d using %s" % (block,thecolumn,thecandidate)
        return dosomething

    def solve_forward(self):
        while True:
            donothing=True
            # check single candidate
            for i in range(9):
                for j in range(9):
                    if self.board[i][j]==0:
                        if len(self.candidate[i][j])==0:
                            return -1;
                        if len(self.candidate[i][j])==1:
                            self.board[i][j]=self.candidate[i][j].pop()
                            self.update_all(i,j,self.board[i][j])
                            self.unresolved-=1
                            donothing=False
            # update block by row
            if donothing==True and self.unresolved!=0:
                for row in range(9):
                    for number in range(1,10):
                        row_block_set=set()
                        for column in range(9):
                            if number in self.candidate[row][column]:
                                row_block_set.add(toblock(row,column))
                        if len(row_block_set)==1:
                            if self.update_block_by_row(row_block_set.pop(),row,number):
                                donothing=False
            # update block by column
            if donothing==True and self.unresolved!=0:
                for column in range(9):
                    for number in range(1,10):
                        column_block_set=set()
                        for row in range(9):
                            if number in self.candidate[row][column]:
                                column_block_set.add(toblock(row,column))
                        if len(column_block_set)==1:
                            if self.update_block_by_column(column_block_set.pop(),column,number):
                                donothing=False
            # update row or column by block
            if donothing==True and self.unresolved!=0:
                for block in range(9):
                    for number in range(1,10):
                        block_row_set=set()
                        block_column_set=set()
                        for order in range(9):
                            row=torow(block,order)
                            column=tocolumn(block,order)
                            if number in self.candidate[row][column]:
                                block_row_set.add(row)
                                block_column_set.add(column)
                        if len(block_row_set)==1:
                            if self.update_row_by_block(block_row_set.pop(),block,number):
                                donothing=False
                        if len(block_column_set)==1:
                            if self.update_column_by_block(block_column_set.pop(),block,number):
                                donothing=False
            # update row by subset
            if donothing==True and self.unresolved!=0:
                for row in range(9):
                    row_candidate_set_vector=[]
                    for column in range(9):
                        row_candidate_set_vector.append(self.candidate[row][column])
                    row_result_index_set,row_result_candidate_set=\
                        findsubset(row_candidate_set_vector)
                    if row_result_index_set!=None and row_result_candidate_set!=None:
                        if self.update_row_by_subset(row,row_result_index_set,row_result_candidate_set):
                            donothing = False
                            break
            # update column by subset
            if donothing==True and self.unresolved!=0:
                for column in range(9):
                    column_candidate_set_vector=[]
                    for row in range(9):
                        column_candidate_set_vector.append(self.candidate[row][column])
                    column_result_index_set,column_result_candidate_set=\
                            findsubset(column_candidate_set_vector)
                    if column_result_index_set!=None and column_result_candidate_set!=None:
                        if self.update_column_by_subset(column,column_result_index_set,column_result_candidate_set):
                            donothing=False
                            break
            # update block by subset
            if donothing==True and self.unresolved!=0:
                for block in range(9):
                    block_candidate_set_vector=[]
                    for order in range(9):
                        row=torow(block,order)
                        column=tocolumn(block,order)
                        block_candidate_set_vector.append(self.candidate[row][column])
                    block_result_index_set,block_result_candidate_set=\
                            findsubset(block_candidate_set_vector)
                    if block_result_index_set!=None and block_result_candidate_set!=None:
                        if self.update_block_by_subset(block,block_result_index_set,block_result_candidate_set):
                            donothing=False
                            break
            # update row or column by number
            if donothing==True and self.unresolved!=0:
                for number in range(1,10):
                    number_column_set_on_row=[set() for x in range(9)]
                    number_row_set_on_column=[set() for x in range(9)]
                    number_column_set=set()
                    number_row_set=set()
                    for row in range(9):
                        for column in range(9):
                            if number in self.candidate[row][column]:
                                number_column_set_on_row[row].add(column)
                                number_row_set_on_column[column].add(row)
                                number_column_set.add(column)
                                number_row_set.add(row)
                    number_unresolved=len(number_row_set)
                    if number_unresolved < 4:
                        continue
                    number_result_row_set_on_row,number_result_column_set_on_row=\
                        findsubset(number_column_set_on_row)
                    if number_result_column_set_on_row!=None and number_result_row_set_on_row!=None:
                        if self.update_column_set_by_row_set(number_result_column_set_on_row,number_result_row_set_on_row,number):
                            donothing=False
                    number_result_column_set_on_column,number_result_row_set_on_column=\
                        findsubset(number_row_set_on_column)
                    if number_result_row_set_on_column!=None and number_result_column_set_on_column!=None:
                        if self.update_row_set_by_column_set(number_result_row_set_on_column,number_result_column_set_on_column,number):
                            donothing=False
            if self.unresolved==0 or donothing==True:
                return self.unresolved

    def solve_recursive(self):
        unresolved=self.solve_forward()
        #self.print_board(True)
        if unresolved==-1:
            if self.solution_number_limit<=0 or self.solution_number < self.solution_number_limit:
                print "Fail!"
            return -1
        if unresolved==0:
            self.solution_number +=1
            if self.solution_number_limit<=0 or self.solution_number <= self.solution_number_limit:
                print "Success!"
                self.print_board()
            return -1

        found=False;
        for row in range(9):
            for column in range(9):
                if self.board[row][column]==0:
                    found=True;
                    break;
            if found:
                break;

        for thecandidate in self.candidate[row][column]:
            if self.solution_number_limit<=0 or self.solution_number < self.solution_number_limit:
                print "Try: [%d,%d]=%d"%(row+1,column+1,thecandidate)
            newself = copy.deepcopy(self)
            newself.candidate[row][column]=set([thecandidate])
            newunresolved = newself.solve_recursive()
            self.solution_number = newself.solution_number
            if (self.solution_number_limit>0 and self.solution_number>=self.solution_number_limit):
                break;
        return

    def solve(self):
        # check valid and initial check vector
        self.check_row=[]
        self.check_column=[]
        self.check_block=[]
        for i in range(9):
            self.check_row.append(set())
            self.check_column.append(set())
            self.check_block.append(set())
            for j in range(9):
                for (check_i,check_j,check_set) in \
                    ((i,j,self.check_row[i]),(j,i,self.check_column[i]),(torow(i,j),tocolumn(i,j),self.check_block[i])):
                    element=self.board[check_i][check_j]
                    if element!=0 and element in check_set:
                        SudokuError="SudokuError"
                        raise SudokuError
                    elif element!=0:
                        check_set.add(element)

        self.candidate=[]
        self.unresolved=0
        # initial candidate and unresolved
        for i in range(9):
            self.candidate.append([])
            for j in range(9):
                if self.board[i][j]==0:
                    self.candidate[i].append(set(range(1,10))-self.check_row[i]-self.check_column[j]-self.check_block[toblock(i,j)])
                    self.unresolved+=1
                else:
                    self.candidate[i].append(set())

        print "input:"
        self.print_board()

        # main loop
        self.solution_number=0
        # self.solution_number_limit=0
        self.solve_recursive()
        if self.solution_number >0:
            print "solution number = ",self.solution_number
            if self.solution_number==self.solution_number_limit:
                print "more solutions may be cut off..."
        else:
            print "Fail!"
            self.print_board(True)
            print "unresolved =",self.unresolved
        print

if __name__ == "__main__":
    sudoku1=sudoku(\
           [[6,0,0,3,1,0,0,4,0],\
            [0,0,1,0,0,0,0,7,5],\
            [7,4,2,0,5,0,0,0,0],\
            [0,7,4,5,0,0,2,0,9],\
            [0,0,9,7,0,4,5,3,1],\
            [0,0,0,0,0,1,0,6,0],\
            [4,8,6,2,7,0,1,0,0],\
            [3,0,5,0,0,6,7,0,4],\
            [0,0,7,4,3,9,0,5,8]])
    sudoku2=sudoku("794386020638000749215947836,073600098,900803467,08607901,80976005,30009867,067030984")
    sudoku3=sudoku("000500260305000004090001000020040600000012005900830000000700100800000047057009000")
    sudoku4=sudoku("600000017 400001600 001000000 000010970 310800064 062004001 108097046 000000100 200100705")
    sudoku6=sudoku("00007619,972158463,061040507,59000267,70800523,006700045,600007004,00003075,00700031")
    sudoku7=sudoku("0204007,006709,080002006,230000095,0,090000017,010205048,5020043,0083")
    sudoku8=sudoku("10000709,030020008,0096005,0053009,010080002,600004,30000001,041000007,0070003") # very hard
    sudoku9=sudoku("000000039,000001005,0030508,008090006,070002,1004,00908005,0200006,4007") # very hard
    sudoku0=sudoku("070000004,60000009,0080031,0000153,000302,00586,0015002,090000006,40000007") # extremely hard
    sudokua=sudoku("0007008,00004003,000009001,6005,01003004,005001007,5002006,03008009,007000002") # very hard
    sudokub=sudoku("0900817,0000008,800007012,207,000506,000000903,580300004,001,00480006") # hard
    sudokuc=sudoku("100000089,000009002,00000045,0076,03004,900002005,00407,50000801,0603") # hard
    sudoku7.solve()
