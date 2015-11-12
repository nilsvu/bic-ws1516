close all
clear all
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% I. DEFINE PARAMETERs

% Euler
h = 10e-5; % step size parameter
time = 500; % simulation time
t = 0:h:time; % generate time vector

% model
epsilon = 0.1;
a = 15/8;
b = 3/2;
I = linspace(0,3,50); % create linear incresing current vector

rate = zeros(50,1); % preallocate rate array

for j = 1:length(I) % loop over currents
curr = I(j);
u = zeros(size(t)); % Preallocate array for velocities
w = zeros(size(t)); % Preallocate array for positions

u(1) = -1.5; % Initial condition gives solution for position at t=0.
w(1) = -0.375; % Initial condition gives solution for velocity at t=0.

numberOfPeaks = 0; % set counter
alreadyPeaked = 0; % set counter
threshold = 1; % set threshold

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% II. PERFORM INTEGRATION
for i=1:(length(t)-1)
    u(i+1) = u(i) + (u(i) -u(i)^3/3 -w(i) + curr)*h; % integrate u
    w(i+1) = w(i) + epsilon*(a + b*u(i) - w(i))*h; % inegrate w
    % detection algorithm
    if(u(i+1) >= threshold)
        alreadyPeaked = 1;
    else
        if(alreadyPeaked == 1)
            alreadyPeaked = 0;
            numberOfPeaks = numberOfPeaks + 1;
        end
    end
end
rate(j) = numberOfPeaks/time; % normalize rate
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% III. PLOT RESULTS

figure                      % prepare figure
hold on                     % plot in every loop cycle in same figure
grid on                     % plot mesh grid
xlabel('Current')
ylabel('Rate')
plot(I,rate,'Linewidth',2)
print(gcf,'-depsc','excercise33a.eps')