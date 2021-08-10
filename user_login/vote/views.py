import pytz
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json
from web3 import Web3, exceptions
from .utils import get_plot
from .models import Election_start_stop
#from datetime import datetime
from pytz import timezone
from django.utils import timezone
from datetime import datetime
from django.core.cache import cache
from voters.models import Voter
from django.conf import settings
#now=timezone.now()
#now = datetime.datetime.now()
#start_stop = get_object_or_404(Election_start_stop, pk =0)
#start_time = start_stop.start_time
#end_time = start_stop.end_time
#now = now.strftime("%Y-%m-%d %H:%M:%S")
#start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
#end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

#if now > start_time and now < end_time:
 #   start_stop.Election_status = True
#else:
 #   start_stop.Election_status = False



ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.defaultAcount = web3.eth.accounts[0]

abi = json.loads('[{"constant":false,"inputs":[{"name":"_candidateid","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"candidates","outputs":[{"name":"id","type":"uint256"},{"name":"name","type":"string"},{"name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"temp","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_candidateid","type":"uint256"}],"name":"disname","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"voters","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_candidateid","type":"uint256"}],"name":"display","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"end","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"chalu","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_candidateid","type":"uint256"}],"name":"votedEvent","type":"event"}]')

address = web3.toChecksumAddress("0x6c655D7CeD3EaBB97F0167A438239Ed4753F9215")

contract = web3.eth.contract(address=address, abi= abi)
candidateCount = 2

def vote(request):
    if settings.BOOL_KEY == False:
        return redirect('http://127.0.0.1:8000/login/')
    now = timezone.now()
    # now = datetime.datetime.now()
    start_stop = get_object_or_404(Election_start_stop, pk=0)
    start_time = start_stop.start_time
    temp = start_time
    tz = pytz.timezone('Asia/Kolkata')
    #temp =temp.replace(tzinfo = tz)
    temp = temp.astimezone(tz)
    print(temp)
    end_time = start_stop.end_time
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

    if now > start_time and now < end_time:
        Election_start_stop.objects.filter(index =0).update(Election_status = True)
    else:
        #start_stop.Election_status = False
        Election_start_stop.objects.filter(index=0).update(Election_status=False)

    user= request.session.get('user')
    voter = Voter.objects.filter(user=user).first()
    voter_index = voter.index
    mobile = voter.mobile
    name = voter.name
    print(voter_index)
    if now < start_time:
        print(type(temp))
        return render(request,"vote/Not_started.html",{"time" : temp})
        return HttpResponse("Election not started yet")
    if now > end_time:
        return render(request,"vote/ended.html")
        return HttpResponse("Election already ended")
    l = {}
    candidateList=[]
    for i in range (1,candidateCount+1):
        nameOfCandidate = contract.functions.disname(i).call()
        l[i] = nameOfCandidate
        candidateList.append(nameOfCandidate)
    if request.method == 'POST':
        q= request.POST.dict()
        temp_list=[k for k,v in q.items()]
        print(temp_list[1])
        vote_casted_for = int(temp_list[1])
        print(vote_casted_for)
        print(contract.functions.display(vote_casted_for).call())
        #voter_index = 6
        try:
            tx_hash = contract.functions.vote(vote_casted_for).transact({'from': web3.eth.accounts[voter_index]})
            web3.eth.wait_for_transaction_receipt(tx_hash)
            print('now voteCount')
            print(contract.functions.display(vote_casted_for).call())
            name_of_candidate_voted_for = contract.functions.disname(vote_casted_for).call()
            # print(n)
            context = {'candidate': name_of_candidate_voted_for, 'mobile': mobile, 'user': user, 'name': name}
            return render(request, "vote/successful_vote.html", context)
        except exceptions.SolidityError as error:
            return render(request, "vote/alreadyVoted.html",{'name':name,'user':user})
    return render(request, "vote/election.html",{"names": l,'mobile':mobile,'user':user,'name':name})

def result(request):
    now = timezone.now()
    # now = datetime.datetime.now()
    start_stop = get_object_or_404(Election_start_stop, pk=0)
    start_time = start_stop.start_time
    temp = start_time
    end_time = start_stop.end_time
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    if now < end_time:
        return render(request, "vote/still_going_on.html")
    candidateVoteCount = {}
    x=[]
    for i in range (1, candidateCount+1):
        candidateVoteCount[i] = contract.functions.display(i).call()
        x.append(contract.functions.disname(i).call())
    winner = max(candidateVoteCount, key= candidateVoteCount.get)

    nameOfWinner = contract.functions.disname(winner).call()
    voteCount = contract.functions.display(winner).call()
    count =0
    for i in range(1, candidateCount+1):
        if contract.functions.display(i).call() == voteCount:
            count= count +1
    if count > 1:
        return render(request,"vote/tie.html")
    y = [v for k,v in candidateVoteCount.items()]
    chart = get_plot(x,y)
    context = {'name': nameOfWinner, 'id': winner, 'count': voteCount, 'chart' : chart}

    return render(request, "vote/results.html", context)

def candidateDetails(request):
    l = {}
    candidateList = []
    for i in range(1, candidateCount + 1):
        nameOfCandidate = contract.functions.disname(i).call()
        l[i] = nameOfCandidate
        candidateList.append(nameOfCandidate)
    context={'candidates':l}
    return render(request, "vote/details.html", context)

