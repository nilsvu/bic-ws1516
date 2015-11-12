close all
clear all
clc

a = 15/8;
b = 3/2;
I = 0;

u = linspace(-1.5,3,20000);

w1 = u - u^3/3 + I;
w2 = a + b*u;

figure
hold on
grid on
plot(u,w1,'b','linewidth',2)
plot(u,w2,'r','linewidth',2)