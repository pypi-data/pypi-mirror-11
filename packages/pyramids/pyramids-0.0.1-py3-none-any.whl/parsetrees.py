from functools import reduce
import math
import time

from pyramids.exceptions import Timeout
from pyramids.categories import Category
from tokens import TokenSequence
import semantic_nets
import words

import pyramids.rules
import pyramids.parser

__author__ = 'Aaron Hosford'


class ParseTreeNode:
    """Represents a branch or leaf node in a parse tree."""

    def __init__(self, parser_state, rule, head_index, category,
                 index_or_components):
        if not isinstance(parser_state, pyramids.parser.ParserState):
            raise TypeError(parser_state, pyramids.parser.ParserState)
        if not isinstance(rule, pyramids.rules.ParseRule):
            raise TypeError(rule, pyramids.rules.ParseRule)
        if not isinstance(category, Category):
            raise TypeError(category, Category)
        self._parser_state = parser_state
        self._head_index = int(head_index)
        self._rule = rule
        if isinstance(index_or_components, int):
            self._start = index_or_components
            self._end = self._start + 1
            self._components = None
        else:
            self._components = tuple(index_or_components)
            if not self._components:
                raise ValueError(
                    "At least one component must be provided for a non-"
                    "leaf node."
                )
            for component in self._components:
                if not isinstance(component, ParseTreeNodeSet):
                    raise TypeError(component, ParseTreeNodeSet)
            self._start = self._end = self._components[0].start
            for component in self._components:
                if self._end != component.start:
                    raise ValueError(
                        "Discontinuity in component coverage."
                    )
                self._end = component.end
        self._category = category
        self._hash = (
            hash(self._rule) ^
            hash(self._head_index) ^
            hash(self._category) ^
            hash(self._start) ^
            hash(self._end) ^
            hash(self._components)
        )
        self._score = None
        self._raw_score = None

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, ParseTreeNode):
            return NotImplemented
        return self is other or (
            self._hash == other._hash and
            self._start == other._start and
            self._end == other._end and
            self._head_index == other._head_index and
            self._category == other._category and
            self._rule == other._rule and
            self._components == other._components
        )

    def __ne__(self, other):
        if not isinstance(other, ParseTreeNode):
            return NotImplemented
        return not (self == other)

    def __le__(self, other):
        if not isinstance(other, ParseTreeNode):
            return NotImplemented
        if self._start != other._start:
            return self._start < other._start
        if self._end != other._end:
            return self._end < other._end
        if self._head_index != other._head_index:
            return self._head_index < other._head_index
        if self._category != other._category:
            return self._category < other._category
        if self._rule != other._rule:
            return self._rule < other._rule
        return self._components <= other._components

    def __lt__(self, other):
        if not isinstance(other, ParseTreeNode):
            return NotImplemented
        if self._start != other._start:
            return self._start < other._start
        if self._end != other._end:
            return self._end < other._end
        if self._head_index != other._head_index:
            return self._head_index < other._head_index
        if self._category != other._category:
            return self._category < other._category
        if self._rule != other._rule:
            return self._rule < other._rule
        return self._components < other._components

    def __ge__(self, other):
        if not isinstance(other, ParseTreeNode):
            return NotImplemented
        return other <= self

    def __gt__(self, other):
        if not isinstance(other, ParseTreeNode):
            return NotImplemented
        return other < self

    def __repr__(self):
        # TODO: Update this
        if self.is_leaf():
            return (
                type(self).__name__ + "(" +
                repr(self._rule) + ", " +
                repr(self.span) + ")"
            )
        else:
            return (
                type(self).__name__ + "(" +
                repr(self._rule) + ", " +
                repr(self.components) + ")"
            )

    def __str__(self):
        return self.to_str()

    @property
    def tokens(self):
        return self._parser_state.tokens

    @property
    def rule(self):
        return self._rule

    @property
    def head_index(self):
        return self._head_index

    @property
    def category(self):
        return self._category

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def span(self):
        return self.start, self.end

    @property
    def components(self):
        return self._components

    @property
    def coverage(self):
        return (
            1
            if self.is_leaf()
            else reduce(lambda a, b: a * b.coverage, self.components, 1)
        )

    @property
    def head_token(self):
        return (
            self.tokens[self._start]
            if self.is_leaf()
            else self._components[self._head_index].head_token
        )

    def is_leaf(self):
        return self._components is None

    def to_str(self, simplify=False):
        result = self.category.to_str(simplify) + ':'
        if self.is_leaf():
            covered_tokens = ' '.join(self.tokens[self.start:self.end])
            result += ' ' + repr(covered_tokens) + ' ' + repr(self.span)
            if not simplify:
                result += ' [' + str(self.rule) + ']'
        elif len(self.components) == 1 and simplify:
            result += ' ' + self.components[0].to_str(simplify)
        else:
            if not simplify:
                result += ' [' + str(self.rule) + ']'
            for component in self.components:
                result += (
                    '\n    ' +
                    component.to_str(simplify).replace('\n', '\n    ')
                )
        return result

    def restrict(self, categories):
        for category in categories:
            if self._category in category:
                yield self
                break
        else:
            if self._components:
                for component in self._components:
                    for restriction in component.restrict(categories):
                        yield restriction

    def weighted_score_is_dirty(self):
        if self.is_leaf():
            return False
        for component in self.components:
            if component.weighted_score_is_dirty():
                return True
        return False

    def _calculate_weighted_score(self):
        total_weighted_score, total_weight = \
            self.rule.calculate_weighted_score(self)
        if self.is_leaf():
            depth = 1
        else:
            depth = total_weight
            for component in self.components:
                component_depth, weighted_score, weight = \
                    component._calculate_weighted_score()

                # It's already weighted, so don't multiply it
                total_weighted_score += weighted_score

                total_weight += weight
                depth += component_depth * weight
            depth /= total_weight

            # TODO: At each level, divide both values by the number of
            #       values summed. This way we have a usable confidence
            #       score between 0 and 1 that comes out at the top.
            # self._score = total_weighted_score, total_weight

        # return self._score

        self._raw_score = (depth, total_weighted_score, total_weight)
        self._score = (
            total_weighted_score / math.log(1 + depth, 2),
            total_weight
        )

        return self._raw_score

    def calculate_weighted_score(self):
        self._calculate_weighted_score()
        return self._score

    def _get_weighted_score(self):
        if self._score is None or self.weighted_score_is_dirty():
            self._calculate_weighted_score()
        return self._raw_score

    def get_weighted_score(self):
        if self._score is None or self.weighted_score_is_dirty():
            self._calculate_weighted_score()
        return self._score

    def adjust_score(self, target):
        self.rule.adjust_score(self, target)
        if not self.is_leaf():
            for component in self.components:
                component.adjust_score(target)
        self._score = None

    def build_language_graph(self, language_graph_builder):
        """Accepts a new, unfinished sentence and fills it by adding nodes
        and links according to the parse tree's structure and its rule's
        indications, returning the head node(s) of the subtree in a
        frozenset."""
        if self.is_leaf():
            head = language_graph_builder.add_word_use(
                self.tokens[self.start],
                self.category,
                self.span
            )
            need_sources = {}
            for prop in self.category.positive_properties:
                if prop.name.startswith(('needs_', 'takes_')):
                    need_sources[prop.name[6:]] = {head}
            return head, need_sources

        # Build the subgraph corresponding to each subtree, remembering
        # which node in the subgraph is to receive which potential links.
        nodes = []
        need_sources = {}
        head_need_sources = {}
        index = 0
        for component in self.components:
            component_head, component_need_sources = \
                component.build_language_graph(language_graph_builder)
            nodes.append(component_head)
            for property_name in component_need_sources:
                # if (Property('needs_'+ property_name) not in
                #         self.category.positive_properties and
                #         Property('takes_'+ property_name) not in
                #         self.category.positive_properties):
                #     continue
                if property_name in need_sources:
                    need_sources[property_name] |= component_need_sources[
                        property_name]
                else:
                    need_sources[property_name] = component_need_sources[
                        property_name]
            if index == self._head_index:
                head_need_sources = component_need_sources
            index += 1

        # Add the links as appropriate for the rule used to build this tree
        head = nodes[self._head_index]
        language_graph_builder.set_tree_category(head, self.category)
        for index in range(len(self.components) - 1):
            link_type_set = self.rule.get_link_types(self, index)
            if index < self._head_index:
                left_side = nodes[index]
                right_side = head
            else:
                left_side = head
                right_side = nodes[index + 1]
            for link_type, left, right in link_type_set:
                if left:
                    if link_type.lower() in head_need_sources:
                            # and not (
                            # Property('needs_' + link_type.lower()) in
                            # self.category.positive_properties or
                            # Property('takes_' + link_type.lower()) in
                            # self.category.positive_properties):
                        for node in need_sources[link_type.lower()]:
                            semantic_nets.Link(
                                node,
                                link_type,
                                left_side
                            ).connect()
                    elif (link_type[-3:].lower() == '_of' and
                            link_type[:-3].lower() in head_need_sources):
                        for node in need_sources[link_type[:-3].lower()]:
                            semantic_nets.Link(
                                left_side,
                                link_type,
                                node
                            ).connect()
                    else:
                        semantic_nets.Link(
                            right_side,
                            link_type,
                            left_side
                        ).connect()
                if right:
                    if link_type.lower() in head_need_sources:
                            # and not (
                            # Property('needs_' + link_type.lower()) in
                            # self.category.positive_properties or
                            # Property('takes_' + link_type.lower()) in
                            # self.category.positive_properties):
                        for node in need_sources[link_type.lower()]:
                            semantic_nets.Link(
                                node,
                                link_type,
                                right_side
                            ).connect()
                    elif (link_type[-3:].lower() == '_of' and
                            link_type[:-3].lower() in head_need_sources):
                        for node in need_sources[link_type[:-3].lower()]:
                            semantic_nets.Link(
                                right_side,
                                link_type,
                                node
                            ).connect()
                    else:
                        semantic_nets.Link(
                            left_side,
                            link_type,
                            right_side
                        ).connect()

        # Figure out which nodes should get which links from outside this
        # subtree
        words.WordUse(head).roles.append(self.category)
        parent_need_sources = {}
        for prop in self.category.positive_properties:
            if prop.name.startswith(('needs_', 'takes_')):
                if prop.name[6:] in need_sources:
                    parent_need_sources[prop.name[6:]] = \
                        need_sources[prop.name[6:]]
                else:
                    parent_need_sources[prop.name[6:]] = {head}
        return head, parent_need_sources


