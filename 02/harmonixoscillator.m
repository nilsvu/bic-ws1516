close all
clear all
clc

% Calculate solution of higher order ODE (harmonic oscillator) using Euler
% moving forward algorithm

steps = [1,0.1,10e-5];      % step size parameter
time = 10;                  % simulation time

figure                      % prepare figure
hold on                     % plot in every loop cycle in same figure
grid on                     % plot mesh grid
xlabel('time')
ylabel('x')
cc = hsv(3);
n=1;
for h = steps               % loop over different step sizes
    t = 0:h:time;               % generate time vector
    
    ystar = zeros(size(t));     % Preallocate array for velocities
    xstar = zeros(size(t));     % Preallocate array for positions

    ystar(1) = 0;               % Initial condition gives solution for position at t=0.
    xstar(1) = 1;               % Initial condition gives solution for velocity at t=0.
    for i=1:(length(t)-1)
        ystar(i+1) = ystar(i) - xstar(i)*h; % Approximate solution for next value of velocity
        xstar(i+1) = xstar(i) + ystar(i)*h; % Approximate solution for next value of position
    end
    
    plot(t,xstar,'color',cc(n,:),'linewidth',2);              % plot result for specific time step
    n=n+1;
end
legend('1','0.1','10e-5')   % write step size values in legend
print(gcf,'-depsc','exercise1c.eps')