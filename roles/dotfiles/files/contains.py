# *****************************************************************************
#
# Copyright (C) 2009 VisoTech Softwareentwicklungsges.m.b.H.
# Contact: contact@visotech.at
# URL:     http://www.visotech.at
#
# This file may be used under the terms of the GNU General Public License
# version 2.0, or (at your option) any later version, as published by the
# Free Software Foundation and appearing in the file COPYING.txt included
# in the packaging of this file.
#
# This extension is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along
# with this extension. If not, see <http://www.gnu.org/licenses/>.
#
# *****************************************************************************
#
# contains.py - check simple relationships between mercurial changesets

"""tests parent-child relationships
"""
import re
from collections import deque
from mercurial.i18n import _
from mercurial import hg, cmdutil, error, util, commands

def _iter_transplants(repo, node):
    # hg transplant sets 'transplant_source'
    # hg graft sets 'source'
    extra_keys = set(["transplant_source", "source"])

    # start with the input node
    yield node
    try:
        while True:
            extra_data = node.extra()
            common_keys = set(extra_data.keys()) & extra_keys
            if not common_keys:
                break
            assert common_keys != extra_keys # there should be only 1 of the keys present
            node = repo[extra_data[common_keys.pop()]]
            yield node
    except (KeyError, error.RepoError):
        # no 'transplant_source' or the transplant source is
        # not in this repo
        pass

def _find_in_transplants(repo, stop_rev, node):
    transplant_chain = []
    for node in _iter_transplants(repo, node):
        transplant_chain.append(node)
        if node.rev() == stop_rev:
            return transplant_chain
    return []

#FIXME: use DFS in order to generate a 'trail' through the DAG from 'rev' to 'child'
def _find_changeset(repo, node, child, transplants):
    """ Looks for a changeset 'node' as parent to 'child'.
        Checks for transplanted changesets as well if 'transplants' is True.
    """
    stop_rev = node.rev()
    next_nodes = deque([child])
    seen_revs = set()

    while next_nodes:
        n = next_nodes.popleft()
        nrev = n.rev()

        if nrev in seen_revs:
            continue
        seen_revs.add(nrev)

        if nrev == stop_rev:
            return True, False

        if transplants:
            transplant_chain = _find_in_transplants(repo, stop_rev, n)
            if transplant_chain:
                seen_revs.update(transplant_chain)
                return True, True

        next_nodes.extend(n.parents())

    return False, False

def _int(x):
    try:
        return int(x)
    except ValueError:
        return None

def _resolve_node(ui, repo, rev, revno):
    node = repo[rev]

    # the 'rev' argument is supposed to be a revision number of 'revno' is set.
    irev = _int(rev)
    if revno and (irev != node.rev()):
        msg = _("lookup for revision '%s' yields changeset %s:%s\n") % (rev, node.rev(), str(node))
        raise util.Abort(msg)

    # see whether pattern matching magic was used
    if (str(node) != rev) and (irev != node.rev()):
        ui.warn(_("lookup for revision '%s' yields changeset %s:%s\n") % (rev, node.rev(), str(node)))
    return node

def contains(ui, repo, rev, child, transplants, revno, **opts):
    """tests whether a changeset is parent to another one

    This command tests whether the changeset given in 'rev' is a parent to
    the changeset given in 'child'. If no 'child' revision is given, the
    current working directory is used.
    If 'transplants' is given transplanted changesets are followed as well.

    If 'revno' is given the 'child' and 'rev' arguments are interpreted as
    revision numbers to prevent false positives due to pattern matching.
    You can use hashes instead of revision numbers to prevent pattern matching
    on the revision.
    """
    node = _resolve_node(ui, repo, rev, revno)
    # if child is given resolve it, else use the current checkout
    if child:
        child = _resolve_node(ui, repo, child, revno)
    else:
        child = repo['']
    if not (node and child):
        return -1

    found, transplanted = _find_changeset(repo, node, child, transplants)
    mparts = []
    if found:
        mparts.append(_("true"))
    else:
        mparts.append(_("false"))
    if transplanted:
        mparts.append(_("(transplanted)"))

    ui.status("%s\n" % " ".join(mparts))
    return not found

def headscontaining(ui, repo, rev, transplants, revno, **opts):
    """finds heads containing a specific changeset

    This command shows all heads containing the changeset given in 'rev'.
    If 'transplants' is given transplanted changesets are followed as well.

    If 'revno' is given the 'rev' argument is interpreted as revision
    number to prevent false positives due to pattern matching.
    You can use hashes instead of revision numbers to prevent pattern matching
    on the revision.
    """
    node = _resolve_node(ui, repo, rev, revno)
    if not node:
        return -1

    # get an unbuffered displayer
    displayer = cmdutil.show_changeset(ui, repo, opts, False)

    if opts["branchheads"]:
        # use branch heads (no topological children within the same branch, this
        # includes the last changeset in merged branches)
        heads = []
        for bheads in repo.branchmap().values():
            heads.extend(bheads)
    else:
        # use real heads (no topological children)
        heads = repo.heads()
    for head in heads:
        # FIXME: make _find_changeset using DFS and cache/reuse the changesets we
        # know to include/not include node.rev()
        found, transplanted = _find_changeset(repo, node, repo[head], transplants)
        if found:
            # let the user know which head we're talking about
            displayer.show(repo[head])

