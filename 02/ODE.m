close all
clear all
clc

% Calculate solution of single linear ODE using Euler moving forward
% algorithm

steps = [30,20,10,5,0.1];   % step size parameter
time = 200;                 % simulation time

figure                      % prepare figure
hold on                     % plot in every loop cycle in same figure
grid on                     % plot mesh grid
xlabel('time')
ylabel('voltage')
cc = hsv(5);
n=1;
for h = steps               % loop over different step sizes
    t = 0:h:time;               % t goes from 0 to 2 seconds.
    ystar = zeros(size(t));     % Preallocate array

    % Generate heaviside function
    N=round(100/h);             % convert time scale to steps
    h1=zeros(N,1);              % generate part which is 0 (x<100)
    h2=ones(length(t)-N,1);     % generate part which is 1 (x>100)
    heavi=[h1; h2];             % combine two parts

    ystar(1) = 0;               % Initial condition gives solution at t=0.
    
    for i=1:(length(t)-1)
        k1 = 1/10*ystar(i)+heavi(i);   % Previous approx for y gives approx for derivative
        ystar(i+1) = ystar(i) + k1*h;   % Approximate solution for next value of y
    end
    
    plot(t,ystar,'color',cc(n,:),'linewidth',2);              % plot result for specific time step
    n=n+1;
end
legend('30','20','10','5','0.1')    % write step size values in legend
print(gcf,'-depsc','exercise1b.eps');