# TODO: Merge ParseTreeNode and BuildTreeNode, making it possible to assign
#       a semantic net node and token index/range in the parse tree node
#       after the tree has been built. These values will be extra data that
#       isn't necessary to build the tree. During parsing, no semantic net
#       nodes will be stored in the tree node, and when the language graph
#       is built these values will be fixed. During building, no token
#       interval/index values will be stored in the tree node, and when
#       they are requested after the tree is built, they will be calculated
#       and stored.
class BuildTreeNode:
    def __init__(self, rule, category, head_node, components=None):
        # TODO: Type checking
        self._rule = rule
        self._category = category
        self._head_node = head_node
        self._components = None if components is None else tuple(
            components)
        self._nodes = (
            (head_node,)
            if components is None
            else sum([component.nodes for component in components], ())
        )
        self._node_coverage = frozenset(self._nodes)
        self._tokens = tuple([node.spelling for node in self._nodes])
        self._hash = None

    def __repr__(self):
        if self.is_leaf():
            return (
                type(self).__name__ + "(" +
                repr(self._rule) + ", " +
                repr(self.category) + ", " +
                repr(self._head_node) + ")"
            )
        else:
            return (
                type(self).__name__ + "(" +
                repr(self._rule) + ", " +
                repr(self.category) + ", " +
                repr(self._head_node) + ", " +
                repr(self.components) + ")"
            )

    def __str__(self):
        return self.to_str()

    def __hash__(self):
        if self._hash is None:
            self._hash = (
                hash(self._rule) ^
                hash(self._category) ^
                hash(self._head_node) ^
                hash(self._components)
            )
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, BuildTreeNode):
            return NotImplemented
        return (
            self._rule == other._rule and
            self._category == other._category and
            self._head_node == other._head_node and
            self._components == other._components
        )

    def __ne__(self, other):
        if not isinstance(other, BuildTreeNode):
            return NotImplemented
        return (
            self._rule != other._rule or
            self._category != other._category or
            self._head_node != other._head_node or
            self._components != other._components
        )

    def __le__(self, other):
        if not isinstance(other, BuildTreeNode):
            return NotImplemented
        if self._tokens != other._tokens:
            return self._tokens < other._tokens
        if self._rule != other._rule:
            return self._rule < other._rule
        if self._category != other._category:
            return self._category < other._category
        if self._head_node.spelling != other._head_node.spelling:
            return self._head_node.spelling < other._head_node.spelling
        return self._components <= other._components

    def __ge__(self, other):
        if not isinstance(other, BuildTreeNode):
            return NotImplemented
        return other <= self

    def __lt__(self, other):
        if not isinstance(other, BuildTreeNode):
            return NotImplemented
        if self._tokens != other._tokens:
            return self._tokens < other._tokens
        if self._rule != other._rule:
            return self._rule < other._rule
        if self._category != other._category:
            return self._category < other._category
        if self._head_node.spelling != other._head_node.spelling:
            return self._head_node.spelling < other._head_node.spelling
        return self._components < other._components

    def __gt__(self, other):
        if not isinstance(other, BuildTreeNode):
            return NotImplemented
        return other < self

    @property
    def rule(self):
        return self._rule

    @property
    def category(self):
        return self._category

    @property
    def head_node(self):
        return self._head_node

    @property
    def components(self):
        return self._components

    @property
    def nodes(self):
        return self._nodes

    @property
    def node_coverage(self):
        return self._node_coverage

    @property
    def tokens(self):
        return self._tokens

    def is_leaf(self):
        return self._components is None

    def to_str(self, simplify=False):
        result = self.category.to_str(simplify) + ':'
        if self.is_leaf():
            covered_tokens = ' '.join(self.tokens)
            result += ' ' + repr(covered_tokens)
            if not simplify:
                result += ' [' + str(self.rule) + ']'
        elif len(self.components) == 1 and simplify:
            result += ' ' + self.components[0].to_str(simplify)
        else:
            if not simplify:
                result += ' [' + str(self.rule) + ']'
            for component in self.components:
                result += (
                    '\n    ' +
                    component.to_str(simplify).replace('\n', '\n    ')
                )
        return result


