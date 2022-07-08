from pygit2 import Repository

from RepositoryWalkers.RepositoryWalker import RepositoryWalker
from Interoperability.ShellCommandExecuter import ShellCommandExecuter

class BranchToCommitWalker(RepositoryWalker):
    def __init__(self, repository: Repository, commit_to_stop_at):
        self.repository_directory = repository.path
        self.commit_to_stop_at = commit_to_stop_at
        super().__init__(repository)

    def walk(self, branch):
        for commit in super().walk(branch):
            yield commit
            if commit.hex == self.commit_to_stop_at:
                return

    def is_ancestor(self, commit, possible_ancestor):
        args = ['git', 'merge-base', '--is-ancestor', possible_ancestor, commit]
        executer = ShellCommandExecuter(self.repository_directory, args)
        return not executer.execute_for_return_code()