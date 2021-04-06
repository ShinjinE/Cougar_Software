%--------------------------------------------------------------------------
% FILE: time_delay_analysis.m
% AUTHOR: Parker King
% DATE: 3/17/2021
% 
% PURPOSE: To process and analyze data to help understand the results of
%           the input frequency time test which records the time between
%           inputing inputs from the right analog stick, left analog stick,
%           right trigger and left trigger being input continuously.
%
%           This code specifically checks for time data that is longer than
%           a specified time length. This is to better understand the
%           circumstances these longer delays occur under.
%
% INPUT:
% input_frequency.txt - A comma delimited text file with four columns of
%           data. The only columns data are captured from is the first and
%           the fourth column. The first column contains the data point
%           number and the fourthcolumn contains a timestamp for the data
%           point.
%
% OUTPUT:
% latency_summary.xlsx - An excel file with three sheets: Data, Summary and
%           Percents Analysis.
%
%           Data contains the data point number and timestamp from
%           input_frequency.txt as well as the computed time delay between
%           each point.
% 
%           Summary contains the extract time delays that were longer than
%           the specified criteria.
% 
%           Percents Analaysis computes the percent for how many data
%           points had a long delay and the percent of how much time those
%           delays took up out of the duration of the data collection.
%
%--------------------------------------------------------------------------

%% Load Data
% Clear vectors that don't have a set size
clear latency_num latency_point latency_stamp long_latency

% Define properties to read a delimited text file, then read it
varNames = {'Input_Number','Button_Input','Process_Time_micro_s'...
            ,'Total_Time_s'};
varTypes = {'int32','char','double','double'};
delimiter = ',';
dataStartLine = 2;
opts = delimitedTextImportOptions('VariableNames',varNames,...
                                'VariableTypes',varTypes,...
                                'Delimiter',delimiter,...
                                'DataLines', dataStartLine);
raw_table = readtable('input_frequency.txt',opts);

% Extract data to analyze
data_num = raw_table.Input_Number;
time_stamp = raw_table.Total_Time_s;

%% Find long latency
% Initialize loop variables
j = 0;
time_delay = zeros((length(data_num)-1),1);
criteria_time = 0.060;  % Seconds

for i = 1:(length(data_num) - 1)
    % Time delay between each timestamp
    time_delay(i) = time_stamp(i + 1) - time_stamp(i);
    
    % Identify delays that are very long
    if time_delay(i) > criteria_time
        j = j + 1;
        latency_num(j,1) = j;
        latency_point(j,1) = data_num(i);
        latency_stamp(j,1) = time_stamp(i);
        long_latency(j,1) = time_delay(i) * 1000;   % Milliseconds
    end
end

%% Percentages
% What is the percentage of points with a long delay
latency_points = length(latency_num);
total_points = length(data_num);
percent_data = latency_points/total_points * 100;

% What is the percentage of elapsed time that consists of long delays
latency_time = sum(long_latency)/1000;
total_time = time_stamp(end) - time_stamp(1);
percent_time = latency_time/total_time * 100;

%% Analysis Summary Table
% Create table to export summary data
latency_summary = table(latency_num,latency_point,latency_stamp,...
    long_latency);

%% Write Data
% Export data to an excel file
writematrix(["Data Number", "Timestamp (s)", "Time Delay (ms)"],...
            'latency_summary.xlsx','Sheet','Data')
writematrix(data_num,'latency_summary.xlsx','Sheet','Data','Range','A2')
writematrix(time_stamp,'latency_summary.xlsx','Sheet','Data','Range','B2')
writematrix(time_delay*1000,'latency_summary.xlsx','Sheet','Data',...
            'Range','C3')
writetable(latency_summary,'latency_summary.xlsx','Sheet','Summary')
writematrix(["Latency Number", "Data Point", "Timestamp (s)",...
            "Latency Duration (ms)"],'latency_summary.xlsx','Sheet',...
            'Summary','Range','A1')
writecell({'',"Data Points","Time (s)";
            "Latency",latency_points,latency_time;
            "Total",total_points,total_time;
            "Percentage",percent_data,percent_time},...
            'latency_summary.xlsx','Sheet','Percents Analysis')