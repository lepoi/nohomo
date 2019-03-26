airport(atd).
airport(dvr).
airport(mxl).
airport(bsl).
airport(cct).
% --po_def--
name(atd, amsterdam).
name(dvr, denver).
name(mxl, mexicali).
name(bsl, brasilia).
name(cct, calcuta).
% --po_det--
flight(f2).
flight(f3).
flight(f4).
flight(f5).
flight(f6).
flight(f7).
flight(f8).
flight(f9).
flight(f10).
% --fl_def--
path(f2, bsl, atd, 22).
path(f3, cct, atd, 14).
path(f4, cct, atd, 20).
path(f5, dvr, cct, 20).
path(f6, bsl, dvr, 20).
path(f7, dvr, mxl, 22).
path(f8, mxl, dvr, 24).
path(f9, atd, mxl, 26).
path(f10, mxl, atd, 28).
% --fl_det--

path_to_0(From, To, X, P) :-
    path(X, From, To, P),
    From \= To.

path_to_1(From, To, X, A, Y, P) :-
    path_to_0(From, A, X, P1),
    path_to_0(A, To, Y, P2),
    From \= To,
    P is P1 + P2.

path_to_2(From, To, X, A, Y, B, Z, P) :-
    path_to_1(From, B, X, A, Y, P1),
    To \= A,
    path_to_0(B, To, Z, P2),
    From \= To,
    P is P1 + P2.

path_to_3(From, To, W, A, X, B, Y, C, Z, P) :-
    path_to_1(From, B, W, A, X, P1),
    path_to_1(B, To, Y, C, Z, P2),
    A \= C,
    To \= A,
    From \= C,
    From \= To,
    P is P1 + P2.

