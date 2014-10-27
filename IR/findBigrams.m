function [ bigrams ] = findBigrams( words )
%findBigrams
%   finds all bigrams and skip-bigrams out of an array of words
%   @input args:
%   words cell array of words
%   @output args:
%   bigrams cell array of skip-bigrams, bigrams and words

bigrams=words{1};
for i=1:length(words)
    if i~= 1
        bigrams=[bigrams words{i}];
    end
    if i<length(words)
        bigrams=[bigrams strcat(words{i},{' '},words{i+1})];
        bigrams=[bigrams strcat(words{i+1},{' '},words{i})];
        if i<length(words)-1
            bigrams=[bigrams strcat(words{i},{' '},words{i+2})];
            bigrams=[bigrams strcat(words{i+2},{' '},words{i})];
        end
    end
end

end

