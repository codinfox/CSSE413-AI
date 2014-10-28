%RELATED_CONCEPT Find the most relavent words
% corpus - ngram_corpus
% query  - string (character array)
% f      - number of results
function [ concepts ] = related_concept( corpus, query, f )

counter = 1;
result = [];
for idx = 1:length(corpus)
    if counter > 5
        break;
    end
    if find(not(cellfun('isempty', strfind(corpus{idx, 1}, query))))
        result = [result, corpus{idx, 1}];
    end
end

[unique_terms, ~, J] = unique(result);
occ = histc(J, 1:numel(unique_terms));

[~, od] = sort(occ, 'descend');
concepts = [];

tail = f;
if length(unique_terms) < f
    tail = length(unique_terms);
end

for idx = 1 : tail
    concepts = [concepts, {unique_terms{od(idx)}}]; 
end

end

