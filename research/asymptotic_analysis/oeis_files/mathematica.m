
nMax = 20;
s = 2;
A[0] = 1;
Do[
  A[t] = Expand[
    (A[t - 1] /. n -> t) +
    Integrate[s t (A[t - 1] /. n -> u), {u, t, n}]
  ],
  {t, 1, nMax}
];
Flatten[Table[A[t] /. n -> k, {k, 1, nMax}, {t, 1, k}]]
