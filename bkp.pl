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
flight(f1).
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
path(f1, bsl, atd, 12).
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

path_to_0(From, To, A, P) :-
    path(A, From, To, P).

path_to_1(From, To, A, X, B, P) :-
    path(A, From, X, P1),
    path(B, X, To, P2),
    P is P1 + P2.

path_to_2(From, To, A, X, B, Y, C, P) :-
    path(A, From, X, P1),
    path(B, X, Y, P2),
    path(C, Y, To, P3),
    From \= Y,
    To \= X,
    P is P1 + P2 + P3.

