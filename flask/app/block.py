import json
import os
import hashlib


class Blockchain:
    def __init__(self, working_dir=os.curdir + '/blockchain/'):
        self.working_dir = working_dir

    def get_hash(self, filename):
        file = open(self.working_dir + filename, 'rb').read()
        return hashlib.md5(file).hexdigest()

    def get_sorted_files_list(self):
        files = os.listdir(self.working_dir)
        return sorted([int(i) for i in files])

    def check_integrity(self):
        files = self.get_sorted_files_list()

        results = []

        for file in files[2:]:
            f = open(self.working_dir + str(file))
            h = json.load(f)['hash']

            prev_file = str(file - 1)
            actual_hash = self.get_hash(prev_file)

            if h == actual_hash:
                corrupted = False
            else:
                corrupted = True

            results.append({'block': prev_file, 'corrupted': corrupted})
        
        return results

    def has_corrupted_results(self, results):
        return any(res['corrupted'] == True for res in results)

    def write_block(self, name, amount, to_whom, prev_hash=''):
        files = self.get_sorted_files_list()
        last_file = files[-1]
        filename = str(last_file + 1)
        prev_hash = self.get_hash(str(last_file))

        data = {'name': name,
                'amount': amount,
                'to_whom': to_whom,
                'hash': prev_hash}
        with open(self.working_dir + filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_block(self, name, amount, to_whom, prev_hash=''):
        chain_blocks = self.check_integrity()
        chain_is_corrupted = self.has_corrupted_results(chain_blocks)
        if chain_is_corrupted == True:
            print("The Chain is corrupted. Can't write blocks.")
            return False
        else:
            self.write_block(name, amount, to_whom, prev_hash)
            print("The Block was added.")
            return True
        

def main():
    blockchanin_dir = os.curdir + '/blockchain/'
    blockchain = Blockchain(blockchanin_dir)
    blockchain.add_block('vasia', 4, 'john')


if __name__ == "__main__":
    main()