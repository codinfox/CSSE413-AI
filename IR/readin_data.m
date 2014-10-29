clear all; clc;
load filename
for i = 1:43
fn=['./processed_nonstop/' filenames(i).name];
data{i,1}=filenames(i).name;
data{i,2}=readtext(fn, ' ', '', '', 'textual');
end
clear i fn filenames;
save data_nonstop;