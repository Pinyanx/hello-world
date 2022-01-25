function x = hwk2p3(x0,c)

x = x0
c = c
k = 0
f = func(x,c)
g = grad(x,c)
c1 = 1e-4
ro = 0.8

while (norm(grad(x,c)) > 1e-7) || (k == 1000)
    d = -g %steepest descent direction
    alpha = 1;
    newfunc = func(x+alpha*d,c);
    while (newfunc > f + c1*alpha*dot(g,d))
        alpha = alpha*ro;
        newfunc = func(x+alpha*d,c);
    end
    x = x+alpha*d;
    f = newfunc;
    g = grad(x,c);
    k = k+1
end

x = x