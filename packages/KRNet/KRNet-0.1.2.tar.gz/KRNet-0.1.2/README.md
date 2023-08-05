Python3 package to construct a metabolic network (NetworkX DiGraph)
from a reaction set (with multiple KEGG Reactions in a file).
For KEGG Reaction file format refer:
<http://www.kegg.jp/kegg/rest/dbentry.html>

KRNet depends on NetworkX package.
<http://networkx.github.io/>

INSTALL
Use the following command to install krnet:
sudo pip install -e /path/to/downloaded/package

RUN
python3 <path/>krnet <KEGG_REACTIONS_FILE> <OUTFILE.gml>
