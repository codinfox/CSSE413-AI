% BM25 Computing the BM25 score for givin document and search query
% ASSUME THERE IS A VARIABLE NAMED DATA IN MAIN WORKSPACE
% document - a 1x2 cell with 1st column to be the filename and second
%            to be the content string array
% query    - a string array
function score = BM25(document, query)
data = evalin('base', 'data'); % get all documents from base workspace

% some constants
k1 = 1.5; % 1.2 <= k1 <= 2.0
b = 0.75;
avgdl = avg_doc_len(data); % average document length
doclen = length(document{2});

result = 0;
for q = query
    fq = f(q, document);
    tmp = IDF(q,data)*((fq*(k1+1))/(fq+k1*(1-b+b*doclen/avgdl)));
    result = result + tmp;
end

score = result;
end

% F Computing term frequency of  givin term q in Document D
function frequency = f(q, D)
total_words = length(D{2}); % total number of words of the document
counter = 0;
for word = D{2}
    if strcmp(word, q)
        counter = counter+1;
    end
end
frequency = counter / total_words;
end

% AVG_DOC_LEN Computing the average document length in text collecton
function len = avg_doc_len(data)
num_docs = length(data);
total_words = 0; % total word counts for entire text collection
for idx = 1:num_docs
    total_words = total_words + length(data{idx, 2});
end
len = total_words / num_docs;
end

% IDF Computing the inverse document frequency
% q - a string
function freq = IDF(q, data)
N = length(data);
nd = 0; % number of documents that contain q
for idx = 1:N
    if ~isempty(find(strcmp(q, data{idx,2}), 1))
        nd = nd + 1;
    end
end
freq = log2((N-nd+0.5)/(nd+0.5));
end