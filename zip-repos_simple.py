#!/usr/bin/python

import sys
import os
import optparse

# Tool to zip repos from command line with following command
# ./zip-repos_simple.py -l <login_name>:<password> -all -b master

def zip(repos, zip_name, login_str, branch):
    cloneHTTPS = "git clone https://"
    github ="github.com/00qnavry00"

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

def full_branch_name(branch, char):
    branch_name = branch
    try:
        if 'release' in branch:
            return branch
        else:
            float(branch)
            branch_name = 'release' + char + branch
            return branch_name
    except ValueError:
        return branch_name

def main(): #USED TO HAVE 'argv = None' AS PARAMETER. IF ERROR RESULTS, RETURN TO THIS
    argv = sys.argv[1:]
    try:
        # if not "-l" in argv:
        #     print("\nPlease add '-l <login_name>:<password>' as argument to this script for authentication.\n")
        #     sys.exit()
        # else:
        #     i = argv.index("-l")
        #     login = argv[i+1]
        #
        #     if not len(login) or not ':' in login:
        #         print("\nPlease provide login info in the following format: -l <login_name>:<password>\n")
        #         sys.exit()

        if "-h" in argv:
            print("---------------------------------------\nHELP TOOL \n---------\n\n")
            print("If you want specific repositories:")
            print("./zip-repos_simple.py -l <login_name>:<password> -repos repo1 repo2\n\n")
            print("If you want all repositories:")
            print("./zip-repos_simple.py -l <login_name>:<password> -all\n\n")
            print("If you want repos from select groups:")
            print("./zip-repos_simple.py -l <login_name>:<password> -groups group1 group2\n\n")
            print("If you want a branch other than 'master':")
            print("./zip-repos_simple.py -l <login_name>:<password> -all -b 10.1")
            print("You can elect to either use the full branch name or just the suffix")
            print("If you don't include '-b' branch will be assumed to be 'master'\n\n")
            print("Please ensure when executing the file that commands are typed in specified order.\n\n")
            print("If you have any difficulties, contact Nina at 'ninkin@yahoo.com'\n---------------------------------------")
            sys.exit()

        if not "-b" in argv:
            print("\nSince '-b <branch_name>' is not specified, we will zip master branch.\n")
            branch = 'master'
        else:
            i = argv.index("-b")
            branch = argv[i+1]

        #
        # Opens up repo_list.txt and writes all contents into a list to be used later
        #
        with open("repo_list.txt", 'r', newline='') as e:
            repo_list = []
            for i in e:
                repo_list.append(i.strip().split("|"))
        #print(repo_list) #FOR DEBUGGING PURPOSES

        # Will now look for and zip specific repositories specified by user
        if "-repo" in argv:
            start = argv.index("-repo") + 1
            if "-b" in argv:
                finish_index = argv.index("-b")
            else:
                finish_index = len(repo_list)
            desired_repos = argv[start:finish_index]
            for k in desired_repos:
                if k[0] in repo_list:
                    try:
                        zip([k[0].lower()], k[0], "", full_branch_name(branch, '-'))
                    except:
                        try:
                            zip([k[0].lower()], k[0], "", full_branch_name(branch, '/'))
                        except:
                            print("\n The Repository: '" + k[0] + "' was NOT found; UNABLE TO ZIP.\n")
                else:
                    print("\n The Repository: '" + k[0] + "' was NOT found; UNABLE TO ZIP.\n")

        elif "-groups" in argv:
            start = argv.index("-groups") + 1
            if "-b" in argv:
                finish_index = argv.index("-b")
            else:
                finish_index = len(repo_list)
            desired_groups = argv[start:finish_index]
            for s in repo_list:
                if s[1] in desired_groups:
                    try:
                        zip([s[0].lower()], s[0], "", full_branch_name(branch, '-'))
                    except:
                        try:
                            zip([s[0].lower()], s[0], "", full_branch_name(branch, '/'))
                        except:
                            print("\n Potential Syntax Error Detected for '" + s[0] + "' in repo_list.txt; UNABLE TO ZIP")


        # Will zip all repositories
        elif "-all" in argv:
            for j in repo_list:
                try:
                    zip([j[0].lower()], j[0], "", full_branch_name(branch, '-'))
                except:
                    try:
                        zip([j[0].lower()], j[0], "", full_branch_name(branch, '/'))
                    except:
                        print("\n Potential Syntax Error Detected for '" + j[0] + "' in repo_list.txt; UNABLE TO ZIP")


        # Will advise user of improper use of syntax
        else:
            print("\nPlease either include '-repo <repo names>' separated by white spaces as the script arguments for specific repositories, '-all' for all repositories,"
                  " OR '-groups <group names>' separated by white spaces as the script arguments for all repositories from specific groups.\n")


    except Exception as e:
        raise(e)


if __name__ == '__main__':
    sys.exit(main())