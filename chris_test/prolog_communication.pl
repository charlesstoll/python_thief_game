:- initialization readfile.

readfile :-
    open('myFile.txt', read, str),
    open('commandsFile.txt', append, cmds), 
    read_string(str, "\t", "\r", End, Lines),
    close(str),
    close(cmds
    write(Lines), 
    halt.

