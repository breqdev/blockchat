import hashlib
import json

import powlib

class Block:
    def __init__(self, index, data, powval, lastHash, hash=None):
        self.index = index
        self.data = data
        self.powval = powval
        self.lastHash = lastHash
        self.hash = hash or self.hashme()

    def __str__(self):
        """ String representation of the block.
            Does NOT include the current hash!
            (Intended to be called from the hasher function.)
        """
        
        return json.dumps({"index": self.index,
                           "data": self.data,
                           "powval": self.powval,
                           "lastHash": self.lastHash})

    def hashme(self):
        sha256 = hashlib.sha256()
        sha256.update(str(self).encode("utf-8"))
        return sha256.hexdigest()

    def dictrep(self):
        return {"index": self.index,
                "data": self.data,
                "powval": self.powval,
                "lastHash": self.lastHash,
                "hash": self.hash}

class Blockchain:
    def __init__(self, blocks=[]):
        self.blocks = blocks

    def genesis(self):
        self.blocks = [Block(0, ["Genesis Block"], 0, "0")]

    def add_block(self, data):
        last = self.blocks[-1]
        powval = powlib.compute(last.powval)
        self.blocks.append(Block(last.index + 1, data, powval, last.hash))

    def verify(self):
        biggestPow = -1
        for i in range(1, len(self.blocks)):
            if self.blocks[i].lastHash != self.blocks[i-1].hash:
                return False
            if self.blocks[i].powval <= biggestPow:
                return False
            biggestPow = self.blocks[i].powval
        return True

    def consensus(self, other):
        "Gets the current consensus. If it's our chain, returns True."
        if not Blockchain.verify(other):
            return True
        if not self.verify():
            self.blocks = other.blocks
            return False
        if len(other.blocks) > len(self.blocks):
            self.blocks = other.blocks
            return False # keep valid chain with most blocks
        return True

    def jsonrep(self):
        return json.dumps([block.dictrep() for block in self.blocks])

    def fromjson(message):
        jblocks = json.loads(message)
        chain = []
        for jblock in jblocks:
            chain.append(Block(jblock["index"], jblock["data"],
                               jblock["powval"], jblock["lastHash"],
                               jblock["hash"]))
        return Blockchain(chain)
