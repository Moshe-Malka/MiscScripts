# mat =   [ [1,2,3],
#           [45,66,90],
#           [100,101,110],
#           [200,345,400],
#           [777,888,999],
#         ]

# mat = [
#     [1,2,3,4],
#     [5,6,7,8],
#     [9,10,11,12]
#     ]

mat = [ [3,10,34,50],
        [100,132,500,504],
        [150,153,502,700] ]


def matFind(mat, val):
    max_row_len = len(mat)-1
    max_col_len = len(mat[0])-1
    print "Dim: {}:{}".format(len(mat), len(mat[0]))
    i=0
    j=0
    maxIterations = len(mat) * len(mat[0])
    counter = 0
    last = None
    while(counter < maxIterations):
        counter+=1
        # check that we do not get stuck on same value. OR that the value exists.
        if mat[i][j] == last or last > val:
            break
        last =  mat[i][j]
        print "Itiration {} => {}".format(counter, mat[i][j])
        if mat[i][j] == val:
            print "Found it! [{}][{}] => {}".format(i, j, mat[i][j])
            break
        if j<max_col_len:
            if i<max_row_len:       # not in last row
                if (mat[i+1][j] < val and mat[i][j+1] < val):                 
                    i+=1
                    j+=1
                else:
                    if mat[i+1][j] == val:
                        print "Found it! [{}][{}] => {}".format(i+1, j, mat[i+1][j])
                        break
                    elif mat[i][j+1] == val:
                        print "Found it! [{}][{}] => {}".format(i+1, j, mat[i][j+1])
                        break
                    elif mat[i+1][j] > val:
                        j+=1
                    elif mat[i][j+1] > val:
                        i+=1
                    
            else:       # in last row
                if mat[i][j+1] == val:
                    print "Found it! [{}][{}] => {}".format(i+1, j, mat[i][j+1])
                    break
        else:
            if i==max_row_len:      # in last row
                j+=1
            if j==max_col_len:      # last column
                j=0
                i+=1               


matFind(mat, 153)