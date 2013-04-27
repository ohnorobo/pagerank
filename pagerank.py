#!/usr/bin/python

'''
// P is the set of all pages; |P| = N
// // S is the set of sink nodes, i.e., pages that have no out links
// // M(p) is the set of pages that link to page p
// // L(q) is the number of out-links from page q
// // d is the PageRank damping/teleportation factor; use d = 0.85 as is typical
//

foreach page p in P
  PR(p) = 1/N                     /* initial value */

  while PageRank has not converged do
    sinkPR = 0
    foreach page p in S           /* calculate total sink PR */
      sinkPR += PR(p)
    foreach page p in P
      newPR(p) = (1-d)/N          /* teleportation */
      newPR(p) += d*sinkPR/N      /* spread remaining sink PR evenly */
      foreach page q in M(p)      /* pages pointing to p */
        newPR(p) += d*PR(q)/L(q)  /* add share of PageRank from in-links */
    foreach page p
      PR(p) = newPR(p)

return PR
'''

import pprint, math, sys

t = .85 #teleportation factor

def calculatePagerank(allpages, inlinks, outlinks, count):

    #find all pages with no outlinks
    nooutlinks = []
    for page in allpages:
        #if outlinks[page] == 0:
        if page not in outlinks:
            nooutlinks.append(page)

    #initial pagerank is evenly split
    pagerank = {}
    for key in allpages:
        pagerank[key] = 1.0/count

    prevPerplexity = 0
    currentPerplexity = perplex(pagerank)


    #main loop
    while not hasconverged(prevPerplexity, currentPerplexity):
        pprint.pprint(currentPerplexity)

        ####pagerank

        newpagerank = {}
        sinkPR = 0

        for page in nooutlinks:
            sinkPR += pagerank[page]

        for key in pagerank.keys():

            newpagerank[key] = (1 - t) / count
            newpagerank[key] += t * sinkPR / count
            for inlink in inlinks[key]:
                newpagerank[key] += t * pagerank[inlink] / outlinks[inlink]

        ###

        pagerank = newpagerank
        prevPerplexity = currentPerplexity
        currentPerplexity = perplex(pagerank)

    return pagerank

def hasconverged(prevPerplexity, currentPerplexity):
    r1 = round(prevPerplexity, 4)
    r2 = round(currentPerplexity, 4)
    return r1 == r2

def perplex(pagerank):
    return pow(2, shannonEntropy(pagerank))

def shannonEntropy(pagerank):
    s = 0
    for key in pagerank:
        p = pagerank[key]
        s += p * math.log(p, 2)
    return -1 * s

def readFile():
    count = 0 #total num pages in collection
    inlinks = {} #dict of pages to a list of all inlinks
    outlinks = {} #dict of pages to count of outlinks
    allpages = [] #list of all pages seen
    f = open(sys.argv[1], 'r')
    content = f.readlines()

    for line in content:
        line = line.strip() #remove newlines
        links = line.split(" ")

        node = links[0]

        links.remove(node)

        inlinks[node] = links
        allpages.append(node)

        for link in links:
            if link in outlinks:
                outlinks[link] += 1
            else:
                outlinks[link] = 1

        count += 1

    return allpages, inlinks, outlinks, count


def getTopXbyPagerank(x, pageranks):
    for key, value in sorted(pageranks.iteritems(), key=lambda (k,v): (v,k)):
        print "%s: %s" % (key, value)

def sumPagerank(pagerank):
    s = 0
    for key in pagerank.keys():
        s += pagerank[key]
    return s

#main
allpages, inlinks, outlinks, count = readFile()
#pprint.pprint(inlinks)
print count
pagerank = calculatePagerank(allpages, inlinks, outlinks, count)
print "final pagerank"
#pprint.pprint(pagerank)
getTopXbyPagerank(10, pagerank)
