close all
clear all
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% I. DEFINE PARAMETERS

% Euler integration
h = 10e-5; % step size parameter
time = 500; % simulation time
t = 0:h:time; % generate time vector

% model
a = 15/8;
b = 3/2;
epsilon = 0.1;
I = 0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% II. CALCULATE NULLCLINES

u0 = linspace(-3,3,20000);

w1 = u0 - u0.^3/3 + I; % calculate u nullcline
w2 = a + b*u0; % calculate w nullcline

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% III. SOLVE DEs

u = zeros(size(t)); % Preallocate array for velocities
w = zeros(size(t)); % Preallocate array for positions

u(1) = -2; % Initial condition gives solution for position at t=0.
w(1) = -2; % Initial condition gives solution for velocity at t=0.

for i=1:(length(t)-1)
    u(i+1) = u(i) + (u(i) -u(i)^3/3 -w(i) + I)*h;
    w(i+1) = w(i) + epsilon*(a + b*u(i) - w(i))*h;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%
%% IIII. PLOT RESULTS

figure
hold on
grid on
plot(u0,w1,'b','linewidth',2)
plot(u0,w2,'r','linewidth',2)
plot(u,w,'g','linewidth',2)
legend('u nullcline','w nullcline','trajectory')
xlabel('u')
ylabel('w')
print(gcf,'-depsc','excercise33c_I0.eps')