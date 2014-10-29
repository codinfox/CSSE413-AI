clear all; clc;
% Initialization
load data_nonstop;

n = 5; % num of grams
ngram_corpus_per_passage = cell(length(data), 1);

num_corpus = 0;
for idx = 1:length(data)
    five_grams = cell(length(data{idx, 2})-n+1, 1);
    for s_idx = 1:(length(data{idx, 2})-n+1)
        tmp_grams = data{idx, 2}(s_idx: s_idx+n-1);
        five_grams{s_idx} = tmp_grams;
    end
    ngram_corpus_per_passage{idx} = five_grams;
    num_corpus = num_corpus + length(five_grams);
end

ngram_corpus = cell(num_corpus, 2);
idx_corpus = 1;
for idx = 1:length(ngram_corpus_per_passage)
    for s_idx = 1:(length(ngram_corpus_per_passage{idx,1}))
        five_grams = ngram_corpus_per_passage{idx}{s_idx};
        five_grams = sort(five_grams);
        ngram_corpus{idx_corpus,1} = five_grams;
        ngram_corpus{idx_corpus,2} = 1;
        idx_corpus = idx_corpus+1;
    end
end

idx = 1;
while idx <= length(ngram_corpus)
    fprintf('%d\n', idx);
    s_idx = idx + 1;
    while s_idx <= length(ngram_corpus)
        if isequal(ngram_corpus(idx, 1), ngram_corpus(s_idx, 1))
            ngram_corpus(s_idx,:) = [];
            ngram_corpus{idx, 2} = ngram_corpus{idx, 2} + 1;
        else
            s_idx = s_idx + 1;
        end
    end
    idx = idx + 1;
end

ngram_corpus_sorted = sortrows(ngram_corpus, -2);

save('ngram_corpus.mat', 'ngram_corpus_sorted', 'ngram_corpus', 'ngram_corpus_per_passage', n);
