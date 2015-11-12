function f = fu(u,a,c1)
c0 = -0.5*u -1.5*c1;
if u<0.5
    f = a*u;
elseif 0.5 <= u && u < 1.5
    f = a*(1-u);
elseif u >= 1.5
    f = c0 + c1*u;
end
end