def play(unji):
    for a in unji:
        if isinstance(a,list):
            play(a)
        else:
            print(a)
            
