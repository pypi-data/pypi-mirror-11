"""함수 도입"""
"""num=0"""
def test(movie,indent=False,num=0):
    for the_list in movie:
        if isinstance(the_list,list):
            test(the_list,indent,num+1)

        else:
            if indent:
                for tab in range(num):
                    print("\t", end='')
            print(the_list)
            
