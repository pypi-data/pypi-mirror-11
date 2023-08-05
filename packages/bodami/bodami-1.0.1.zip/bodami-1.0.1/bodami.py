def test(movie,num):
    for the_list in movie:
        if isinstance(the_list,list):
            test(the_list,num+1)
        else:
            for tab in range(num):
                print("\t", end='')
            print(the_list)
            
