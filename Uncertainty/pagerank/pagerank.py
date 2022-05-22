import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    result={}
    if(len(corpus[page])==0):
        for i in corpus.keys():
            result[i]=1/len(corpus.keys())
    else:
        for i in corpus.keys():
            if(i in corpus[page]):
                result[i]=((1-damping_factor)/len(corpus.keys()))+(damping_factor/len(corpus[page]))
            else:
                result[i]=(1-damping_factor)/len(corpus.keys())
                    
    
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result={}
    for i in corpus.keys():
        result[i]=0
    
    numPage=random.randint(0,len(corpus.keys())-1)
    page=list(corpus.keys())[numPage]
    result[page]+=1
    
    for i in range(n-1):
        dico=transition_model(corpus,page,damping_factor)
        memoire=[]
        for i in dico.keys():
            if(len(memoire)==0):
                memoire.append(i)
            elif(dico[i]==dico[memoire[0]]):
                memoire.append(i)
            elif(dico[i]>dico[memoire[0]]):
                memoire=[i]
            else:
                pass
        numPage=random.randint(0,len(memoire)-1)
        page=memoire[numPage]
        result[page]+=1
        
    for i in result.keys():
        result[i]/=n
    
    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    result={}
    for i in corpus.keys():
        result[i]=1/len(corpus.keys())
    test=False
    
    while(not test):
        result2={}
        for i in result.keys():
            result2[i]=((1-damping_factor)/len(result.keys()))
            memoire=0
            for j in corpus.keys():
                if(len(corpus[j])!=0):
                    if(j!=i and i in corpus[j]):
                        memoire+=(result[j]/len(corpus[j]))
                else:
                    memoire+=(result[j]/len(result.keys()))
            result2[i]+=damping_factor*memoire
        for i in result.keys():
            if(abs(result[i]-result2[i])>0.001):
                test=False
                break
            else:
                test=True
        result=result2
    
    return result


if __name__ == "__main__":
    main()