# TODO: Each of these really represents a group of parses having the same
#       root form. In Parse, when we get a list of ranked parses, we're
#       ignoring all the other parses that have the same root form. While
#       this *usually* means we see all the parses we actually care to see,
#       sometimes there is an alternate parse with the same root form which
#       actually has a higher rank than the best representatives of other
#       forms. When this happens, we want to see this alternate form, but
#       we don't get to. Create a method in Parse (along with helper
#       methods here) to allow the caller to essentially treat the Parse as
#       a priority queue for the best parses, so that we can iterate over
#       *all* complete parses in order of score and not just those that are
#       the best for each root form, but without forcing the caller to wait
#       for every single complete parse to be calculated up front. That is,
#       we should iteratively expand the parse set just enough to find the
#       next best parse and yield it immediately, keeping track of where we
#       are in case the client isn't satisfied.
#
#       Now that I think about it, the best way to implement this is
#       literally with a priority queue. We create an iterator for each
#       top-level parse set, which iterates over each alternative parse
#       with the same root form, and we get the first parse from each one.
#       We then rank each iterator by the quality of the parse we got from
#       it. We take the best one & yield its parse, then grab another parse
#       from it and re-rank the iterator by the new parse, putting it back
#       into the priority queue. If no more parses are available from one
#       of the iterators, we don't add it back to the priority queue. When
#       the priority queue is empty, we return from the method. Probably
#       what's going to happen is each of these iterators is actually going
#       to use a recursive call back into the same method for each child of
#       the root node, putting the pieces together to create the next best
#       alternate parse.
class ParseTreeNodeSet:

    def __init__(self, nodes):  # Always has to contain at least one node.
        if isinstance(nodes, ParseTreeNode):
            nodes = [nodes]
        self._unique = set()
        self._best_node = None
        self._best_score = None
        self._best_raw_score = None
        values_set = False
        for node in nodes:
            if not values_set:
                self._start = node.start
                self._end = node.end
                self._category = node.category
                values_set = True
            self.add(node)
        if not values_set:
            raise ValueError(
                "ParseTreeNodeSet must contain at least one node.")
        self._hash = (
            hash(self._start) ^
            hash(self._end) ^
            hash(self._category)
        )

    def __repr__(self):
        return type(self).__name__ + "(" + repr(self._unique) + ")"

    def __iter__(self):
        return iter(self._unique)

    def __len__(self):
        return len(self._unique)

    def __contains__(self, node):
        return node in self._unique

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, ParseTreeNodeSet):
            return NotImplemented
        return self is other or (
            self._hash == other._hash and
            self._start == other._start and
            self._end == other._end and
            self._category == other._category
        )

    def __ne__(self, other):
        if not isinstance(other, ParseTreeNodeSet):
            return NotImplemented
        return not self == other

    def __le__(self, other):
        if not isinstance(other, ParseTreeNodeSet):
            return NotImplemented
        if self._start != other._start:
            return self._start < other._start
        if self._end != other._end:
            return self._end < other._end
        return self._category <= other._category

    def __ge__(self, other):
        if not isinstance(other, ParseTreeNodeSet):
            return NotImplemented
        return other <= self

    def __lt__(self, other):
        if not isinstance(other, ParseTreeNodeSet):
            return NotImplemented
        return not (self >= other)

    def __gt__(self, other):
        if not isinstance(other, ParseTreeNodeSet):
            return NotImplemented
        return not (self <= other)

    def __str__(self):
        return self.to_str()

    @property
    def category(self):
        return self._category

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def span(self):
        return self._start, self._end

    @property
    def count(self):
        return len(self._unique)

    @property
    def best(self):
        return self._best_node

    @property
    def coverage(self):
        return sum([node.coverage for node in self._unique])

    @property
    def head_token(self):
        return self._best_node.head_token

    def is_compatible(self, node_or_set):
        if not isinstance(node_or_set, (ParseTreeNode, ParseTreeNodeSet)):
            raise TypeError(node_or_set, (ParseTreeNode, ParseTreeNodeSet))
        return (node_or_set.start == self._start and
                node_or_set.end == self._end and
                node_or_set.category == self._category)

    def add(self, node):
        if not isinstance(node, ParseTreeNode):
            raise TypeError(node, ParseTreeNode)
        if not self.is_compatible(node):
            raise ValueError("Node is not compatible.")
        if node in self._unique:
            return
        self._unique.add(node)
        score = node.get_weighted_score()
        if self._best_score is None or score > self._best_score:
            self._best_score = score
            self._best_node = node

    # TODO: Scoring is all jacked up! All these methods with ambiguous
    #       names and purposes... It's not even clear what's happening.
    def weighted_score_is_dirty(self):
        for node in self._unique:
            if node.weighted_score_is_dirty():
                return True
        return False

    def _calculate_weighted_score(self):
        self._best_score = (
            self._best_node.calculate_weighted_score()
            if self._best_node is not None
            else None
        )
        self._best_raw_score = (
            self._best_node._get_weighted_score()
            if self._best_node is not None
            else None
        )
        for node in self._unique:
            score = node.get_weighted_score()
            if self._best_score is None or score > self._best_score:
                self._best_score = score
                self._best_node = node
                self._best_raw_score = node._get_weighted_score()
        return self._best_raw_score

    def calculate_weighted_score(self):
        self._calculate_weighted_score()
        return self._best_score

    def _get_weighted_score(self):
        if self.weighted_score_is_dirty():
            self.calculate_weighted_score()
        return self._best_raw_score

    def get_weighted_score(self):
        if self.weighted_score_is_dirty():
            self.calculate_weighted_score()
        return self._best_score

    def adjust_score(self, target):
        self._best_node.adjust_score(target)

    def to_str(self, simplify=False):
        return self._best_node.to_str(simplify)

    def restrict(self, categories):
        for category in categories:
            if self._category in category:
                yield self
                break
        else:
            for node in self._unique:
                for restriction in node.restrict(categories):
                    yield restriction

    def build_language_graph(self, language_graph_builder):
        return self._best_node.build_language_graph(language_graph_builder)