def _collect_changesets(repo, node, transplants):
    next_nodes = deque([node])
    csets = {}
    intermediate_transplants = set()
    transplanted = set()

    while next_nodes:
        n = next_nodes.popleft()

        # if we've already seen a node, but it was not a transplant_source,
        # there is no need to investigate it further.
        # otoh, if we've seen this node, but it was transplanted, then we're
        # coming here because the node was both transplanted and merged, so
        # we have to follow it's parents again.
        if n.hex() in transplanted:
            transplanted.remove(n.hex())
        elif n.hex() in csets:
            continue

        csets[n.hex()] = n
        next_nodes.extend(n.parents())

        if transplants:
            ts = list(_iter_transplants(repo, n))
            # remember repeatedly transplanted nodes (all but the last one in ts)
            intermediate_transplants.update(t.hex() for t in ts[:-1])
            # add the 'original' node
            if ts:
                ts = ts[-1]
                if ts.hex() in csets:
                    continue

                csets[ts.hex()] = ts
                transplanted.add(ts.hex())

    # discard all intermediate transplants
    for thex in intermediate_transplants:
        csets.pop(thex, None)

    return csets

def missing(ui, repo, target, source, transplants, revno, no_merges, no_tags, **opts):
    """finds changesets missing in a branch

    This command reports all changesets present in 'source' but not in
    'target'.
    If 'transplants' is given transplanted changesets are considered as well.
    If a changeset is transplanted repeatedly (x -> x' -> x'') the transplanted
    nodes x' and x'' are not considered but only the original changeset x.

    If 'revno' is given the 'target' and 'source' arguments are interpreted as
    revision numbers to prevent false positives due to pattern matching.
    You can use hashes instead of revision numbers to prevent pattern matching
    on the revision.
    """
    target = _resolve_node(ui, repo, target, revno)
    source = _resolve_node(ui, repo, source, revno)

    if not (source and target):
        return -1

    target_nodes = _collect_changesets(repo, target, transplants)
    source_nodes = _collect_changesets(repo, source, transplants)

    missing = set(source_nodes.keys()) - set(target_nodes.keys())
    # sort changesets by date
    def skey(chash):
        n = source_nodes[chash]
        return n.rev(), n.date()
    reverse = opts.get('reverse', False)
    missing = sorted(missing, key=skey, reverse=reverse)

    # get an unbuffered displayer
    displayer = cmdutil.show_changeset(ui, repo, opts, False)
    for m in missing:
        n = source_nodes[m]

        if opts['user'] != '' and opts['user'] not in n.user():
            continue
        if opts['description'] != '' and opts['description'] not in n.description():
            continue
        if no_merges and (len(n.parents()) > 1):
            continue
        if no_tags and n.files() == ['.hgtags']:
            continue
        if opts['no_empty'] and len(n.files()) == 0:
            continue
        if opts['file'] != "" and not reduce(lambda x,y: x or y, [re.match(opts['file'], f) for f in n.files()], False):
            continue
        if opts['branch'] != "" and opts['branch'] != n.branch():
            continue
        displayer.show(n)

cmdtable = {
        "contains" :
            (contains,
             [('c', 'child', '', _('check relationship to the given child changeset')),
              ('t', 'transplants', False, _('check transplanted changesets')),
              ('', 'revno', False, _('interpret arguments as revision number (no pattern magic)')),
             ],
             _('hg contains [-c child] [-t] [--revno] rev')),

        "headscontaining" :
            (headscontaining,
             [('t', 'transplants', False, _('check transplanted changesets')),
              ('b', 'branchheads', False, _('include heads of merged branches')),
              ('', 'revno', False, _('interpret argument as revision number (no pattern magic)')),
             ] + commands.templateopts,
             _('hg headscontaining [-t] [--revno] rev')),

        "missing" :
            (missing,
             [('t', 'transplants', False, _('check transplanted changesets')),
              ('', 'revno', False, _('interpret arguments as revision number (no pattern magic)')),
              ('M', 'no-merges', False, _('do not show merges')),
              ('E', 'no-empty', False, _('do not show empty commits (i.e. branch manipulation commits)')),
              ('r', 'reverse', False, _('reverse ordering')),
              ('f', 'file', "", _('show only changesets that change specified file')),
              ('b', 'branch', "", _('show only changesets that were made in specified branch (even if they were merged later)')),
              ('u', 'user', "", _('show only changesets from specified user')),
              ('d', 'description', "", _('show only changesets with description containing specified string')),
              ('T', 'no-tags', False, _('ignore changesets that only touch .hgtags')),
             ] + commands.templateopts,
             _('hg missing [-M] [-t] [-r] [--revno] [--no-tags] [--no-empty] [-b <branch>] [-d <description] [-f <file>] [-u <user>]  target source')),
    }
