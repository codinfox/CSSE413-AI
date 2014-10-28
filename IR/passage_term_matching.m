function [ scores ] = passage_term_matching( data, query )
%applies the passage term matching scoring method over ALL documents
%   @input args
%   query : cell of strings
%   data : cell of even more cells - can be found in data.mat
%   @output args
%   scores : array of doubles
numberOfDocs=length(data(:,2));
intersections=ones(numberOfDocs,length(query));
numberOfDocsWithToken=1:length(query);
if iscellstr(query)==0
    query=query{1};
end
for j=1:length(query)
    numberOfDocsWithToken(j)=0;
    for i=1:numberOfDocs
      
        
        intersections(i,j)=ismember(query{j},data{i,2});
        if intersections(i,j)==1
            numberOfDocsWithToken(j)=numberOfDocsWithToken(j)+1;
        end
    end 
    if numberOfDocsWithToken(j)==numberOfDocs-1
        numberOfDocsWithToken(j)=numberOfDocsWithToken(j)+0.000000001;
    end
end

idf=log(numberOfDocs./(numberOfDocsWithToken+1));
sumOfW=0.*(1:numberOfDocs);
sumOfIdf=0;
for j=1:length(query)
    sumOfIdf=sumOfIdf+idf(j);
    for i=1:numberOfDocs
        w(i,j)=intersections(i,j)*numberOfDocsWithToken(j);
        sumOfW(i)=sumOfW(i)+w(i,j);
    end  
end

scores=sumOfW./sumOfIdf;

end

