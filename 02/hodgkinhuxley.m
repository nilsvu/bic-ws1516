close all
clear all
clc

% Hodgkin Huxley simulation

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% I. Parameter %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
simulationTime = 200; %in milliseconds
deltaT=.01;
t=0:deltaT:simulationTime;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% II. Specification of external current %%%
%I(1:1000) = 0; I(1001:2000) = 3; I(2001:numel(t)) = 0;

% in order to plot result of exercise 2.4 uncomment the following lines
%% rheobase
I = 0.08*t;

%% inhibitory rebound
%I(1:5000) = 0; I(5001:10000) = -3; I(10001:numel(t)) = 0;

%% resonant spiking
%I(1:5000) = 0; I(5001:6000) = 2.05; I(6001:7000) = 0; I(7001:8000) = 2.05; I(8001:9000) = 0; I(9001:10000) = 2.05; I(10001:11000) = 0; I(11001:12000) = 2.05; I(12001:numel(t)) = 0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% III. Model parameter %%%%%%%%%%%%%%%%%%%%
gbar_K=36; gbar_Na=120; g_L=.3; % concutivities
E_K = -12; E_Na=115; E_L=10.6; % Nernst potentials
C=1; % membrane capacitance

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% IV. Initial values for Euler %%%%%%%%%%%%
V=0; %Baseline voltage
alpha_n = ( (0.1-0.01*V) / (exp(1  -0.1*V)-1) ); % alpha n gate
alpha_m = ( (2.5- 0.1*V) / (exp(2.5-0.1*V)-1) ); % alpha m gate
alpha_h = 0.07*             exp(-V/20); % alpha h gate
beta_n  = 0.125*            exp(-V/80); % beta n gate
beta_m  = 4*                exp(-V/18); % beta m gate
beta_h  = 1              / (exp(3-0.1*V)+1); % beta h gate

n(1) = alpha_n/(alpha_n+beta_n); % channel activation n gate
m(1) = alpha_m/(alpha_m+beta_m); % channel activation m gate
h(1) = alpha_h/(alpha_h+beta_h); % channel activation h gate

for i=1:numel(t)-1 %Compute coefficients, currents, and derivates at each time step
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% V. Calculate coefficients %%%%%%%%%%%%%%%
    %Equations here are same as above, just calculating at each time step
    alpha_n(i) = ( (0.1-0.01*V(i)) / (exp(1  -0.1*V(i))-1) );
    alpha_m(i) = ( (2.5- 0.1*V(i)) / (exp(2.5-0.1*V(i))-1) );
    alpha_h(i) = .07*                 exp(-V(i)/20);
    beta_n(i)  = 0.125*               exp(-V(i)/80);
    beta_m(i)  = 4*                   exp(-V(i)/18);
    beta_h(i)  = 1                 / (exp(3-0.1*V(i))+1);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% VI. Calculate currents %%%%%%%%%%%%%%%%%%
    I_Na = (m(i)^3) * gbar_Na * h(i) * (V(i)-E_Na); %Equations 3 and 14
    I_K = (n(i)^4) * gbar_K * (V(i)-E_K); %Equations 4 and 6
    I_L = g_L *(V(i)-E_L); %Equation 5
    I_ion = I(i) - I_K - I_Na - I_L; 
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% VII. Calculate derivatives %%%%%%%%%%%%%%
    V(i+1) = V(i) + deltaT*I_ion/C;
    n(i+1) = n(i) + deltaT*(alpha_n(i) *(1-n(i)) - beta_n(i) * n(i)); %Equation 7
    m(i+1) = m(i) + deltaT*(alpha_m(i) *(1-m(i)) - beta_m(i) * m(i)); %Equation 15
    h(i+1) = h(i) + deltaT*(alpha_h(i) *(1-h(i)) - beta_h(i) * h(i)); %Equation 16

end

V = V-65; %Set resting potential to -65mv to deal with shift

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% VIII. Plot voltage %%%%%%%%%%%%%%%%%%%%%%
figure
subplot(311)
grid on
hold on
plot(t,I,'r','lineWidth',3)
legend('current')
ylabel('current (mA)')
xlabel('time (ms)')
title('Stimulus current')
subplot(312)
plot(t,V,'LineWidth',3)
grid on
hold on
legend({'voltage'})
ylabel('Voltage (mv)')
xlabel('time (ms)')
title('Membrane potential')
subplot(313)
p1 = plot(t,gbar_K*n.^4,'LineWidth',2); % plot potassium conductance
grid on
hold on
p2 = plot(t,gbar_Na*(m.^3).*h,'r','LineWidth',2); % plot sodium conductance
legend([p1, p2], 'Conductance for Potassium', 'Conductance for Sodium')
ylabel('Conductance')
xlabel('time (ms)')
title('Conductance for Potassium and Sodium Ions')
print(gcf,'-depsc','rheobase.eps')