class ParseTree:
    """Represents a complete parse tree."""

    def __init__(self, tokens, root):
        if not isinstance(tokens, TokenSequence):
            raise TypeError(tokens, TokenSequence)
        self._tokens = tokens
        if not isinstance(root, ParseTreeNodeSet):
            raise TypeError(root, ParseTreeNodeSet)
        self._root = root

    def __repr__(self):
        return type(self).__name__ + "(" + repr(
            self._tokens) + ", " + repr(self._root) + ")"

    def __str__(self):
        return self.to_str()

    def __hash__(self):
        return hash(self._tokens) ^ hash(self._root)

    def __eq__(self, other):
        if not isinstance(other, ParseTree):
            return NotImplemented
        return self is other or (
            self._tokens == other._tokens and
            self._root == other._root
        )

    def __ne__(self, other):
        if not isinstance(other, ParseTree):
            return NotImplemented
        return not (self == other)

    def __le__(self, other):
        if not isinstance(other, ParseTree):
            return NotImplemented
        if self is other:
            return True
        if self._tokens != other._tokens:
            return self._tokens < other._tokens
        return self._root <= other._root

    def __lt__(self, other):
        if not isinstance(other, ParseTree):
            return NotImplemented
        if self is other:
            return False
        if self._tokens != other._tokens:
            return self._tokens < other._tokens
        return self._root < other._root

    def __ge__(self, other):
        if not isinstance(other, ParseTree):
            return NotImplemented
        return other <= self

    def __gt__(self, other):
        if not isinstance(other, ParseTree):
            return NotImplemented
        return other < self

    @property
    def tokens(self):
        return self._tokens

    @property
    def root(self):
        return self._root

    @property
    def category(self):
        return self._root.category

    @property
    def start(self):
        return self._root.start

    @property
    def end(self):
        return self._root.end

    @property
    def span(self):
        return self._root.span

    @property
    def coverage(self):
        return self._root.coverage

    def to_str(self, simplify=True):
        return self._root.to_str(simplify)

    def restrict(self, categories):
        results = set()
        for node in self._root.restrict(categories):
            results.add(type(self)(self._tokens, node))
        return results

    def is_ambiguous_with(self, other):
        return (
            self.start <= other.start < self.end or
            other.start <= self.start < other.end
        )

    def weighted_score_is_dirty(self):
        return self.root.weighted_score_is_dirty()

    def calculate_weighted_score(self):
        return self.root.calculate_weighted_score()

    def get_weighted_score(self):
        return self.root.get_weighted_score()

    def adjust_score(self, target):
        self.root.adjust_score(target)

    def build_language_graph(self, language_graph_builder):
        head, need_sources = self.root.build_language_graph(
            language_graph_builder)
        # TODO: Make sure need_sources is empty. If not, it's a bad parse
        #       tree. This case should be detected when the Parse instance
        #       is created, and bad trees should automatically be filtered
        #       out then, so we should *never* get a need source here.
        language_graph_builder.add_head(head, self.category)
        return head


