class BooleanEvaluator:
    def __init__(self, index):
        self.index = index

    def evaluate(self, node, all_docs: set[str]) -> set[str]:
        node_type = node[0]

        if node_type == "WORD":
            return self.index.get(node[1])

        if node_type == "AND":
            return self.evaluate(node[1], all_docs) & self.evaluate(node[2], all_docs)

        if node_type == "OR":
            return self.evaluate(node[1], all_docs) | self.evaluate(node[2], all_docs)

        if node_type == "NOT":
            return all_docs - self.evaluate(node[1], all_docs)

        raise ValueError("Unknown node")