function [ score ] = skip_bi_gram( query, text )
%skip_bi_gram
%   applies the skip-bigram scoring method on a text based on a query
%   @input args
%   query, text : cell arrays of strings
%   @output args
%   score : double
if length(text)<0 && length(query)<0
    score=0;
else
querybigrams=findBigrams(query);
textbigrams=findBigrams(text);
scoreP=length(intersect(querybigrams,textbigrams))/length(querybigrams);
scoreQ=length(intersect(querybigrams,textbigrams))/length(textbigrams);
if scoreP+scoreQ>0
    score=(2*scoreP*scoreQ)/(scoreP+scoreQ);
else
    score=0;
end
end




end