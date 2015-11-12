close all
clear all
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 0. PARAMETERS

% Euler integration
h = 10e-5;      % step size parameter
time = 500;     % simulation time

% Model
a = -1;
c1 = -1;
b = 2;
epsilon = 0.1;

t = 0:h:time; % generate time vector
I = [-1*(linspace(0,2,round(length(t)/2-1))) zeros(round(length(t)/2),1)']'; % create current vector

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% I. CALCULATE NULLCLINES

u = linspace(-3,3,length(t)); % preallocate voltage array
w = linspace(-3,3,length(t)); % preallocate w array
w = zeros(length(u),1); % preallocate aray for piecewise function

for i = 1:length(u)
    u1 = u(i);
    w(i) = fu(u1,a,c1);
end

nu = w + 0; % calculate voltage nullcline
nu_new = w - 2; % calculate voltage nullcline
nw = b*u; % calculate w nullcline
%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% II. PERFORM INTEGRATION

u_sol = zeros(size(t)); % Preallocate array for velocities
w_sol = zeros(size(t)); % Preallocate array for positions

u_sol(1) = -2/3;%1.5;               % Initial condition gives solution for position at t=0.
w_sol(1) = -4/3;%0.375;             % Initial condition gives solution for velocity at t=0.

for i=1:(length(t)-1) % loop over time
    u_sol(i+1) = u_sol(i) + (fu(u_sol(i),a,c1) - w_sol(i) + I(i))*h; % integrate voltage DE
    w_sol(i+1) = w_sol(i) + epsilon*(b*u_sol(i) - w_sol(i))*h; % integrate w DE
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% III. PLOT REULTS
figure
hold on
grid on
plot(u,nu,'b','linewidth',2)
plot(u,nu_new,'k','linewidth',2)
plot(u,nw,'r','linewidth',2)
plot(u_sol,w_sol,'g','linewidth',2)
legend('u nullcline for I=0','u nullcline for I=-2','w nullcline','trajectory')
xlabel('u')
ylabel('w')
print(gcf,'-depsc','excercise32c_full.eps')