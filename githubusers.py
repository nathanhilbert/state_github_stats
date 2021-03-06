from pygithub3 import Github
import ConfigParser
import sys
import os
import json


config = ConfigParser.ConfigParser()
config.read(['.githubconfig', os.path.expanduser('~/.privatestuff/.githubconfig')])


username = config.get('github', 'username', None) 
password = config.get('github', 'password', None) 

if not username or not password:
    print "No user name or password supplied"
    print "Create a config file in ~/.privatestuff/.githubconfig (Sorry Windows users, this will not work for you)"
    print "[github]"
    print "username=mygithubusername"
    print "password=mygithubpassword"
    print "*remember to delete the file when you walk away"
    sys.exit(1)

gh = Github(login=username, password=password)

totalstats = {"orgrepos":0, "memberrepos":0, "nummembers":0}

ORGNAME = 'USStateDept'

orgrepos_contribs = {}

for repo in gh.repos.list_by_org(ORGNAME).all():

    contribers = gh.repos.list_contributors(user=ORGNAME, repo=repo.name).all()
    con_array = []
    for contriber in contribers:
        con_array.append(contriber.login)
    orgrepos_contribs[repo.name] = con_array

totalstats['orgrepos'] = len(orgrepos_contribs.keys())



#username:
#       numprivaterepos
#       contribs to org
output = {}


for member in gh.orgs.members.list(ORGNAME).all():
    totalstats['nummembers'] += 1
    output[member.login] = {"orgcontribs": 0, "privaterepos":0}
    for memrepo in gh.repos.list(member.login).all():
        #find if they actually contribute to their own repos
        try:
            tempcontribers = gh.repos.list_contributors(user=member.login, repo=memrepo.name).all()
        except:
            print "probably empty repo"
            tempcontribers = []
        for tc in tempcontribers:
            if (member.login == tc.login):
                output[member.login]["privaterepos"] += 1
                totalstats['memberrepos'] +=1
                #output[member.login]["repos"].append(memrepo.name)
        #output[member.login]["stats"]["privaterepos"] = len(output[member.login]["repos"])

    #find where they contribute at state
    for reponame, contriblist in orgrepos_contribs.iteritems():
        if member.login in contriblist:
            output[member.login]['orgcontribs'] += 1


print "Looked at ", str(totalstats['nummembers']), "members"
print "Those members had", str(totalstats['memberrepos']), "repositories"
print "Our Org has", str(totalstats['orgrepos'])
with open(os.path.dirname(os.path.realpath(__file__)) + "/output.json", 'wb') as jsonfile:
    json.dump(output, jsonfile)















