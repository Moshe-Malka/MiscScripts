arr = [1,2,3,4,5,6,7,8,9]

""" Clasical answer"""
def chunkify(arr,x):
  out=[]
  p1=0
  p2=x
  while(p1<len(arr)):
    out.append(arr[p1:p2])
    p1+=x
    p2+=x
  return out

""" Generator-Based answer """
def chunks(_list, x):
    for i in range(0, len(_list), x):
        yield _list[i:i + x]


a = chunkify(arr,2)
print chunkify(arr,3)
print next(a)
