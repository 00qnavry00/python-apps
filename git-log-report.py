#!/usr/bin/python

import sys
import os
from subprocess import check_output, STDOUT, CalledProcessError



#Tool to give list of branches between specified releases of either all repos or specific repos.



def git_report(repo, b1, b2, d1, d2):
    os.system("git clone https://github.com/00qnavry00/%s.git" % repo)
    os.chdir(repo)

    try:
        check_output(['git', 'checkout', '%s' % b1])
        check_output(['git', 'checkout', '%s' % b2])
        os.system("git log --pretty=format:%s origin/%s..origin/%s --after=%s --before=%s --date=short > ../git-revision-report-text/%s_revisions.txt" % ("%h%x09%ad", b1, b2, d1, d2, repo))
    except CalledProcessError:
        print("\n\nINVALID BRANCH NAME, USING ONLY DATES\n\n")
        os.system("git log --pretty=format:%s --after=%s --before=%s --date=short > ../git-revision-report-text/%s_revisions.txt" % ("%h%x09%ad", d1, d2, repo))
    os.chdir("../")
    os.system("rm -rf %s" % repo)


def main():
    # -repo <repo_name>  -branches <branch1> <branch2> -after 2019-03-24 -before 2019-09-30
    os.system("rm -rf git-revision-report-text")
    argv = sys.argv[1:]
    with open("repo_list.txt", 'r', newline='') as e:
        repo_list = []
        for i in e:
            repo_list.append(i.strip().split("|"))


    branch_start = argv[argv.index("-branches") + 1]
    branch_end = argv[argv.index("-branches") + 2]

    date_start = argv[argv.index("-after") + 1]
    date_end = argv[argv.index("-before") + 1]

    os.makedirs("git-revision-report-text")


    if "-all" in argv:
        for j in repo_list:
            git_report(j[0], branch_start, branch_end, date_start, date_end)


    elif "-repo" in argv:
        repo = argv[argv.index("-repo") + 1]
        git_report(repo, branch_start, branch_end, date_start, date_end)


    else:
        print("Incorrect format printed.")


if __name__ == '__main__':
    sys.exit(main())