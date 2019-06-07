from miner import Miner


if __name__ == '__main__':
    miner = Miner()
    miner.prepare_docs()
    print(len(miner.categories))
    miner.fit(parameter_list={len(miner.categories)})

    miner.predict()
