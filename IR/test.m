load('/home/jon/workspace/CSSE413-AI/IR/data.mat');
queries={{'adams'},{'lincoln'},{'president'},{'assassinated','president'},{'great','president'},{'first','president'},{'civil','war','president'},{'united','states'}};
for i=1:length(queries)
    query=queries{i};
    
    
    passagescores=passage_term_matching(data,query);
    counter=j
    for j=1:length(data)
        scores_passage_term_matching(i,j)=passagescores(j);
        
        scores_BM25(i,j)=BM25({data{j,1},data{j,2}},query);
        
        scores_skip_bi_gram(i,j)=skip_bi_gram(data{j,2},query);
    end
end
close all
for num=1:length(queries)

figure(num)
plot(1:43,scores_BM25(num,:)/max(scores_BM25(num,:)),'g');
hold on;

plot(1:43,scores_skip_bi_gram(num,:)/max(scores_skip_bi_gram(num,:)),'r');

plot(1:43,scores_passage_term_matching(num,:)/max(scores_passage_term_matching(num,:)));

end