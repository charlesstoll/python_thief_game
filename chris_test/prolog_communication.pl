:- initialization readfile.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Defining the game board          %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


neimat(10, 11, 21).
neimatl(11, 10, 12, 00).
neimat(12, 11, 23).
neimat(20, 23, 31).
neimatl(21, 20, 10, 22).
neimatl(22, 23, 33, 21).
neimatl(23, 12, 22, 24).
neimat(24, 35, 23).
neimatl(31, 30, 20, 32).
neimat(32, 31, 33).
neimatl(33, 32, 34, 22).
neimat(34, 33, 35).
neimatl(35, 34, 24, 36).

% are_neighbors(X, _, _,_) :-

readfile :-
    open('myFile.txt', read, str),
    % open('myFile.txt', append, neighs), 
    read_string(str, "\t", "\r", End, Lines),
    % find_neighbors(Lines),
    close(str),
    % close(neighs),
    write(Lines), 
    halt.

% find_neighbors(loc) :-
	
