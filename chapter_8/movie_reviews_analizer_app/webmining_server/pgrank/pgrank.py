from pages.models import Page,SearchTerm

num_iterations = 100000
eps=0.0001
D = 0.85

def pgrank(searchid):
    s = SearchTerm.objects.get(id=int(searchid))
    links = s.links.all()
    print 'len',len(links),' name',s.term
    from_idxs = [i.from_id for i in links ]
    # Find the idxs that receive page rank 
    links_received = []
    to_idxs = []
    for l in links:
        from_id = l.from_id
        to_id = l.to_id
        if from_id not in from_idxs: continue
        if to_id  not in from_idxs: continue
        links_received.append([from_id,to_id])
        if to_id  not in to_idxs: to_idxs.append(to_id)
        
    pages = s.pages.all()
    prev_ranks = dict()
    for node in from_idxs:
        ptmp  = Page.objects.get(id=node)
        prev_ranks[node] = ptmp.old_rank
        
    #print 'prev_ranks:',len(prev_ranks)
    conv=1.
    cnt=0
    while conv>eps or cnt<num_iterations:
        next_ranks = dict()
        total = 0.0
        for (node,old_rank) in prev_ranks.items():
            total += old_rank
            next_ranks[node] = 0.0
        
        #find the outbound links and send the pagerank down to each of them
        for (node, old_rank) in prev_ranks.items():
            give_idxs = []
            for (from_id, to_id) in links_received:
                if from_id != node: continue
                if to_id  not in to_idxs: continue
                give_idxs.append(to_id)
            if (len(give_idxs) < 1): continue
            amount = D*old_rank/len(give_idxs)
            for id in give_idxs:
                next_ranks[id] += amount
        tot = 0
        for (node,next_rank) in next_ranks.items():
            tot += next_rank
        const = (1-D)/ len(next_ranks)
        
        for node in next_ranks:
            next_ranks[node] += const
        
        tot = 0
        for (node,old_rank) in next_ranks.items():
            tot += next_rank
        
        difftot = 0
        for (node, old_rank) in prev_ranks.items():
            new_rank = next_ranks[node]
            diff = abs(old_rank-new_rank)
            difftot += diff
        conv= difftot/len(prev_ranks)
        cnt+=1
        prev_ranks = next_ranks
        
    print 'convergence:',conv,' its:',cnt
    for (id,new_rank) in next_ranks.items():
        ptmp = Page.objects.get(id=id)
        url = ptmp.url
        print id,' url:',url
    
    for (id,new_rank) in next_ranks.items():
        ptmp = Page.objects.get(id=id)
        ptmp.old_rank = ptmp.new_rank
        ptmp.new_rank = new_rank
        ptmp.save()