class Parse:
    # TODO: Make sure the docstrings are up to date.
    """A finished parse. Stores the state of the parse during Parser's
    operation as a separate, first class object. Because a sentence can
    potentially be parsed in many different ways, also represents the
    collection of ParseTrees which apply to the input after parsing is
    complete."""

    def __init__(self, tokens, parse_trees):
        self._tokens = tokens
        self._parse_trees = frozenset(parse_trees)
        self._hash = None
        self._score = None

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self._tokens) ^ hash(self._parse_trees)
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, Parse):
            return NotImplemented
        return self is other or (
            self._tokens == other._tokens and
            self._parse_trees == other._parse_trees
        )

    def __ne__(self, other):
        if not isinstance(other, Parse):
            return NotImplemented
        return not (self == other)

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return type(self).__name__ + "(" + repr(
            self._tokens) + ", " + repr(self._parse_trees) + ")"

    @property
    def tokens(self):
        return self._tokens

    @property
    def parse_trees(self):
        return self._parse_trees

    @property
    def coverage(self):
        return sum([tree.coverage for tree in self._parse_trees])

    def to_str(self, simplify=True):
        return '\n'.join(
            [tree.to_str(simplify) for tree in sorted(self._parse_trees)])

    def get_rank(self):
        score, weight = self.get_weighted_score()
        return (
            self.total_gap_size(),
            len(self.parse_trees),
            -score,
            -weight
        )

    def weighted_score_is_dirty(self):
        if self._score is None:
            return True
        for tree in self._parse_trees:
            if tree.weighted_score_is_dirty():
                return True
        return False

    def calculate_weighted_score(self):
        total_weighted_score = 0.0
        total_weight = 0.0
        for tree in self._parse_trees:
            weighted_score, weight = tree.get_weighted_score()
            total_weighted_score += weighted_score
            total_weight += weight
        self._score = (
            (total_weighted_score / total_weight if total_weight else 0.0),
            total_weight
        )
        return self._score

    def get_weighted_score(self):
        if self.weighted_score_is_dirty():
            self.calculate_weighted_score()
        return self._score

    def adjust_score(self, target):
        for tree in self._parse_trees:
            tree.adjust_score(target)

    def restrict(self, categories):
        if isinstance(categories, Category):
            categories = [categories]
        trees = []
        for tree in self._parse_trees:
            for restricted in tree.restrict(categories):
                trees.append(restricted)
        return type(self)(self._tokens, trees)

    def iter_ambiguities(self):
        covered = set()
        for tree1 in self._parse_trees:
            covered.add(tree1)
            for tree2 in self._parse_trees:
                if tree2 in covered:
                    continue
                if tree1.is_ambiguous_with(tree2):
                    yield tree1, tree2

    def is_ambiguous(self):
        for _ in self.iter_ambiguities():
            return True
        return False

    def disambiguate(self):
        if len(self._parse_trees) <= 1:
            return self
        scores = {}
        for tree in self._parse_trees:
            scores[tree] = tree.get_weighted_score()
        trees = []
        for tree in sorted(scores, key=scores.get, reverse=True):
            for other_tree in trees:
                if tree.is_ambiguous_with(other_tree):
                    break
            else:
                trees.append(tree)
        return type(self)(self._tokens, trees)

    def _iter_disambiguation_tails(self, index, max_index, gaps, pieces,
                                   timeout):
        if timeout is not None and time.time() >= timeout:
            raise Timeout()
        if index >= len(self._tokens):
            if not gaps and not pieces:
                yield []
        elif index < max_index and pieces > 0:
            nearest_end = None
            for tree in self._parse_trees:
                if tree.start == index:
                    if nearest_end is None or tree.end < nearest_end:
                        nearest_end = tree.end
                    for tail in self._iter_disambiguation_tails(
                            tree.end,
                            max_index,
                            gaps,
                            pieces - 1,
                            timeout):
                        yield [tree] + tail
            if nearest_end is None:
                if gaps > 0:
                    for tail in self._iter_disambiguation_tails(
                            index + 1,
                            max_index,
                            gaps - 1,
                            pieces,
                            timeout):
                        yield tail
            else:
                for overlap_index in range(index + 1, nearest_end):
                    for tail in self._iter_disambiguation_tails(
                            overlap_index,
                            nearest_end,
                            gaps,
                            pieces,
                            timeout):
                        yield tail

    # TODO: This fails if we have a partial parse in the *middle* of the
    #       string, surrounded by gaps.
    def iter_disambiguations(self, gaps=None, pieces=None, timeout=None):
        if gaps is None:
            gaps_seq = range(self.total_gap_size(), len(self._tokens) + 1)
        else:
            gaps_seq = [gaps] if gaps >= self.total_gap_size() else []
        if pieces is None:
            pieces_seq = range(self.min_disambiguation_size(),
                               len(self._tokens) + 1)
        else:
            pieces_seq = [
                pieces] if pieces >= self.min_disambiguation_size() else []
        try:
            success = False
            for gaps in gaps_seq:
                for pieces in pieces_seq:
                    for tail in self._iter_disambiguation_tails(0, len(
                            self._tokens), gaps, pieces, timeout):
                        yield type(self)(self._tokens, tail)
                        success = True
                    if success:
                        break
                if success:
                    break
        except Timeout:
            # Don't do anything; we just want to exit early if this
            # happens.
            pass

    def get_disambiguations(self, gaps=None, pieces=None, timeout=None):
        return set(self.iter_disambiguations(gaps, pieces, timeout))

    def get_ranked_disambiguations(self, gaps=None, pieces=None,
                                   timeout=None):
        ranks = {}
        for disambiguation in self.get_disambiguations(gaps, pieces,
                                                       timeout):
            ranks[disambiguation] = disambiguation.get_rank()
        return ranks

    def get_sorted_disambiguations(self, gaps=None, pieces=None,
                                   timeout=None):
        ranks = self.get_ranked_disambiguations(gaps, pieces, timeout)
        return [
            (disambiguation, ranks[disambiguation])
            for disambiguation in sorted(ranks, key=ranks.get)
        ]

    def iter_gaps(self):
        gap_start = None
        index = -1
        for index in range(len(self._tokens)):
            for tree in self._parse_trees:
                if tree.start <= index < tree.end:
                    if gap_start is not None:
                        yield gap_start, index
                        gap_start = None
                    break
            else:
                if gap_start is None:
                    gap_start = index
        if gap_start is not None:
            yield gap_start, index + 1

    def has_gaps(self):
        for _ in self.iter_gaps():
            return True
        return False

    def total_gap_size(self):
        size = 0
        for start, end in self.iter_gaps():
            size += end - start
        return size

    def max_tree_width(self):
        max_width = 0
        for tree in self._parse_trees:
            width = tree.end - tree.start
            if max_width is None or width > max_width:
                max_width = width
        return max_width

    def min_disambiguation_size(self):
        max_width = self.max_tree_width()
        if not max_width:
            return 0
        return int(math.floor(len(self._tokens) / float(max_width)))

    def build_language_graph(self, language_graph_builder):
        scores = {}
        for tree in self._parse_trees:
            scores[tree] = tree.get_weighted_score()
        heads = []
        for tree in sorted(
                self._parse_trees,
                key=lambda tree: (
                    tree.start,
                    -tree.end,
                    -scores[tree][0],
                    -scores[tree][1])):
            heads.append(tree.build_language_graph(language_graph_builder))
        return heads