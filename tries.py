def charPosition(c):
    c = c.lower()
    return ord(c) - ord("a")


def positionChar(i):
    az = "abcdefghijklmnopqrstuvwxyz"
    return az[i]


class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word):
        curr = self.root
        for char in word:
            charPos = charPosition(char)
            if curr.children[charPos] == None:
                curr.children[charPos] = TrieNode()
            curr = curr.children[charPos]
        curr.end = True

    def addManyWords(self, words):
        for word in words:
            self.addWord(word)

    def addSentenceWords(self, sentence):
        words = sentence.split(" ")
        self.addManyWords(words)

    def searchWord(self, pre):
        curr = self.root
        for char in pre:
            charPos = charPosition(char)
            if curr.children[charPos] == None:
                return False
            curr = curr.children[charPos]
        return True

    def fuzzySearch(self, word):
        from collections import deque  # deque only used in this function

        queue = deque([self.root])
        for char in word:
            newNodes = []
            if char == ".":
                while queue:
                    node = queue.popleft()
                    for child in node.children:
                        if child != None:
                            newNodes.append(child)
            else:
                charPos = charPosition(char)
                while queue:
                    node = queue.popleft()
                    if node.children[charPos] != None:
                        newNodes.append(node.children[charPos])
            queue.extend(newNodes)
        while queue:
            node = queue.popleft()
            if node.end:
                return True
        return False

    def listWords(self, prefix=""):
        words = []
        curr = self.root

        def dfs(currChar, currStr):
            nonlocal words
            for i, node in enumerate(currChar.children):
                if node != None:
                    char = positionChar(i)
                    if node.end == True:
                        words.append(currStr + char)
                    dfs(node, currStr + char)

        if prefix != "":
            for c in prefix:
                charPos = charPosition(c)
                curr = curr.children[charPos]
            if curr.end == True:
                words.append(prefix)

        dfs(curr, prefix)

        if not words:
            if prefix != "":
                return [f"No words with given prefix: {prefix}"]
            else:
                return [f"No words in trie as of yet"]
        else:
            return words
