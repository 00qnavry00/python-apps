#!/usr/bin/python

import sys
import os
import optparse

# Tool to zip repos from command line with following command
# ./zip-repos_simple.py -l <login_name>:<password> -all -b master


def zip (repos, zip_name, login_str, branch):
    cloneHTTPS = "git clone http://"
    github ="github.com/00qnavry00/"

    # if there is only one repo in the repos list, there is no need to create a project directory
    if len(repos) == 1:
        repo = repos[0]
        print("\n Cloning " + repo + " repo, branch " + branch + "\n")

        os.system(cloneHTTPS + login_str + github + '/' + repo + '.git -b' + branch)
        if os.path.exists(repo):
            os.system('rm -rf %s/.git' % repo)
            os.system('zip -r9 %s.zip %s' % (zip_name, repo))
            os.system('rm -rf %s' % repo)

    else:
        os.makedirs(zip_name)
        os.chdir(zip_name)

        for repo in repos:
            print("\n Cloning " + repo + " repo, branch " + branch + "\n")
            os.system(cloneHTTPS + login_str + github + '/' + repo + '.git -b' + branch)
            if os.path.exists(repo):
                os.system('rm -rf %s/.git' % repo)

        os.chdir('../')
        os.system('zip -r9 %s.zip %s' % (zip_name, zip_name))
        os.system('rm -rf %s' % zip_name)
    

## Assuming that xx.x branch value is only reserved for release branches
## If not float value is entered, entered value is assumed to be an existing branch name (Ex.: master, develop)

# def full_branch_name(branch, char):
#     branch_name = branch
#     try:
#         float(branch)
#         branch_name = 'release' + char + branch
#         return branch_name
#     except ValueError:
#         return branch_name

def main(): #USED TO HAVE 'argv = None' HERE. IF ERROR RESULTS, RETURN TO THIS
    argv = sys.argv[1:]
    try:
        if not "-l" in argv:
            print("\nPlease add '-l <login_name>:<password>' as argument to this script for authentication.\n")
            sys.exit()
        else:
            i = argv.index("-l")
            login = argv[i+1]
            
            if not len(login) or not ':' in login:
                print("\nPlease provide login info in the following format: -l <login_name>:<password>\n")
                sys.exit()

        if not "-b" in argv:
            print("\nSince '-b <branch_name>' is not specified, we will zip master branch.\n")
            branch = 'master'
        else:
            i = argv.index("-b")
            branch = argv[i+1]


        # Opens up repo_list.txt and writes all contents into a list to be used later
        with open("repo_list.txt", 'r') as e:
            repo_list = []
            for i in e:
                repo_list.append(i)

        # Will now look for and zip specific repositories specified by user
        if "-repo" in argv:
            start = argv.index("-repo") + 1
            if "-b" in argv:
                finish = argv.index("-b")
            else:
                finish = argv.index("master")
            desired_repos = argv[start:finish]
            for k in desired_repos:
                if k in repo_list:
                    zip([k.lower()], k, login, 'master')
                else:
                    print("\n The Repository: '" + k + "' was NOT found.")

        # Will zip all repositories
        elif "-all" in argv:
            for j in repo_list:
                zip([j.lower()], j, login, 'master')

        # Will advise user of improper use of syntax
        else:
            print("\nPlease either include '-repo <repo names>' separated by white spaces as the script arguments for specific repositories or '-all' for all repositories.")


        # if "-all" in argv or 'application1' in repo_list:
        #     # Create zip file with application1 repo
        #     zip(['application1'], 'zip_name1', login, 'master')
        #
        # if "-all" in argv or 'application2' in repo_list:
        #     # Create zip file with application2 repo
        #     zip(['application2'], 'zip_name2', login, 'master')


    except Exception as e:
        raise(e)


if __name__ == '__main__':
    sys.exit(main())

