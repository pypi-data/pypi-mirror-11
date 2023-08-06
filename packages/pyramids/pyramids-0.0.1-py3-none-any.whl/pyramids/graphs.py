__author__ = 'Aaron Hosford'
__all__ = [
    'LanguageContentHandler',
    'ParseGraph',
    'ParseGraphBuilder',
    'TestHandler',
]


class LanguageContentHandler:
    """A content handler for natural language, in the style of the
    ContentHandler class of the xml.sax module."""

    def handle_tree_end(self):
        """Called to indicate the end of a tree."""
        pass

    def handle_token(self, start_index, spelling, span, category):
        """Called to indicate the occurrence of a token."""
        pass

    def handle_root(self):
        """Called to indicate that the next token is the root."""
        pass

    def handle_link(self, source_start_index, sink_start_index, label):
        """Called to indicate the occurrence of a link between two tokens.
        Note that this will not be called until handle_token() has been
        called for both the source and sink."""
        pass

    def handle_phrase_start(self, head_start_index, category):
        """Called to indicate the start of a phrase."""
        pass

    def handle_phrase_end(self):
        """Called to indicate the end of a phrase."""
        pass


# TODO: Make this able to utilize a parser to construct a set of parse
#       trees that correspond to the sentence, and pick the one that has
#       the best score.
# TODO: Create Query class which represents the satisfaction set of a
#       sentence in terms of the actual logical structure, and which can
#       retrieve other queries or actual facts related to its meaning.
#       Then give this class a method that builds a Query instance
#       corresponding to it.
class ParseGraph:

    def __init__(self, root, tokens, links, phrases):
        self._root = root
        self._tokens = tuple(tokens)
        self._links = tuple(dict(sink_map) for sink_map in links)
        self._phrases = tuple(
            tuple(
                (
                    category,
                    frozenset(
                        (source, sink)
                        for source, sink in phrase_links
                    )
                )
                for category, phrase_links in phrase_stack
            )
            for phrase_stack in phrases
        )
        assert self._phrases and self._phrases[-1]

        self._reversed_links = tuple(
            {source: self._links[source][sink]
             for source in range(len(self._tokens))
             if sink in self._links[source]}
            for sink in range(len(self._tokens))
        )

    @property
    def root_index(self):
        return self._root

    @property
    def root_category(self):
        return self._phrases[self._root][-1][0]

    def __str__(self):
        result = str(self.root_category) + ':'
        for index in range(len(self._tokens)):
            result += '\n  '
            if index == self._root:
                result += '*'
            result += self._tokens[index][1] + ':'
            for sink, label in sorted(self._links[index].items()):
                result += (
                    '\n    ' + str(label) + ': ' +
                    self._tokens[sink][1]
                )
        return result

    def __getitem__(self, index):
        return self._tokens[index]

    def __len__(self):
        return len(self._tokens)

    def get_sinks(self, source):
        assert 0 <= source < len(self._tokens)
        return set(self._links[source])

    def get_sources(self, sink):
        assert 0 <= sink <= len(self._tokens)
        return set(self._reversed_links[sink])

    def get_label(self, source, sink, default=None):
        assert 0 <= source <= len(self._tokens)
        assert 0 <= sink <= len(self._tokens)
        return self._links[source].get(sink, default)

    def _get_phrase_tokens(self, head, indices):
        if head not in indices:
            indices.add(head)
            for sink in self.get_sinks(head):
                self._get_phrase_tokens(sink, indices)

    def get_phrase_tokens(self, head):
        assert 0 <= head <= len(self._tokens)
        indices = set()
        self._get_phrase_tokens(head, indices)
        return [self._tokens[index] for index in sorted(indices)]


class ParseGraphBuilder(LanguageContentHandler):
    """A simple class for representing language content as semantic graphs.
    """

    def __init__(self):
        self._root = None
        self._tokens = []
        self._links = []
        self._phrases = []

        self._start_index_map = {}
        self._graphs = []
        self._phrase_stack = []

    def get_graphs(self):
        if self._tokens:
            self.handle_tree_end()
        graphs = self._graphs
        self._graphs = []
        return graphs

    def handle_tree_end(self):
        assert self._root is not None
        assert not self._phrase_stack

        graph = ParseGraph(
            self._root,
            self._tokens,
            self._links,
            self._phrases
        )

        self._graphs.append(graph)

        self._root = None
        self._tokens.clear()
        self._links.clear()
        self._phrases.clear()
        self._start_index_map.clear()
        self._phrase_stack.clear()

    def handle_token(self, start_index, spelling, span, category):
        assert start_index not in self._start_index_map
        self._start_index_map[start_index] = len(self._tokens)
        self._tokens.append((start_index, spelling, span, category))
        self._links.append({})
        self._phrases.append([(category, frozenset())])

    def handle_root(self):
        assert self._root is None
        self._root = len(self._tokens)

    def handle_link(self, source_start_index, sink_start_index, label):
        assert source_start_index in self._start_index_map
        assert sink_start_index in self._start_index_map
        assert self._phrase_stack

        source_index = self._start_index_map[source_start_index]
        sink_index = self._start_index_map[sink_start_index]

        assert sink_index not in self._links[source_index]
        self._links[source_index][sink_index] = label

        self._phrase_stack[-1][-1].append((source_index, sink_index))

    def handle_phrase_start(self, head_start_index, category):
        # assert head_start_index in self._start_index_map
        # head_index = self._start_index_map[head_start_index]

        self._phrase_stack.append((
            head_start_index,  # head_index,
            category,
            []  # For links
        ))

    def handle_phrase_end(self):
        assert self._phrase_stack

        head_start_index, category, links = self._phrase_stack.pop()

        assert head_start_index in self._start_index_map

        head_index = self._start_index_map[head_start_index]
        self._phrases[head_index].append((category, frozenset(links)))


class TestHandler(LanguageContentHandler):

    def handle_tree_end(self):
        print("Tree end")

    def handle_token(self, start_index, spelling, category):
        print("Token:", start_index, spelling, category)

    def handle_root(self):
        print("Root")

    def handle_link(self, source_start_index, sink_start_index, label):
        print("Link:", source_start_index, sink_start_index, label)

    def handle_phrase_start(self, head_start_index, category):
        print("Phrase start:", head_start_index, category)

    def handle_phrase_end(self):
        print("Phrase end")
